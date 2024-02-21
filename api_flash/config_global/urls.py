from django.urls import path, include
from rest_framework import routers
#from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()

router.register('category-teacher', CategoryTeacherViewSet, basename='category-teacher')
router.register('departement', DepartementViewSet, basename='departement')
router.register('ladder', LadderViewSet, basename='ladder')
router.register('echelon', EchelomViewSet, basename='echelon')
router.register('town', TownViewSet, basename='town')
router.register('country', CountryViewSet, basename='country')
router.register('speciality', SpecialityViewSet, basename='speciality')
router.register('grade', GradeViewSet, basename='grade')
router.register('personal_class', PersonalClassViewSet, basename='personal-class')
router.register('group', GroupViewSet, basename='group')
router.register('box', BoxViewSet, basename='box')


urlpatterns = [
    #path('token/', CustomTokenObtnain.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]