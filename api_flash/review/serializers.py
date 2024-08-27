from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from agent.serializers import AgentListSerializer, AgentSerializer
from .models import Review, Volume, Numero, Author, Reference, Article, TypeSource
from api_flash.utils import get_object_or_raise, gen_matricule, set_each_first_letter_in_upper
from api_flash.exceptions import CustomValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import status
from .models import PageContent
import json


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ["adress", "contact", "civility", "function", "institution", "about", "photo", 'email', 'last_name', 'first_name']

class UserSerializer(ModelSerializer):
    contact = serializers.CharField(source='author.contact', required=False,  allow_blank=True, allow_null=True)
    civility = serializers.CharField(source='author.civility', required=False, allow_blank=True, allow_null=True)
    about = serializers.CharField(source='author.about', required=False, allow_blank=True, allow_null=True)
    institution = serializers.CharField(source='author.institution', required=False, allow_null=True,  allow_blank=True)
    photo = serializers.CharField(source='author.photo', required=False, allow_null=True, allow_blank=True)
    adress = serializers.CharField(source='author.adress', required=False, allow_null=True, allow_blank=True)
    id = serializers.IntegerField(source='author.id', required=False, allow_null=True)
    username = serializers.CharField(source='author.id', required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(source='author.id', required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = "__all__"

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('request') and self.context['request'].method == "GET": 
            representation['civility'] = instance.agent.civility if hasattr(instance, 'agent') else instance.teacher.civility if hasattr(instance, 'teacher') else instance.author.civility if hasattr(instance, 'author') else ''

            representation['adress'] = instance.agent.adress if hasattr(instance, 'agent') else instance.teacher.adress if hasattr(instance, 'teacher') else instance.author.adress if hasattr(instance, 'author') else ''

            representation['contact'] = instance.agent.contact if hasattr(instance, 'agent') else instance.teacher.contact if hasattr(instance, 'teacher') else instance.author.contact if hasattr(instance, 'author') else ''

            representation['institution'] = instance.agent.institution if hasattr(instance, 'agent') else instance.teacher.institution if hasattr(instance, 'teacher') else instance.author.institution if hasattr(instance, 'author') else ''

            representation['function'] = instance.agent.function if hasattr(instance, 'agent') else instance.teacher.function if hasattr(instance, 'teacher') else instance.author.function if hasattr(instance, 'author') else ''

            representation['about'] = instance.agent.about if hasattr(instance, 'agent') else instance.teacher.about if hasattr(instance, 'teacher') else instance.author.about if hasattr(instance, 'author') else ''

            representation['photo'] = instance.agent.photo if hasattr(instance, 'agent') else instance.teacher.photo if hasattr(instance, 'teacher') else instance.author.photo if hasattr(instance, 'author') else ''

        return representation
    

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        extra_kwargs = {
            'author': {'required': False},
        }
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('request') and self.context['request'].method == "GET": 
            representation['author_label'] = instance.author.first_name + " " + instance.author.last_name
        return representation
    
class ReviewListSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "title"]

class VolumeSerializer(ModelSerializer):
    class Meta:
        model = Volume
        fields = "__all__"

        
    def validate(self, data):
        instance = self.instance
        index = data.get('index')
        year = data.get('year')
        review = data.get('review')
        fields = []
        if (instance and Volume.objects.exclude(pk=instance.pk).filter(index=index, review=review).exists()) or\
                (not instance and Volume.objects.filter(index=index, review=review).exists()):
            fields.append('numéro du volume')
        if (instance and Volume.objects.exclude(pk=instance.pk).filter(year=year, review=review).exists()) or \
                (not instance and Volume.objects.filter(year=year, review=review).exists()):
            fields.append('année du volume')

        if len(fields) > 0:
            field_names = ', '.join(fields)
            error_message = f"Une donnée avec les champs uniques suivants existe déjà: {field_names}."
            raise CustomValidationError(error_message, status.HTTP_400_BAD_REQUEST)
        return data
        

class NumeroSerialzer(ModelSerializer):

    class Meta:
        model = Numero
        fields = "__all__"

class NumeroRetrieveSerializer(ModelSerializer):
    sommaire_authors = UserSerializer(many=True)
    class Meta:
        model = Numero
        fields = "__all__"

class NumeroCreateUpdateSerializer(ModelSerializer):
    sommaire_authors = UserSerializer(many=True)

    class Meta:
        model = Numero
        fields = "__all__"

    def validate(self, data):
        instance = self.instance
        index = data.get('index')
        volume = data.get('volume')
        fields = []
        if (instance and Numero.objects.exclude(pk=instance.pk).filter(volume=volume, index=index).exists()) or (not instance and Numero.objects.filter(volume=volume, index=index).exists()):
            fields.append('numéro du volume')
            fields.append('numéro')

        if len(fields) > 0:
            field_names = ', '.join(fields)
            error_message = f"Une donnée avec les champs uniques suivants existe déjà: {field_names}."
            raise CustomValidationError(error_message, status.HTTP_400_BAD_REQUEST)
        return data

    def create(self, validated_data):
        nesteed_authors = validated_data.pop('sommaire_authors', None)
        
        numero = Numero.objects.create(**validated_data)
        for data in nesteed_authors:
            users = User.objects.filter(email=data.pop('email'))
            if not users.exists():
                last_id = Author.objects.last().id + 1 if Author.objects.last() else 1
                data['username'] = gen_matricule(last_id, "AUT", length=1000)
                data['password'] = "1234"
                data['last_name'] = data.pop('last_name').upper()
                data['first_name'] = set_each_first_letter_in_upper(data.pop('first_name'))
                dataAuthor = data.pop('author')
                user = User.objects.create_user(**data['user'])
                data['user'] = user
                Author.objects.create(**dataAuthor)
            else:
                user = users[0]
            numero.sommaire_authors.add(user)

        return numero


    def update(self, instance, validated_data):
        nesteed_authors = validated_data.pop('sommaire_authors', None)
        numero = super().update(instance, validated_data)
        users_author = []
        for data in nesteed_authors:
            users = User.objects.filter(email=data['email'])
            if not users.exists():
                last_id = Author.objects.last().id + 1 if Author.objects.last() else 1
                data['username'] = gen_matricule(last_id, "AUT", length=1000)
                data['password'] = "1234"
                data['last_name'] = data.pop('last_name').upper()
                data['first_name'] = set_each_first_letter_in_upper(data.pop('first_name'))
                dataAuthor = data.pop('author')
                user = User.objects.create_user(**data)
                data['user'] = user
                Author.objects.create(**dataAuthor)
            else:
                user = users[0]
                if hasattr(user, 'auhtor'):
                    dataAuthor = data.pop('author')
                    User.objects.filter(pk=user.id).update(**data)
                    Author.objects.filter(user=user).update(**dataAuthor)
            users_author.append(user)
        if len(users_author) > 0:
            numero.sommaire_authors.set(users_author)
        else:
            [numero.sommaire_authors.remove(user) for user in numero.sommaire_authors.all()]
        return numero

class NumeroListSerializer(ModelSerializer):
    class Meta:
        model = Numero
        fields = ('id', 'label', 'index')   

class ReferenceSerializer(ModelSerializer):
    class Meta:
        model = Reference
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('request') and self.context['request'].method == "GET": 
            representation['type_source_name'] = instance.type_source.name
        return representation

class ArticleSerializer(ModelSerializer):
    authors = AuthorSerializer(many=True)
    references = ReferenceSerializer(many=True)
    class Meta:
        model = Article
        fields = "__all__"
        extra_kwargs = {
            'user': {'required': False},
        }
    
    def create(self, validated_data):
        nesteed_authors = validated_data.pop('authors', None)
        nesteed_references = validated_data.pop('references', None)
        validated_data['user'] = self.context['request'].user
        article = Article.objects.create(**validated_data)
        authors = []
        for data in nesteed_authors:
            user = User.objects.filter(email=data['email'])
            if (not user.exists()):
                user = User.objects.create(email=data['email'], password="1234", username=data['email'])
            else:
                user = user[0]
            data['user'] = user
            author, created = Author.objects.get_or_create(**data)
            if created:
                authors.append(author)
        article.authors.set(authors)

        if nesteed_references:
            references = []
            for data in nesteed_references:
                reference = Reference.objects.create(**data)
                references.append(reference)
            article.references.set(references)
            
        return article


    def update(self, instance, validated_data):
        nesteed_authors = validated_data.pop('authors', None)
        nesteed_references = validated_data.pop('references', None)
        article = super().update(instance, validated_data)
        authors_created  = []
        for data in nesteed_authors:
            users = User.objects.filter(email=data['email'])
            if users.exists():
                data['user'] = users[0]
                if not hasattr(User, 'author'):
                    author = Author.objects.create(**data)
                else:
                    author = Author.objects.filter(user=users[0]).update(**data)
            else:
                user = User.objects.create(email=data['email'], password="1234", username=data['email'])
                data['user'] = user
                author = Author.objects.filter(user=users[0]).update(**data)

            authors_created.append(author)
                      
        article.authors.set(authors_created)
        article.save()
    

        #remove all references
        for reference in article.references.all():
            article.references.remove(reference)
        if nesteed_references:
            for data in nesteed_references:
                reference = Reference.objects.create(**data)
                article.references.add(reference)

        return article
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['numero_volume_review_code'] = instance.user.review.code
        data['numero_volume_review_id'] = instance.user.review.id
        data['numero_volume_review_name'] = instance.user.review.title
        data['numero_volume_review_issn'] = instance.user.review.issn
        data['numero_volume_review_logo'] = instance.user.review.logo
        data['user_first_name'] = instance.user.first_name
        data['user_last_name'] = instance.user.last_name
        #import pdb;pdb.set_trace()
        #data['authors'] =  
        if hasattr(instance.user, "author") or hasattr(instance.user, "agent"):
            data['user_institution'] = instance.user.author.institution if hasattr(instance.user, "author") else instance.user.agent.institution 
        if instance.numero:
            data['numero_index'] = instance.numero.index
            data['numero_volume_index'] = instance.numero.volume.index
        if instance.page_begin and instance.page_end:
            data['interval_page'] = f"{instance.page_begin}-{instance.page_end}"
        return data


class ArticleSerializerList(ModelSerializer):
    authors_labels = serializers.ListSerializer(child=UserSerializer(), source='authors')
    class Meta:
        model = Article
        fields = ('id', 'title_fr','state', 'counter_download', 'page_begin', 'page_end', 'authors_labels')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['numero_volume_review_code'] = instance.user.review.code
        data['numero_volume_review_id'] = instance.user.review.id
        data['numero_volume_review_name'] = instance.user.review.title
        data['numero_volume_review_logo'] = instance.user.review.logo
        data['user_first_name'] = instance.user.first_name
        data['user_last_name'] = instance.user.last_name
        
        author = Author.objects.filter(user__id=instance.user.id)
        
        if author.exists():
            data['user_institution'] = author[0].institution
        if instance.numero:
            data['numero_index'] = instance.numero.index
            data['numero_volume_index'] = instance.numero.volume.index
        if instance.page_begin and instance.page_end:
            data['interval_page'] = f"{instance.page_begin}-{instance.page_end}"
        return data
    

class TypeSourceSerializer(ModelSerializer):
    class Meta:
        model = TypeSource
        fields = "__all__"


class FilterArticleSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=False, allow_null=True)
    review = serializers.IntegerField(required=False, allow_null=True)
    numero = serializers.IntegerField(required=False, allow_null=True)
    state = serializers.IntegerField(required=False, allow_null=True)
    authors = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageContent
        fields = "__all__"
        extra_kwargs = {
            'review': {'required': False},
        }

    def validate(self, data):
        instance = self.instance
        order = data.get('order')
        review = data.get('review')
        fields = []
        if (instance and PageContent.objects.exclude(pk=instance.pk).filter(review=review, order=order).exists()) or (not instance and PageContent.objects.filter(review=review, order=order).exists()):
            fields.append('ordre d\'affichage')
            fields.append('revue')

        if len(fields) > 0:
            field_names = ', '.join(fields)
            error_message = f"Une donnée avec les champs uniques suivants existe déjà: {field_names}."
            raise CustomValidationError(error_message, status.HTTP_400_BAD_REQUEST)
        return data
    
    def to_internal_value(self, data):
            internal_value = super().to_internal_value(data)
            internal_value['review'] = self.context['request'].user.review

            return internal_value


class PageListSerializer(ModelSerializer):
    class Meta:
        model = PageContent
        exclude = ('content', 'pdf_file')


class VolumeNumeroSerializer(ModelSerializer):
    numeros = NumeroListSerializer(many=True)

    class Meta:
        model = Volume
        fields = ("id", "index", "date_created", "year", "numeros")
