from django.contrib import admin
from .models import TypeSource
from api_flash.permissions import SuperUserAdmin


class TypeSoyurceAdmin(SuperUserAdmin):
    pass


admin.site.register(TypeSource, TypeSoyurceAdmin)