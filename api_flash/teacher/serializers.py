from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Teacher
from django.contrib.auth.models import User
from api_flash.utils import get_object_or_raise, set_each_first_letter_in_upper, gen_matricule, generate_number, sendemail
from api_flash.constantes import YEAR_ID_HEADER
from academic_years.models import AcademicYear
from api_flash.exceptions import CustomValidationError


class TeacherSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username', allow_null=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_active = serializers.BooleanField(source='user.is_active', default=True)

    class Meta:
        model = Teacher
        fields = "__all__"
        extra_kwargs = {
            'user': {'required': False},
        }

    def get_field_names(self, declared_fields, info):
        field_names = super().get_field_names(declared_fields, info)

        if self.context['request'].method in ["POST", "PUT"]:
            fields_to_exclude = ['academic_years']  # Liste des champs à exclure
            return [field for field in field_names if field not in fields_to_exclude]
        return field_names
    
    def create(self, validated_data):
        request = self.context['request']
        #create user before
        password = f"{generate_number(5)}"
        id = User.objects.last().id + 1 if User.objects.last() else 1 
        matricule = gen_matricule(id, "ENS", length=1000)
        validated_data['user']['username'] = matricule
        validated_data['user']['password'] = password
        validated_data['user']['last_name'] = validated_data['user']['last_name'].upper()
        validated_data['user']['first_name'] = set_each_first_letter_in_upper(validated_data['user']['first_name'])
        user = User.objects.create_user(**validated_data['user'])
        validated_data['user'] = user

        new_teacher = super().create(validated_data)
        year_id = request.headers.get(YEAR_ID_HEADER)
        year = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
        year.users.add(user)
        try:
            sendemail("Mot de passe", f"Information de connexion FLASH-APPLICATION \nlogin: {matricule}\nMot de passe: {password}", [user.email])
        except Exception:
            return CustomValidationError({'detail': "L'email n'a pas été envoyé prière de contacter l'administrateur"}, status=400)
        return new_teacher

    def update(self, instance, validated_data):
        validated_data['user']['last_name'] = validated_data['user']['last_name'].upper()
        validated_data['user']['first_name'] = set_each_first_letter_in_upper(validated_data['user']['first_name'])
        User.objects.filter(pk=instance.user.id).update(**validated_data['user'])
        validated_data['user'] = User.objects.get(pk=instance.user.id)
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


    def validate_email(self, value):
        request = self.context['request']
        teacherList = Teacher.objects.filter(user__email=value)
        if teacherList.exists():
            teacher_exist = teacherList[0]
            if request.method == "POST" or (request.method == "PUT" and teacher_exist.id != int(request.data['id'])):
                #verif if agent exist is in current year
                custom_header_value = request.headers[YEAR_ID_HEADER]
                active_year = get_object_or_raise(AcademicYear, custom_header_value, "ANNEE ACADEMIQUE")
                code = 0
                msg_sup = ""
                if teacher_exist.user in active_year.users.all():
                    code = 409
                elif teacher_exist.user.years.count() > 0:
                    code = 452
                    msg_sup = f" dans l'année {teacher_exist.user.years.all()[0].year_name}"
                else:
                    code = 453
                    
                raise CustomValidationError(detail=f"Attention cet email est déjà utilisé par l'agent {teacher_exist.user.last_name} {teacher_exist.user.first_name} {msg_sup}", code=code)
        return value
    