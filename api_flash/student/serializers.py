from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import Inscription, Student
from api_flash.utils import get_object_or_raise, gen_matricule, generate_number
from api_flash.constantes import YEAR_ID_HEADER
from academic_years.models import AcademicYear
from api_flash.enum import type_inscription
from api_flash.exceptions import CustomValidationError


class InscriptionSerializer(ModelSerializer):
    baccalaureat_option = serializers.CharField(source='student.baccalaureat_option')
    origin_city = serializers.CharField(source='student.origin_city')
    birth_city = serializers.CharField(source='student.birth_city')
    sex = serializers.CharField(source='student.sex')
    contact1 = serializers.CharField(source='student.contact1')
    adress = serializers.CharField(source='student.adress')
    contact2 = serializers.CharField(source='student.contact2', required=False,  allow_blank=True, allow_null=True)
    email = serializers.CharField(source='student.user.email', required=False,  allow_blank=True, allow_null=True)
    last_name = serializers.CharField(source='student.user.last_name')
    first_name = serializers.CharField(source='student.user.first_name')

    class Meta:
        model = Inscription
        fields = "__all__"

        extra_kwargs = {
            'academic_year': {'required': False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        if request.method == "GET":
            representation['first_name'] = instance.student.user.first_name if instance.student else ''
            representation['last_name'] = instance.student.user.last_name if instance.student else ''
            representation['parcours_label'] = instance.parcours.label if instance.parcours else ''
            representation['nivel_label'] = instance.nivel.label if instance.nivel else ''
            representation['class_room_label'] = instance.class_room.label if instance.class_room else ''

        return representation

    def create(self, validated_data):
        request = self.context['request']
        year_id = request.headers.get(YEAR_ID_HEADER)
        if year_id:
            year = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
        else:
            try:
                year = AcademicYear.objects.get(is_completed=True)
            except Exception as e:
                return CustomValidationError(detail="Aucune année académique active trouvée!", code=404)
            
        find_inscription = Inscription.objects.filter(academic_year=year, student__contact1=validated_data['contact1'])
        
        if find_inscription.exists():
            user = find_inscription[0].student.user
            #verif if already inscription valid
            if find_inscription[0].status == type_inscription.INSCRIPTION_VALID.value:
                return CustomValidationError(f"Ce numéro de téléphone est déjà utilisé par {user.last_name} {user.first_name} avec une inscription valide en {find_inscription[0].nivel.label} {find_inscription[0].parcours.label}", code=455)
            
            if find_inscription[0].status == type_inscription.PREINSCRIPTION_VALID.value:
                return CustomValidationError(f"Ce numéro de téléphone est déjà utilisé par {user.last_name} {user.first_name} avec une préinscription valide en attente de l'inscription définitive. Prière de passer au secretariat pour en savoir plus sur l'état de d'avancement de votre dossier.", code=456)
            
            if find_inscription[0].status == type_inscription.PREINSCRIPTION_INIT.value:
                return CustomValidationError(f"Ce numéro de téléphone est déjà utilisé par {user.last_name} {user.first_name} avec une préinscription en attente d'acceptation. Vous pouvez toutes fois modifier votre dossier.", code=457)
        
        validated_data['academic_year'] = year
        validated_data['status'] = type_inscription.PREINSCRIPTION_INIT.value
        last_student = Student.objects.last()
        last_id = last_student.id + 1 if last_student else 1
        password = generate_number(6)
        validated_data['student']['user']['username'] = gen_matricule(last_id, "EDT")
        validated_data['student']['user']['password'] = password
        return super().create(validated_data)


class ValidInscriptionSerializer(Serializer):
    parcours = serializers.IntegerField()
    class_room = serializers.IntegerField()
