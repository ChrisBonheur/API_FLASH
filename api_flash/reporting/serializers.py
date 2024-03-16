from rest_framework.serializers import ModelSerializer
from .models import UserDocument
from api_flash.constantes import YEAR_ID_HEADER
from api_flash.utils import get_object_or_raise
from agent.models import Agent
from academic_years.models import AcademicYear

class DocumentSerializer(ModelSerializer):
    class Meta:
        model = UserDocument
        fields = "__all__"
        extra_kwargs = {
            'added_by': {'required': False},
            'last_update_by': {'required': False},
            'year': {'required': False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        if request.method == "GET":
            representation['added_by_label'] = instance.added_by.last_name + " " + instance.added_by.first_name if instance.added_by else ''
            representation['last_update_by_label'] = instance.last_update_by.last_name + " " + instance.last_update_by.first_name if instance.last_update_by else ''

        return representation

    def create(self, validated_data):
        request = self.context['request']
        year_id = request.headers.get(YEAR_ID_HEADER)
        year = get_object_or_raise(AcademicYear, year_id, "Année académique")
        agentConnected = get_object_or_raise(Agent, request.user.id, "Agent")
        validated_data['year'] = year
        validated_data['added_by'] = agentConnected
        validated_data['last_update_by'] = agentConnected
        new_doc = super().create(validated_data)
        return new_doc
    
    def update(self, instance, validated_data):
        request = self.context['request']
        agentConnected = get_object_or_raise(Agent, request.user.id, "Agent")
        validated_data['last_update_by'] = agentConnected
        return super().update(instance, validated_data)