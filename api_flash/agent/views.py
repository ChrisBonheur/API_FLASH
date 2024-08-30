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
from django.contrib.auth import authenticate, login as lg
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
import asyncio
from api_flash.enum import type_user
from .data import roles
from django.contrib.auth.models import Group

class AgentViewsSet(ModelViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action in ['retrieve', 'create', 'update']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer = AgentListSerializer
        if self.action in ['retrieve', 'create', 'update']:
            serializer = AgentSerializer
        return serializer
    
    def get_object(self):
        year_id = self.request.headers.get(YEAR_ID_HEADER)
        year_academic = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
        obj = super().get_object()
        if obj in self.get_queryset():
            return obj
        raise CustomValidationError(f"Cet enseignant n'est pas disponible dans  l'année academique '{YEAR_ID_HEADER}'.")
    
    def get_queryset(self):
        year_id = self.request.headers.get(YEAR_ID_HEADER)
        if year_id:
            year_academic = get_object_or_raise(AcademicYear, year_id, "ANNEE ACADEMIQUE")
            queryset = Agent.objects.filter(user__years=year_academic, user__is_active=True)
            return queryset
        else:
            raise ValidationError({'detail': f"Veuillez specifier une année academique '{YEAR_ID_HEADER}' dans les entêtes."})

    @action(detail=False, methods=['GET'])
    def for_all_any_years(self, request): #get all author for auggest author
        agents = Agent.objects.all()
        serializer = AgentListSerializer(agents, context={'request': request}, many=True)
        return Response(serializer.data)

        
class CustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            # Gérer l'exception ici
            return Response({"detail": "Information de connexion non valide !"}, status=status.HTTP_400_BAD_REQUEST)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data['username'])
            found_agent = Agent.objects.filter(user=user)
            
            if found_agent.exists():
                agent = found_agent[0]
                serializer = AgentSerializer(agent, context={"request": request})
                response.data['user'] = serializer.data
                try:
                    response.data['review'] = agent.user.review.id
                except Exception as e:
                    response.data['review'] = 0

                otp = generate_number(6)
                response.data['OTP'] = otp
                response.data['academic_years'] = AcademicSerializer(agent.user.years, many=True).data
                
                currentRoleOfUser = list(user.groups.values_list('name', flat=True))
                if agent.user.years.count() > 0 or roles[0] in currentRoleOfUser or roles[1] in currentRoleOfUser:
                    asyncio.run(sendemail("TOKEN", f"Connexion sur la plateforme FLASH-APPLICATION,\nVotre token d'authenfication est {otp}", [agent.user.email]))
                    print(otp)
            else:
                raise CustomValidationError("Information de connexion non valide !", 400)
        return response

#async def sendmailasync():



class ReviewTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            # Gérer l'exception ici
            return Response({"detail": "Information de connexion non valide !"}, status=status.HTTP_400_BAD_REQUEST)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data['username'])
            user_chosed = request.data.get('type_user')
            found_agent = Agent.objects.filter(user=user)
            if found_agent.exists() and  user.groups.filter(name='auteur').exists():
                agent = found_agent[0]
                serializer = AgentSerializer(agent, context={"request": request})
                response.data['user'] = serializer.data
                try:
                    response.data['review'] = agent.user.review.id
                except Exception as e:
                    response.data['review'] = 0
            else:
                raise CustomValidationError("Cet utilisateur ne fait pas parti du groupe des auteurs des revues de la FLASH !", 400)
        return response


@csrf_exempt
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_chosed = request.POST.get('type_user')
    user = authenticate(request, username=username, password=password)
    agent = Agent.objects.filter(user=user)

    if user and (int(user_chosed) == type_user.AGENT.value) and agent.exists() and user.is_active:
        lg(request, user)
        return redirect('/flashadministration/')  
    return HttpResponse("Vous n'êtes pas habilité à consulter cette page. Prière de se rapprocher du SSE/FLASH pour en savoir d'avantage. Merci!")
