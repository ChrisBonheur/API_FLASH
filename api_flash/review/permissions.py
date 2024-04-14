from rest_framework.permissions import BasePermission

class IsOwnerPAgeOrReadOnly(BasePermission):
    """
    Permission personnalisée pour autoriser seulement l'auteur de la page à modifier ou supprimer.
    """
    def has_object_permission(self, request, view, obj):
        # Vérifie si la méthode de la requête est sécurisée (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return hasattr(obj, 'review') and obj.review.author == request.user
    

class IsOwnerReviewOrReadOnly(BasePermission):
    """
    Permission personnalisée pour autoriser seulement l'auteur de revue à modifier ou supprimer.
    """
    def has_object_permission(self, request, view, obj):
        # Vérifie si la méthode de la requête est sécurisée (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return hasattr(obj, 'author') and obj.author == request.user


class IsOwnerNumeroOrReadOnly(BasePermission):
    """
    Permission personnalisée pour autoriser seulement l'auteur du Numero à modifier ou supprimer.
    """
    def has_object_permission(self, request, view, obj):
        # Vérifie si la méthode de la requête est sécurisée (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return hasattr(obj, 'volume') and obj.volume.review.author == request.user
    

class IsOwnerVolumOrReadOnly(BasePermission):
    """
    Permission personnalisée pour autoriser seulement l'auteur du Numero à modifier ou supprimer.
    """
    def has_object_permission(self, request, view, obj):
        # Vérifie si la méthode de la requête est sécurisée (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return hasattr(obj, 'review') and obj.review.author == request.user