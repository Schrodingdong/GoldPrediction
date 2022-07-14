from django.contrib import admin
from .models import GoldPrice,GoldPricePredictions

# Register your models here.
@admin.register(GoldPrice)
class GoldpriceAdmin(admin.ModelAdmin):
    list_display = ('date','open','high','low','close','growth','volume','currency')

# Register your models here.
@admin.register(GoldPricePredictions)
class GoldpriceAdmin(admin.ModelAdmin):
    list_display = ('date','close','growth','currency')