from django.urls import path
from . import views


app_name = 'goldprice'


urlpatterns = [
    path('',views.goldPriceList, name='goldPriceList')
]