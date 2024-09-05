"""dranksforyou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from dranksforyouapi.views.auth import check_user, register_user
from dranksforyouapi.views.user_view import UserView
from dranksforyouapi.views.orders import OrderView
from dranksforyouapi.views.beverages import BeverageView
from dranksforyouapi.views.liquors import LiquorView
from dranksforyouapi.views.ingredients import IngredientView
from dranksforyouapi.views.order_beverages import OrderBeverageView
from dranksforyouapi.views.ingredient_beverages import IngredientBeverageView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'orders', OrderView, 'order')
router.register(r'beverages', BeverageView, 'beverage')
router.register(r'liquors', LiquorView, 'liquor')
router.register(r'ingredients', IngredientView, 'ingredient')
router.register(r'orderbeverages', OrderBeverageView, 'orderbeverage')
router.register(r'ingredientbeverages', IngredientBeverageView, 'ingredientbeverage')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('checkuser', check_user),
]
