from django.contrib import admin
from .models import Agent

class GlobalControl(admin.ModelAdmin):
    search_fields = ['code', 'label']

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            return False
        

class AgentAdmin(GlobalControl):
    exclude = ('last_login', 'date_joined', 'qrcode_img', 'matricule', 'user_permissions', 'password', "username")


admin.site.register(Agent, AgentAdmin)