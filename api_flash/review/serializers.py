from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from agent.serializers import AgentListSerializer, AgentSerializer
from .models import Review, Volume, Numero, Author, Reference, Article, TypeSource
from agent.models import Agent
from api_flash.utils import get_object_or_raise, gen_matricule, set_each_first_letter_in_upper
from api_flash.exceptions import CustomValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import status
from .models import PageContent


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

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
        if (instance and Volume.objects.exclude(pk=instance.pk).filter(index=index, review=review).exists()) or (not instance and Volume.objects.filter(index=index, review=review).exists()):
            fields.append('numéro du volume')
        if (instance and Volume.objects.exclude(pk=instance.pk).filter(year=year, review=review).exists()) or (not instance and Volume.objects.filter(year=year, review=review).exists()):
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
    authors = UserSerializer(many=True)
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
            article.authors.add(user)

        if nesteed_references:
            for data in nesteed_references:
                reference = Reference.objects.create(**data)
                article.references.add(reference)

        return article


    def update(self, instance, validated_data):
        nesteed_authors = validated_data.pop('authors', None)
        nesteed_references = validated_data.pop('references', None)
        article = super().update(instance, validated_data)
        for data in nesteed_authors:
            users = User.objects.filter(email=data['email'])
            if not users.exists():
                last_id = User.objects.last().id + 1 if User.objects.last() else 1
                data['username'] = gen_matricule(last_id, "AUT", length=1000)
                data['password'] = "1234"
                data['last_name'] = data.pop('last_name').upper()
                data['first_name'] = set_each_first_letter_in_upper(data.pop('first_name'))
                dataAuthor = data.pop('author')
                user = User.objects.create_user(**data)
                dataAuthor['user'] = user
                Author.objects.create(**dataAuthor)
            else:
                user = users[0]
                if hasattr(user, 'auhtor'):
                    dataAuthor = data.pop('author')
                    User.objects.filter(pk=user.id).update(**data)
                    Author.objects.filter(user=user).update(**dataAuthor)
            article.authors.add(user)
        
        #remove not extisting author in new list authors
        emails_in_nesteed = [author['email'] for author in nesteed_authors]

        for email_obj in article.authors.values('email'):
            if not email_obj['email'] in emails_in_nesteed:
                author_to_rmv = User.objects.filter(email=email_obj['email'])
                if author_to_rmv.exists():
                    article.authors.remove(author_to_rmv[0])

        #remove all references
        for reference in article.references.all():
            article.references.remove(reference)
        if nesteed_references:
            for data in nesteed_references:
                reference = Reference.objects.create(**data)
                article.references.add(reference)

        return article
    

class ArticleSerializerList(ModelSerializer):
    authors = UserSerializer(many=True)
    class Meta:
        model = Article
        fields = ('id', 'title_fr', 'date_ajout', 'date_accept', 'date_publication', 'numero', 'state', 'counter_download', 'authors', 'page_begin', 'page_end')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['numero_volume_review_code'] = instance.user.review.code
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
    numero = serializers.IntegerField(required=False, allow_null=True)
    state = serializers.IntegerField(required=False, allow_null=True)
    authors = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageContent
        fields = "__all__"