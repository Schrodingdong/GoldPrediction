from django.shortcuts import HttpResponse, render
from . import prediction

# Create your views here.
def goldpredictionlogic(request):
    #init the model
    model = prediction.initModel
    #init data
    data = prediction.initData()
    x,y = prediction.createDataset(prediction.WINDOW, data)
    print(data)
    print(x)
    print(y)
    return HttpResponse(x)
    #make prediction
    n = 100
    n_values_prediction = prediction.PredictForNValues(prediction.WINDOW,model,)
    #return