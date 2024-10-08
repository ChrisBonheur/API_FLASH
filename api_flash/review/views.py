from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import (ReviewSerializer, VolumeSerializer, NumeroSerialzer, NumeroCreateUpdateSerializer,
                          NumeroRetrieveSerializer, ArticleSerializer, ArticleSerializerList, TypeSourceSerializer,
                          FilterArticleSerializer, PageSerializer, PageListSerializer, VolumeNumeroSerializer,
                          ReviewListSerializer, AuthorSerializer)
from rest_framework.permissions import IsAuthenticated
from api_flash.permissions import IsInGroupAuthorsPermission, FalsePermissionAlways, IsAuthorOrReadOnly
from rest_framework.decorators import action
from django.contrib.auth.models import User
from api_flash.enum import state_article
from api_flash.utils import get_object_or_raise
from api_flash.exceptions import CustomValidationError
from rest_framework import status
from .models import Review, Volume, Numero, Article, TypeSource, PageContent, Author
from rest_framework.response import Response
from agent.models import Agent
from .permissions import IsOwnerPAgeOrReadOnly, IsOwnerReviewOrReadOnly, IsOwnerNumeroOrReadOnly, IsOwnerVolumOrReadOnly
from rest_framework import exceptions
from django.core.cache import cache
from api_flash.cache_prefix import cache_review_one


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(is_active=True)
    

    def retrieve(self, request, *args, **kwargs):
        review_id = self.kwargs.get('pk')
        
        try:
            cache_name = cache_review_one(review_id)
            if cache.get(cache_name):
                data = cache.get(cache_name)
            else:
                obj = Review.objects.get(id=review_id)
                serializer = ReviewSerializer(obj)
                data = serializer.data
                cache.set(cache_name, data)
                
        except Review.DoesNotExist:
            raise exceptions.NotFound("L'objet demandé est introuvable.")

        # Vérifie les permissions
        #self.check_object_permissions(self.request, obj)

        # Retourne la réponse avec les données sérialisées
        serializer = ReviewSerializer(Review.objects.get(id=review_id))
        return Response(serializer.data)


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'destroy', 'retrieve']:
            return ReviewSerializer
        return ReviewListSerializer

    def get_permissions(self):
        permissions = [IsOwnerReviewOrReadOnly]
        if self.action in ['create', 'update', 'destroy']:
            permissions.append(IsInGroupAuthorsPermission)
        return [permission() for permission in permissions]

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def get_for_current_user(self, request):
        user = request.user
        try:
            cache_name = cache_review_one(user.review.id)
            if cache.get(cache_name):
                obj = cache.get(cache_name)
            else:
                serializer = ReviewSerializer(user.review, context={'request': request})
                cache.set(cache_name, serializer.data)
                obj = cache.get(cache_name)
            serializer = ReviewSerializer(user.review, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            raise CustomValidationError("Vous n'avez pas encore crée une revue disponible", status.HTTP_204_NO_CONTENT)



class VolumeViewSet(ModelViewSet):
    serializer_class = VolumeSerializer
    queryset = Volume.objects.all()

    def get_permissions(self):
        permissions = [IsOwnerVolumOrReadOnly]
        if self.action in ['create', 'update', 'destroy']:
            permissions.append(IsAuthenticated)
        return [permission() for permission in permissions]

    @action(detail=True, methods=['GET'])
    def get_by_review(self, request, pk=None):
        review = get_object_or_raise(Review, pk=pk, data_name="Revue")
        serializer = VolumeSerializer(review.volumes.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def get_by_review_with_numeros(self, request, pk=None):
        review = get_object_or_raise(Review, pk=pk, data_name="Revue")
        volumes = review.volumes.all()
        serializer = VolumeNumeroSerializer(volumes, many=True)
        return Response(serializer.data)
        

class NumeroViewSet(ModelViewSet):
    queryset = Numero.objects.all()

    def get_permissions(self):
        permissions = [IsOwnerNumeroOrReadOnly]
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

    def get_object(self):
        article = super().get_object()
        article.counter_download += 1
        article.save()
        return article

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
        review = None
        if request.data.get('review'):
            review = request.data.pop('review')
            review = get_object_or_raise(Review, review, 'Revue')
        serializer = FilterArticleSerializer(data=request.data)
        if serializer.is_valid():
            articles = Article.objects.filter(**request.data)
            if review:
                articles = articles.filter(user=review.author)
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
    
    @action(detail=True, methods=['GET'], serializer_class=ArticleSerializerList, permission_classes=[IsAuthorOrReadOnly])
    def get_most_view_by_review(self, request, pk):
        articles = Article.objects.filter(numero__volume__review__id=pk).order_by('-counter_download')[:10]
        serializer = ArticleSerializerList(articles, many=True)
        return Response(serializer.data)


class TypeSourceViewset(ReadOnlyModelViewSet):
    serializer_class = TypeSourceSerializer
    queryset = TypeSource.objects.all()


class PagesViewSet(ModelViewSet):
    queryset = PageContent.objects.all()
    permission_classes = [IsOwnerPAgeOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'retrieve']:
            return PageSerializer
        return PageListSerializer

    @action(detail=True, methods=['GET'])
    def get_by_review(self, request, pk):
        review = get_object_or_raise(Review, pk=pk, data_name="Revue")
        pages = review.pages.all()
        serializer = PageListSerializer(pages, many=True)
        return Response(serializer.data)
    
    
class AuthorViewset(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    
    @action(detail=True, methods=['GET'])
    def get_author_by_email(self, request, pk):
        author = get_object_or_raise(Author, pk=pk, data_name="Auteur")
        serializer = AuthorSerializer(author, many=True)
        return Response(serializer.data)
    
    