from rest_framework.viewsets import ModelViewSet
from .serializers import TeacherSerializer
from .models import Teacher
from rest_framework.permissions import IsAuthenticated
from academic_years.models import AcademicYear
from api_flash.constantes import YEAR_ID_HEADER
from api_flash.utils import get_object_or_raise
from api_flash.exceptions import CustomValidationError


class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] =  self.request
        return context
    

    def get_object(self):
        obj = super().get_object()
        if obj in self.get_queryset():
            return obj
        raise CustomValidationError(f"Cet enseignant n'est pas disponible dans  l'année academique '{YEAR_ID_HEADER}'.")

    def get_queryset(self):
        year_id = self.request.headers.get(YEAR_ID_HEADER)
        if year_id:
            year_academic = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
            queryset = Teacher.objects.filter(user__years=year_academic, user__is_active=True)
            return queryset
        else:
            raise CustomValidationError(f"Veuillez specifier une année academique '{YEAR_ID_HEADER}' dans les entêtes.")
        