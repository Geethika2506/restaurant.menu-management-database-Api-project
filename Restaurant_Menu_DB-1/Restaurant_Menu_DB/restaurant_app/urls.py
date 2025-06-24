from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)

urlpatterns = router.urls