from django.db import models
from .order import Order
from .beverage import Beverage

class OrderBeverage(models.Model):
    order_id= models.ForeignKey(Order, on_delete=models.CASCADE)
    beverage_id = models.ForeignKey(Beverage, on_delete=models.CASCADE, default=1)