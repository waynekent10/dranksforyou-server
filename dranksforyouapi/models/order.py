from django.db import models
from .user import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_total = models.CharField(max_length=200)
    payment_type = models.CharField(max_length=50)
