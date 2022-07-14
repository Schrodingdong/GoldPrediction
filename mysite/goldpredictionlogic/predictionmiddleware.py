from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from .prediction import MODEL_MANAGER,DATA_MANAGER,WINDOW

from goldprice.models import GoldPricePredictions
from decimal import Decimal

"""Executes on startup !!"""
class StartupMiddleware(object):
    def __init__(self,get_response):
        MODEL_MANAGER.doNextNPredictions(WINDOW,n=30)
        raise MiddlewareNotUsed('Startup complete')