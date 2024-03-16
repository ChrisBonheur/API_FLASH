from django.contrib import admin
from .models import Agent

class GlobalControl(admin.ModelAdmin):
    pass

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            return False
        

class AgentAdmin(GlobalControl):
    pass


admin.site.register(Agent, AgentAdmin)