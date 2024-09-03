from django.urls import path

from .views import UserBuysAPIView, UserSellsAPIView

urlpatterns = [
    path("buys/", UserBuysAPIView.as_view(), name="buys"),
    path("sells/", UserSellsAPIView.as_view(), name="sells"),
]
