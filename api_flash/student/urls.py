from rest_framework import routers
from django.urls import path, include
from .views import InscriptionViewSet

router = routers.SimpleRouter()

router.register("inscription", InscriptionViewSet, basename="inscription")

urlpatterns = [
    path('', include(router.urls))
]
