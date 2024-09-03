from django.urls import path

from .views import UserStocksAPIView

urlpatterns = [
    path("stocks/", UserStocksAPIView.as_view(), name="stocks"),
]
