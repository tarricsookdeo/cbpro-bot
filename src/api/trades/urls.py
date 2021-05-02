from rest_framework import routers

from .views import TradeViewSet

router = routers.SimpleRouter()
router.register(r'trades', TradeViewSet)
urlpatterns = router.urls
