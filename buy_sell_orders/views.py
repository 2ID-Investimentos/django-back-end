from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.models import Buy, Sell
from .serializers import BuySerializer, SellSerializer


class UserBuysAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buys = Buy.objects.filter(user=request.user)
        serializer = BuySerializer(buys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSellsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sells = Sell.objects.filter(user=request.user)
        serializer = SellSerializer(sells, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
