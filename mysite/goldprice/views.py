from django.shortcuts import render
from .models import GoldPrice,GoldPricePredictions


# Create your views here.
def goldPriceList(request):
    prices = GoldPrice.objects.all()
    predictedPrices = GoldPricePredictions.objects.all()
    #calculate the growth :
    

    l = len(prices)
    prices = prices[l-100:]
    return render(  request, 
                    'goldprice/index.html',
                    {
                        'prices' : prices,
                        'predictedPrices' : predictedPrices,
                    })
