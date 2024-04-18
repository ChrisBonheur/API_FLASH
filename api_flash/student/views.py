from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import InscriptionSerializer, ValidInscriptionSerializer
from api_flash.constantes import YEAR_ID_HEADER
from academic_years.models import AcademicYear
from api_flash.utils import get_object_or_raise
from rest_framework.decorators import action
from .models import Inscription
from api_flash.enum import type_inscription
from datetime import datetime


class InscriptionViewSet(ModelViewSet):
    serializer_class = InscriptionSerializer

    def get_permissions(self):
        return super().get_permissions()

    def get_queryset(self):
        year_id = self.request.headers.get(YEAR_ID_HEADER)
        year = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
        status = self.request.GET.get('status')
        if status:
            return year.inscriptions.filter(status=status)
        return year.inscriptions.all()

    @action(detail=True, methods=["GET"])
    def validate_preinscription(self, request, pk=None):
        inscription = get_object_or_raise(Inscription, pk=pk, data_name="Inscription")
        inscription.status = type_inscription.PREINSCRIPTION_VALID.value
        inscription.preinscription_valid_by = request.user
        inscription.date_inscription_valid = datetime.now()
        inscription.save()
        return inscription
    
    validate_preinscription.permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=["POST"], serializer_class=ValidInscriptionSerializer)
    def validate_inscription(self, request, pk=None):
        serializer = ValidInscriptionSerializer(request.data)
        if serializer.is_valid():
            inscription = get_object_or_raise(Inscription, pk=pk, data_name="Inscription")
            inscription.status = type_inscription.INSCRIPTION_VALID.value
            inscription.inscription_valid_by = request.user
            inscription.date_inscription_valid = datetime.now()
            inscription.parcours = serializer.data['parcours']
            inscription.class_room = serializer.data['class_room']
            inscription.save()
            return inscription
        return serializer.errors()
    
    validate_inscription.permission_class=[IsAuthenticated]
    
    @action(detail=True, methods=["GET"])
    def radiation(self, request, pk=None):
        inscription = get_object_or_raise(Inscription, pk=pk, data_name="Inscription")
        inscription.status = type_inscription.RADIATION.value
        inscription.radiation_by = request.user
        inscription.date_radiation = datetime.now()
        inscription.save()
        return inscription
    
    radiation.permission_class=[IsAuthenticated]
    
    @action(detail=True, methods=["GET"])
    def deactivate(self, request, pk=None):
        inscription = get_object_or_raise(Inscription, pk=pk, data_name="Inscription")
        inscription.status = type_inscription.DISABLE.value
        inscription.disabled_by = request.user
        inscription.date_disabled = datetime.now()
        inscription.save()
        return inscription

    deactivate.permnission_class = [IsAuthenticated]
