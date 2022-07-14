from django.urls import path
from . import views


app_name = 'goldpredictionlogic'


urlpatterns = [
    path('predict',views.goldpredictionlogic, name='goldPredictionLogic')
]