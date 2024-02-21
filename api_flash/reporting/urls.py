from rest_framework import routers
from django.urls import path, include
from .views import DocumentsViewSet

router = routers.SimpleRouter()

router.register("documents", DocumentsViewSet, basename="documents")

urlpatterns = [
    path('', include(router.urls))
]
