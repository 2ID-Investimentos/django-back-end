from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.models import Buy, Sell, Stock
from .serializers import StockSerializer


class UserStocksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buy_stocks = Stock.objects.filter(buy__user=request.user)
        sell_stocks = Stock.objects.filter(sell__user=request.user)
        stocks = buy_stocks.union(sell_stocks)

        serializer = StockSerializer(stocks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
