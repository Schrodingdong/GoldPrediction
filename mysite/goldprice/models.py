from django.db import models
import pandas as pd


# Create your models here.
class GoldPrice(models.Model):
    date = models.DateField()
    open = models.DecimalField(max_digits= 15,decimal_places = 4)
    high = models.DecimalField(max_digits= 15,decimal_places = 4)
    low = models.DecimalField(max_digits= 15,decimal_places = 4)
    close = models.DecimalField(max_digits= 15,decimal_places = 4)
    growth = models.DecimalField(max_digits= 15,decimal_places = 4, default=0)
    volume = models.IntegerField()
    currency = models.CharField(max_length=6)

    objects = models.Manager()

    def getField(self,field):
        if field == 'date' :
            return self.date
        elif field == 'open' :
            return self.open
        elif field == 'high' :
            return self.high
        elif field == 'low' :
            return self.low
        elif field == 'close' :
            return self.close
        elif field == 'growth' :
            return self.growth
        elif field == 'volume' :
            return self.volume
        elif field == 'currency' :
            return self.currency




    @staticmethod
    def resetAllData():
        data = GoldPrice.objects.all()
        data.delete()

    @staticmethod
    def initData(csvPath):
        #reset data :
        if input("do you want to erase and rewrite data ? y/n") == 'n':
            return
        GoldPrice.resetAllData()
        # read data :
        csv = pd.read_csv(csvPath)
        # initialise with iterations :
        print("Started Initialising Data ...")
        old_element = None
        for index,element in csv.iterrows() :
            if index == 0 :
                old_element = element
                continue

            new_entry = GoldPrice(  date = element.Date,
                                    open = element.Open,
                                    high = element.High,
                                    low = element.Low,
                                    close = element.Close,
                                    growth = ((element.Close - old_element.Close) / old_element.Close)*100,
                                    volume = element.Volume,
                                    currency = element.Currency)
            old_element = element
            # Save each entry :
            new_entry.save()
        print("Finished Data Init")

    @staticmethod
    def addData(newEntryList) :
        """ newEntryList should be in a list format\n
        ---
        If its elements are of type list
        should be in the following order :\n
        \t[ Date, Open, High, Low, Close, Volume, Currency]
        """
        l = len(GoldPrice.objects.all())
        old_element = GoldPrice.objects.all()[l-1]
        if newEntryList[0] == GoldPrice :
            for element in newEntryList :
                new_entry = GoldPrice(  date = element.Date,
                                        open = element.open,
                                        high = element.high,
                                        low = element.low,
                                        close = element.close,
                                        growth = ((element.close - old_element.close) / old_element.close)*100,
                                        volume = element.volume,
                                        currency = element.currency)
                new_entry.save()
        elif newEntryList[0] == list :
            for element in newEntryList :
                new_entry = GoldPrice(  date = element[0],
                                        open = element[1],
                                        high = element[2],
                                        low = element[3],
                                        close = element[4],
                                        volume = element[5],
                                        growth = (element[5] - old_element.close) / old_element,
                                        currency = element[6])
                new_entry.save()
        print("finished updating !")

    # @staticmethod
    # def updateData(date, **kwargs):
    #     """update the data with the specified *date*
    #         the fields : ['date','open','high','low','close','volume','currency']
    #     """
    #     selectedData = GoldPrice.objects.filter(date = date)
    #     fields = ['date','open','high','low','close','volume','currency']
    #     # field verification
    #     for k,v in kwargs.items :
    #         k = k.lower()
    #         if k not in fields :
    #             print(f"[FIELD_ERROR] wrong specified field {k}\nTry Specifying one or more of these fields : {fields}")
    #             return
    #         if k == 'date' :
    #             selectedData.date = v
    #         elif k == 'open' :
    #             selectedData.open = v
    #         elif k == 'high' :
    #             selectedData.high = v
    #         elif k == 'low' :
    #             selectedData.low = v
    #         elif k == 'close' :
    #             selectedData.close = v
    #         elif k == 'volume' :
    #             selectedData.volume = v
    #         elif k == 'currency' :
    #             selectedData.currency = v

    #     selectedData.save()
    #     return



    def __str__(self):
        return f"{self.date} : {self.close} {self.currency}"



class GoldPricePredictions(models.Model):
    """ Has only the 'date' && 'close' && 'currency' fields ! """
    date = models.DateField()
    close = models.DecimalField(max_digits= 15,decimal_places = 4)
    growth = models.DecimalField(max_digits= 15,decimal_places = 4)
    currency = models.CharField(max_length=6)

    @staticmethod
    def resetAllData():
        data = GoldPricePredictions.objects.all()
        data.delete()