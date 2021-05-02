from rest_framework.viewsets import ModelViewSet

from .models import Trade
from .serializers import TradeSerializer


class TradeViewSet(ModelViewSet):
    serializer_class = TradeSerializer
    queryset = Trade.objects.all()
