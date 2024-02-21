from django.http import JsonResponse
from rest_framework.response import Response
from .constantes import YEAR_ID_HEADER
from api_flash.exceptions import CustomValidationError

class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Récupère la valeur de l'en-tête personnalisé
        custom_header_value = request.headers[YEAR_ID_HEADER]
        if not custom_header_value:
            raise CustomValidationError(detail="Aucune entête trouvée prière de se reconnecter, pour corriger le problème !")
        
        response = self.get_response(request)
        return response
