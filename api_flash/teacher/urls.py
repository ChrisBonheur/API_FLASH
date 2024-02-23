from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from .views import TeacherViewsSet, TeacherCustomTokenObtainPairView

router = routers.SimpleRouter()

router.register('', TeacherViewsSet, basename='teacher')

urlpatterns = [
    path('token/', TeacherCustomTokenObtainPairView.as_view(), name='token_obtain_pair_teacher'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_teacher'),
    path('', include(router.urls)),
]
