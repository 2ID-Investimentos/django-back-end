from rest_framework import serializers
from core.models import Buy, Sell


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = "__all__"


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = "__all__"
