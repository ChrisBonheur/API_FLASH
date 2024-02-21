from rest_framework.viewsets import ModelViewSet
from .serializers import DepartementSerializer, LadderSerializer, EchelonSerializer, CategoryTeacherSerializer, TownSerializer, CountrySerializer, GradeSerializer, PersonalClassSerializer, SpecialitySerializer, GroupSerializer, BoxSerializer
from config_global.models import Departement, Town, Country, CategoryTeacher, Speciality, Echelon, Ladder, Grade, PersonalClass, Box
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated
from api_flash.constantes import YEAR_ID_HEADER
from api_flash.utils import get_object_or_raise
from academic_years.models import AcademicYear
from api_flash.exceptions import CustomValidationError



class DepartementViewSet(ModelViewSet):
    serializer_class = DepartementSerializer
    queryset = Departement.objects.all()
    permission_classes = [IsAuthenticated]


class LadderViewSet(ModelViewSet):
    serializer_class = LadderSerializer
    queryset = Ladder.objects.all()
    permission_classes = [IsAuthenticated]


class EchelomViewSet(ModelViewSet):
    serializer_class = EchelonSerializer
    queryset = Echelon.objects.all()
    permission_classes = [IsAuthenticated]


class CategoryTeacherViewSet(ModelViewSet):
    serializer_class = CategoryTeacherSerializer
    queryset = CategoryTeacher.objects.all()
    permission_classes = [IsAuthenticated]


class TownViewSet(ModelViewSet):
    serializer_class = TownSerializer
    queryset = Town.objects.all()
    permission_classes = [IsAuthenticated]


class CountryViewSet(ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = [IsAuthenticated]


class SpecialityViewSet(ModelViewSet):
    serializer_class = SpecialitySerializer
    queryset = Speciality.objects.all()
    permission_classes = [IsAuthenticated]


class GradeViewSet(ModelViewSet):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    permission_classes = [IsAuthenticated]


class PersonalClassViewSet(ModelViewSet):
    serializer_class = PersonalClassSerializer
    queryset = PersonalClass.objects.all()
    permission_classes = [IsAuthenticated]


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]


class BoxViewSet(ModelViewSet):
    serializer_class = BoxSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        year_id = self.request.headers.get(YEAR_ID_HEADER)
        if year_id:
            year_academic = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
            queryset = year_academic.box_year.all()
            return queryset
        else:
            raise CustomValidationError(f"Veuillez specifier une année academique '{YEAR_ID_HEADER}' dans les entêtes.", 400)