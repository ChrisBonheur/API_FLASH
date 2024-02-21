from django.contrib import admin
from .models import AcademicYear


class AcademicYearAdmin(admin.ModelAdmin):

    fields = ['year_begin', 'year_end']
    
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            return False
        

admin.site.register(AcademicYear, AcademicYearAdmin)