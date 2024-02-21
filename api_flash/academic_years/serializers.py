from rest_framework.serializers import ModelSerializer
from .models import AcademicYear


class AcademicSerializer(ModelSerializer):
    class Meta:
        model=AcademicYear
        fields = "__all__"