from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from .models import Agent
from api_flash.utils import gen_matricule, generate_number, get_object_or_raise
from api_flash.constantes import YEAR_ID_HEADER
from academic_years.models import AcademicYear
from rest_framework.response import Response
from api_flash.exceptions import CustomValidationError
from rest_framework import status
from django.contrib.auth.models import Group


class AgentSerializer(ModelSerializer):

    class Meta:
        model = Agent
        fields = "__all__"
    

    def get_field_names(self, declared_fields, info):
        field_names = super().get_field_names(declared_fields, info)

        if self.context['request'].method in ["POST", "PUT"]:
            fields_to_exclude = ['username', 'academic_years', 'password', 'date_joined', "is_staff", "is_superuser"]  # Liste des champs à exclure
            return [field for field in field_names if field not in fields_to_exclude]
        return field_names
    
    def validate_email(self, value):
        request = self.context['request']
        agentList = Agent.objects.filter(email=value)
        if agentList.exists():
            agent_exist = agentList[0]
            if request.method == "POST" or (request.method == "PUT" and agent_exist.id != int(request.data['id'])):
                #verif if agent exist is in current year
                custom_header_value = request.headers[YEAR_ID_HEADER]
                active_year = get_object_or_raise(AcademicYear, custom_header_value, "ANNEE ACADEMIQUE")
                code = 0
                msg_sup = ""
                if agent_exist in active_year.agents.all():
                    code = 409
                elif agent_exist.academic_years.count() > 0:
                    code = 452
                    msg_sup = f" dans l'année {agent_exist.academic_years.all()[0].year_name}"
                else:
                    code = 453
                    
                raise CustomValidationError(detail=f"Attention cet email est déjà utilisé par l'agent {agent_exist.last_name} {agent_exist.first_name} {msg_sup}", code=code)
        return value
    
    def create(self, validated_data):
        request = self.context['request']
        last_id = Agent.objects.last().id + 1 if Agent.objects.last() else 1
        matricule = gen_matricule(last_id, "FLASH", length=1000)
        agentConnected = Agent.objects.get(pk=request.user.id)
        validated_data['username'] = matricule
        validated_data['created_by'] = agentConnected
        validated_data['last_modified_by'] = agentConnected
        validated_data['password'] = "1234"
        new_agent = super().create(validated_data)

        #Add new user in current year connected
        year_id = request.headers.get(YEAR_ID_HEADER)
        year = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
        year.agents.add(new_agent)
        return new_agent
    
    def update(self, instance, validated_data):
        request = self.context['request']
        agentConnected = Agent.objects.get(pk=request.user.id)
        validated_data['last_modified_by'] = agentConnected
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        if request.method == "GET":
            representation['town_residence_label'] = instance.town_residence.label if instance.town_residence else ''
            representation['country_label'] = instance.town_residence.country.label if instance.town_residence else ''
            representation['country'] = instance.town_residence.country.id if instance.town_residence else ''
            representation['country_birth'] = instance.town_residence.country.id if instance.town_residence else ''
            representation['country_birth_label'] = instance.town_residence.country.label if instance.town_residence else ''
            representation['birth_city_label'] = instance.birth_city.label if instance.birth_city else ''
            representation['nationality_label'] = instance.nationality.nationality_label if instance.nationality else ''
            representation['speciality_label'] = instance.speciality.label if instance.speciality else ''
            representation['ladder_label'] = instance.ladder.label if instance.ladder else ''
            representation['echelon_label'] = instance.echelon.label if instance.echelon else ''
            representation['category_label'] = instance.category.label if instance.category else ''
            representation['grade_label'] = instance.grade.label if instance.grade else ''
            representation['personal_class_label'] = instance.personal_class.label if instance.personal_class else ''
            representation['last_modified_by_label'] = instance.last_modified_by.last_name + " " + instance.last_modified_by.first_name if instance.last_modified_by else ''
            representation['created_by_label'] = instance.created_by.last_name + " " + instance.created_by.first_name if instance.created_by else ''

        return representation



class AgentListSerializer(ModelSerializer):
    class Meta:
        model = Agent
        fields = ["id", "username", "last_name", "first_name", "civility", "contact", "is_active", "adress", "cityArea", "email"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        if request.method == "GET":
            representation['town_residence_label'] = instance.town_residence.label
            representation['country_label'] = instance.town_residence.country.label
            representation['birth_city_label'] = instance.birth_city.label

        return representation