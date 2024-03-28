from rest_framework.permissions import BasePermission
from django.contrib import admin

class IsInGroupAuthorsPermission(BasePermission):
    def has_permission(self, request, view):
        # Vérifiez si l'utilisateur est connecté
        if not request.user.is_authenticated:
            return False
        
        # Vérifiez si l'utilisateur fait partie du groupe souhaité
        return request.user.groups.filter(name='auteur').exists()
    

class IsAuthorOrReadOnly(BasePermission):
    """
    Permission personnalisée pour autoriser seulement l'auteur de l'article à modifier ou supprimer l'article.
    """
    def has_object_permission(self, request, view, obj):
        # Vérifie si la méthode de la requête est sécurisée (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return hasattr(obj, 'user') and obj.user == request.user


class FalsePermissionAlways(BasePermission):
    def has_permission(self, request, view):
        return False
    

class SuperUserAdmin(admin.ModelAdmin):
    search_fields = ['code', 'label']

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            return False