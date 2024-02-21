from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import AcademicYear
from.serializers import DocumentSerializer
from .models import AgentDocument
from api_flash.constantes import YEAR_ID_HEADER
from api_flash.utils import get_object_or_raise
from api_flash.exceptions import CustomValidationError
from rest_framework.response import Response


class DocumentsViewSet(ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year_id = self.request.headers.get(YEAR_ID_HEADER)
        if year_id:
            year_academic = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
            queryset = year_academic.agent_documents.all()
            return queryset
        else:
            raise CustomValidationError(f"Veuillez specifier une année academique '{YEAR_ID_HEADER}' dans les entêtes.", 400)
        
    @action(detail=True, methods=['GET'], url_path='for_agent', url_name='documents_for_agent')
    def for_agent(self, request, pk=None):
        query = AgentDocument.objects.filter(agent__id=pk)
        serializer = DocumentSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)
    