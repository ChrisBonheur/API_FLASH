from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import ReviewSerializer, VolumeSerializer, NumeroSerialzer, NumeroCreateUpdateSerializer, NumeroRetrieveSerializer, ArticleSerializer, ArticleSerializerList, TypeSourceSerializer, FilterArticleSerializer
from rest_framework.permissions import IsAuthenticated
from api_flash.permissions import IsInGroupAuthorsPermission, FalsePermissionAlways, IsAuthorOrReadOnly
from rest_framework.decorators import action
from django.contrib.auth.models import User
from api_flash.enum import state_article
from api_flash.utils import get_object_or_raise
from api_flash.exceptions import CustomValidationError
from rest_framework import status
from .models import Review, Volume, Numero, Article, TypeSource
from rest_framework.response import Response
from agent.models import Agent


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_permissions(self):
        permissions = [IsAuthorOrReadOnly]
        if self.action in ['create', 'update', 'destroy']:
            permissions.append(IsInGroupAuthorsPermission)
        return [permission() for permission in permissions]

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def get_for_current_user(self, request):
        user = request.user
        try:
            serializer = ReviewSerializer(user.review, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            raise CustomValidationError("Vous n'avez pas encore crée une revue disponible", status.HTTP_204_NO_CONTENT)
        else:
            return reviews


class VolumeViewSet(ModelViewSet):
    serializer_class = VolumeSerializer
    queryset = Volume.objects.all()

    def get_permissions(self):
        permissions = [IsAuthorOrReadOnly]
        if self.action in ['create', 'update', 'destroy']:
            permissions.append(IsAuthenticated)
        return [permission() for permission in permissions]

    @action(detail=True, methods=['GET'])
    def get_by_review(self, request, pk=None):
        review = get_object_or_raise(Review, pk=pk, data_name="Revue")
        serializer = VolumeSerializer(review.volumes.all(), many=True)
        return Response(serializer.data)
        

class NumeroViewSet(ModelViewSet):
    queryset = Numero.objects.all()

    def get_permissions(self):
        permissions = [IsAuthorOrReadOnly]
        if self.action in ['create', 'update', 'destroy']:
            permissions.append(IsAuthenticated)
        return [permission() for permission in permissions]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return NumeroCreateUpdateSerializer
        elif self.action in ['retrieve']:
            return NumeroRetrieveSerializer
        return NumeroSerialzer
    
    @action(detail=True, methods=["GET"])
    def get_by_volume(self, request, pk=None):
        volume = get_object_or_raise(Volume, pk=pk, data_name="Volume")
        serializer = NumeroSerialzer(volume.numeros.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def get_by_review(self, request, pk=None):
        review = get_object_or_raise(Review, pk=pk, data_name="Revue")
        numeros = Numero.objects.filter(volume__review=review)
        serializer = NumeroSerialzer(numeros, many=True)
        return Response(serializer.data)
    
        

class ArticleViewset(ModelViewSet):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'retrieve']:
            return ArticleSerializer
        return ArticleSerializerList

    def get_permissions(self):
        permissions = [IsAuthorOrReadOnly]
        if self.action in ['create', 'update', 'destroy']:
            permissions.append(IsAuthenticated)
        return [permission() for permission in permissions]

    @action(detail=True, methods=['GET'])
    def get_by_numero(self, request, pk=None):
        numero = get_object_or_raise(Numero, pk=pk, data_name="Numéro")
        articles = numero.articles.all()
        serializer = ArticleSerializerList(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def get_for_logged_user(self, request, pk=None):
        user = request.user
        if pk and int(pk) > 0:
            #if just init case, getAll with state INIT
            articles = user.articles_owner.filter(state=pk)
        else:
            articles = user.articles_owner.all()
        serializer = ArticleSerializerList(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'], serializer_class=FilterArticleSerializer)
    def filter(self, request):
        serializer = FilterArticleSerializer(data=request.data)
        if serializer.is_valid():   
            articles = Article.objects.filter(**serializer.data)
        else:
            articles = []
        serializer = ArticleSerializerList(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'], serializer_class=ArticleSerializer, permission_classes=[IsAuthorOrReadOnly])
    def valid_for_parrution(self, request, pk):
        article = get_object_or_raise(Article, pk=pk, data_name="Article")
        article.state = state_article.PARRUTION.value
        article.save()
        serializer = ArticleSerializer(article)
        return Response(serializer.data)



class TypeSourceViewset(ReadOnlyModelViewSet):
    serializer_class = TypeSourceSerializer
    queryset = TypeSource.objects.all()