from rest_framework import routers
from django.urls import path, include
from .views import ReviewViewSet, VolumeViewSet, NumeroViewSet, ArticleViewset, TypeSourceViewset, PagesViewSet, AuthorViewset

router = routers.SimpleRouter()

router.register("presentation", ReviewViewSet, basename="review")
router.register("authors", AuthorViewset, basename="authors")
router.register("volumes", VolumeViewSet, basename="volume")
router.register("numeros", NumeroViewSet, basename="numero")
router.register("type-source", TypeSourceViewset, basename="type_source")
router.register("articles", ArticleViewset, basename="articles")
router.register("pages", PagesViewSet, basename="pages")

urlpatterns = [
    path('', include(router.urls))
]
