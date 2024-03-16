from rest_framework import routers
from django.urls import path, include
from .views import TeacherViewSet

router = routers.SimpleRouter()

router.register("", TeacherViewSet, basename="teacher")

urlpatterns = [
    path('', include(router.urls))
]
