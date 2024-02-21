from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Group
from config_global.models import Departement, Town, Country, CategoryTeacher, Speciality, Echelon, Ladder, Grade, PersonalClass, Box

class DepartementSerializer(ModelSerializer):
    class Meta:
        model = Departement
        fields = "__all__"


class TownSerializer(ModelSerializer):
    class Meta:
        model = Town
        fields = "__all__"


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CategoryTeacherSerializer(ModelSerializer):
    class Meta:
        model = CategoryTeacher
        fields = "__all__"


class SpecialitySerializer(ModelSerializer):
    class Meta:
        model = Speciality
        fields = "__all__"


class EchelonSerializer(ModelSerializer):
    class Meta:
        model = Echelon
        fields = "__all__"


class LadderSerializer(ModelSerializer):
    class Meta:
        model = Ladder
        fields = "__all__"


class GradeSerializer(ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"


class PersonalClassSerializer(ModelSerializer):
    class Meta:
        model = PersonalClass
        fields = "__all__"


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class BoxSerializer(ModelSerializer):
    class Meta:
        model = Box
        fields = ["id", "code", "label"]

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        if request.method == "GET":
            representation['chart_of_account_label'] = instance.chart_of_account.label if instance.chart_of_account else ''
            representation['chart_of_account_code'] = instance.chart_of_account.code if instance.chart_of_account else ''
        return representation