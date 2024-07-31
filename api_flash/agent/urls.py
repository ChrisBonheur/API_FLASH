from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from .views import AgentViewsSet, CustomTokenObtainPairView, ReviewTokenObtainPairView

router = routers.SimpleRouter()

router.register('', AgentViewsSet, basename='agent')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('author-login/', ReviewTokenObtainPairView.as_view(), name='author_login'),
    path('', include(router.urls)),
]


