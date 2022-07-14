# =================================== IMPORTS FOR DATA ==================================
import datetime
from decimal import Decimal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout,InputLayer
from keras.metrics import SquaredHinge, mean_absolute_error
import math
from sklearn.preprocessing import MinMaxScaler

# =============================== IMPORTS FOR STATIC LINK ===============================
from goldprice.models import GoldPrice,GoldPricePredictions


# ===================================== MISC IMPORTS ====================================
import os
import time
# ===================================== CONSTANTS ====================================



class DataManager :
    def __init__(self): 
        # load current data :------------------------------
        # 1- get from the DB :
        allData = GoldPrice.objects.all()
        onlyClose = []
        # 2- make it in DF format :
        l = len(allData)
        for i in range(l) :
            close = float(allData[i].close)
            onlyClose.append(close)
        self.data_DataFrame = pd.DataFrame(onlyClose)
        self.allData = allData
        # load and initialise scaler : ----------------------
        scaler = MinMaxScaler(feature_range=(0,1))
        scaler.fit_transform(self.data_DataFrame)
        self.scaler = scaler 
        print("[DATAMANAGER] data_DataFrame : ",self.data_DataFrame)
        print("[DATAMANAGER] scaler : ",self.scaler)


    def SplitData(self,WindowSize,ratio = 0.8):
        dataToSplit = self.data_DataFrame

        if ratio > 1 or ratio < 0 :
            print("Ratio should be within 0 & 1")
            return
        
        training_data_len = math.ceil(len(dataToSplit) *ratio)
        len_dataToSplit =  len(dataToSplit)
        #create the sclaed training dataset
        print("Processing the Training Dataset ...")
        train_data = dataToSplit[len_dataToSplit-training_data_len:,:]
        
        #split the data into x_subject and y_subject datasets
        x_subject = []
        y_subject = []
        for i in range(WindowSize,len(train_data)):
            x_subject.append(train_data[i-WindowSize:i,0])
            y_subject.append(train_data[i,0])
            
        #Transform into ndarray
        x_subject = np.array(x_subject)
        y_subject = np.array(y_subject)
        #reshape :
        x_subject = np.reshape(x_subject , (x_subject.shape[0],x_subject.shape[1],1))
        return (x_subject,y_subject)


    def createDataset(self,WindowSize,ratio = .8):
        data = self.data_DataFrame
        # rescaling data
        scaler = self.scaler
        scaled_data = scaler.fit_transform(data)
        # splitting data
        x_subject,y_subject = self.SplitData(WindowSize,scaled_data,ratio= ratio)
        return x_subject,y_subject

    def generateDates(self,n = 100):
        """
        Generates n Dates starting from the last on in the real database
        """
        l = len(self.allData)
        lastDate = self.allData[l-1].date
        start_date = datetime.date( lastDate.year, 
                                    lastDate.month, 
                                    lastDate.day)
        date_list = []
        for day in range(n+1):
            a_date = (start_date + datetime.timedelta(days = day)).isoformat()
            date_list.append(a_date)
        return date_list[1:]



    def updatePredictionDB(self,newPredictions):
        # get list of dates :
        futureDates = self.generateDates()
        # empty the db :
        GoldPricePredictions.resetAllData()
        # 3emer dinmha
        l = len(GoldPrice.objects.all())
        old_element = GoldPrice.objects.all()[l-1]
        for idx, el in enumerate(newPredictions)  :
            v = Decimal.from_float(float(el[0]))

            prediction_entry = GoldPricePredictions(  
                date = futureDates[idx],
                close = v,
                growth = ((v - old_element.close) / old_element.close )* 100,
                currency = 'USD'
            )
            old_element = prediction_entry
            prediction_entry.save()





class PredictionModel :
    def __init__(self,data_manager) :
        model = keras.models.load_model("C:\\Users\\Hamza\\Documents\\__PROJECTS\\gold_prediction\\mysite\\goldpredictionlogic\\goldpredictionlogic\\myModel")
        self.prediction_model = model
        self.data_manager = data_manager
        
    
    def checkModel(self):
        print("[PREDICTIONMODEL] Our working model : " , self.prediction_model)
        print("[PREDICTIONMODEL] Our data : " , self.data_manager.data_DataFrame)


    def prediction_from_model(self,value_list):
        prediction = self.prediction_model.predict(value_list).flatten()
        return prediction[0]

    def get_model_input_X(self,in_list):
        """ to make an adequate prediction input """
        return np.reshape(in_list , (1,WINDOW,1))

    def PredictForNValues(self,Window,n = 100) :
        """ Will start the prediction with a list of the last n°Window of data elements 
            data should be a list/array
        """
        data = np.array(list(self.data_manager.data_DataFrame[0]))
        data = np.reshape(data , (data.shape[0],1))
        print("[PREDICTION] initialised data : ", data)


        L = []
        #initialise with the last Window training values :
        for el in data[-Window:] :
            L.append(el.tolist()[0])

        try :
            assert len(L) == Window
        except :
            print("Wrong list initialisation")
            return
        
        t0 = time.time()
        print(f"[PREDICTION] Start the prediction for {n} values ...")
        for i in range(n):
            new_list_sample = L[-Window:]
            input_X = self.get_model_input_X(new_list_sample)
            scalar_prediction = self.prediction_from_model(input_X)
            L.append(scalar_prediction)
        t1 = time.time()
        elapsed = t1 - t0

        try :
            assert len(L) == Window+n
            print(f"Successfully predicted {n} values ! elapsed time : {elapsed}")

        except :
            print("Wrong list initialisation")
            return 
        
        # Get rid of those first values
        predictionList = L[Window:]
        # To Dataframe & inverse for actual values
        predictions_dataframe = pd.DataFrame(predictionList)
        scaler = self.data_manager.scaler
        predictions_dataframe = scaler.inverse_transform(predictions_dataframe)

        # Update our prediction :
        self.data_manager.updatePredictionDB(predictions_dataframe)


        return predictions_dataframe


class PredictionManager :
    def __init__(self,predictionModel,dateThreshold):
        """ 
        DateThreshold is the threshold where the model shall redo the prediction (expl : after 7 days, 14days...)
        """
        self.predictionModel = predictionModel
        self.dateThreshold = dateThreshold
    
    def doNextNPredictions(self,Window,n = 100):
        #check if the date difference is bigger than self.dateThreshold :
        allObjects = GoldPrice.objects.all()
        l = len(allObjects)
        lastUpdatedDate = allObjects[l-1].date
        daysDifference = (datetime.date.today() - lastUpdatedDate).days

        if daysDifference > self.dateThreshold :
            # update DB
            
            # do new predictions
            self.predictionModel.PredictForNValues(Window,n)
        else :
            print(f"[PREDICTIONMANAGER] the days difference { daysDifference } should be greater than the threshold of { self.dateThreshold }")
        
  

WINDOW = 60
DATE_THRESHOLD = 7
DATA_MANAGER = DataManager()
MODEL = PredictionModel(DATA_MANAGER)
MODEL_MANAGER = PredictionManager(MODEL,DATE_THRESHOLD)




