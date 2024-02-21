from rest_framework.viewsets import ModelViewSet
from .serializers import AgentSerializer, AgentListSerializer
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from rest_framework.permissions import DjangoModelPermissions
from django.http import HttpResponseForbidden
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from api_flash.utils import get_object_or_raise, generate_number
from .models import Agent
from api_flash.utils import sendemail
from api_flash.enum import type_user
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from academic_years.models import AcademicYear
from academic_years.serializers import AcademicSerializer
from api_flash.constantes import YEAR_ID_HEADER
from api_flash.exceptions import CustomValidationError
from django.http import HttpResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as lg
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


class AgentViewsSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        serializer = AgentListSerializer
        if self.action in ['retrieve', 'create', 'update']:
            serializer = AgentSerializer
        return serializer
    
    def get_queryset(self):
        year_id = self.request.headers.get(YEAR_ID_HEADER)
        if year_id:
            year_academic = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
            queryset = year_academic.agents.all()
            return queryset
        else:
            raise ValidationError({'details': f"Veuillez specifier une année academique '{YEAR_ID_HEADER}' dans les entêtes."})


class CustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            # Gérer l'exception ici
            return Response({"details": "Information de connexion non valide !"}, status=status.HTTP_400_BAD_REQUEST)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data['username'])
            user_chosed = request.data.get('type_user')

            if user_chosed and user_chosed == type_user.AGENT.value:
                agent = get_object_or_raise(Agent, user.id, "Agent")
                serializer = AgentSerializer(agent, context={"request": request})
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
    

@csrf_exempt
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_chosed = request.POST.get('type_user')
    user = authenticate(request, username=username, password=password)
    agent = Agent.objects.filter(username=username)

    if user and (int(user_chosed) == type_user.AGENT.value) and agent.exists() and agent[0].is_active:
        lg(request, agent[0])
        return redirect('/flashadministration/')  
    return HttpResponse("Vous n'êtes pas habilité à consulter cette page. Prière de se rapprocher du SSE/FLASH pour en savoir d'avantage. Merci!")
