from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import TeacherSerializer, TeacherListSerializer
from api_flash.constantes import YEAR_ID_HEADER
from api_flash.utils import get_object_or_raise, generate_number
from academic_years.serializers import AcademicSerializer
from academic_years.models import AcademicYear
from api_flash.exceptions import CustomValidationError
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth.models import User
from api_flash.enum import type_user
from .models import Teacher

class TeacherViewsSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        serializer = TeacherListSerializer
        if self.action in ['retrieve', 'create', 'update']:
            serializer = TeacherSerializer
        return serializer
    
    def get_queryset(self):
        year_id = self.request.headers.get(YEAR_ID_HEADER)
        import pdb;pdb.set_trace()
        if year_id:
            year_academic = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
            queryset = year_academic.teachers.all()
            return queryset
        else:
            raise CustomValidationError("Veuillez specifier une année academique '{YEAR_ID_HEADER}' dans les entêtes.", status.HTTP_400_BAD_REQUEST)


class TeacherCustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            # Gérer l'exception ici
            raise CustomValidationError("Information de connexion non valide !", status=status.HTTP_400_BAD_REQUEST)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data['username'])
            user_chosed = request.data.get('type_user')

            if user_chosed and user_chosed == type_user.ENSEIGNANT.value:
                agent = get_object_or_raise(Teacher, user.id, "ENSEIGNANT")
                serializer = TeacherSerializer(agent, context={"request": request})
                response.data['user'] = serializer.data
                otp = generate_number(6)
                response.data['OTP'] = otp
                response.data['academic_years'] = AcademicSerializer(agent.academic_years, many=True).data
                if agent.academic_years.count() > 0:
                    try:
                        #sendemail("TOKEN", f"Connexion sur la plateforme FLASH-APPLICATION,\nVotre token d'authenfication est {otp}", [agent.email])
                        print(otp)
                    except Exception as e:
                        raise CustomValidationError(f"{e}", 400)
            else:
                raise CustomValidationError("Information de connexion non valide !", 400)
        return response
    