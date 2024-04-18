from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, routers
from agent.views import login

schema_view = get_schema_view(
    openapi.Info(
        title="FLASH API",
        default_version='v1',
        description="api For review",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="bonheurmafoundou@gmail.com"),
        license=openapi.License(name=""),
    ),
    public=True,
)

router = routers.SimpleRouter()


urlpatterns = [
    path('flashadministration/', admin.site.urls),
    path('redirect-to-admin/', login),
    path('agent/', include('agent.urls')),
    path('review/', include('review.urls')),
    path('settings/', include('config_global.urls')),
    path('reporting/', include('reporting.urls')),
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
