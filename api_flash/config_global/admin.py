from django.contrib import admin
from .models import Departement, Town, Country, CategoryTeacher, Speciality, Echelon, Ladder, Grade, PersonalClass, Box, ChartOfAccount, Bundle, Branch, Nivel, ClassRoom

class GlobalControl(admin.ModelAdmin):
    search_fields = ['code', 'label']

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            return False

class DepartementAdmin(GlobalControl):
    list_filter = ('country',)
    ordering = ('ordering',)


class TownAdmin(GlobalControl):
    list_filter = ('country',)
    ordering = ('label',)


class CountryAdmin(GlobalControl):
    ordering = ('label',)


class CategoryTeacherAdmin(GlobalControl):
    ordering = ('label',)


class CategoryTeacherAdmin(GlobalControl):
    ordering = ('label',)


class SpecialityAdmin(GlobalControl):
    ordering = ('label',)


class EchelonAdmin(GlobalControl):
    ordering = ('label',)


class LadderAdmin(GlobalControl):
    ordering = ('label',)


class GradeAdmin(GlobalControl):
    ordering = ('label',)


class PersonalClassAdmin(GlobalControl):
    ordering = ('label',)

class BoxAdmin(GlobalControl):
    pass

class ChartOfAccountAdmin(GlobalControl):
    ordering = ('clase_number', )
    

class BundleAdmin(GlobalControl):
    pass


class NivelAdmin(GlobalControl):
    ordering = ('order',)


class BrancheAdmin(GlobalControl):
    ordering = ('order',)

class ClassRoomAdmin(GlobalControl):
    ordering = ('order',)


admin.site.register(Departement, DepartementAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(CategoryTeacher, CategoryTeacherAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Echelon, EchelonAdmin)
admin.site.register(Ladder, LadderAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(PersonalClass, PersonalClassAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(ChartOfAccount, ChartOfAccountAdmin)
admin.site.register(Bundle, BundleAdmin)
admin.site.register(Branch, BrancheAdmin)
admin.site.register(Nivel, NivelAdmin)
admin.site.register(ClassRoom, ClassRoomAdmin)

