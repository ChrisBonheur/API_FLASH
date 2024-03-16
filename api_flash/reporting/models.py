from django.db import models
from agent.models import Agent
from academic_years.models import AcademicYear
from django.contrib.auth.models import User
from api_flash.enum import type_user

class UserDocument(models.Model):
    TYPE_USER = [
        (type_user.AGENT.value, type_user.AGENT.name),
        (type_user.ENSEIGNANT.value, type_user.ENSEIGNANT.name),
        (type_user.ETUDIANT.value, type_user.ETUDIANT.name),
    ]
    title = models.CharField(max_length=250, verbose_name="Titre")
    description = models.CharField(max_length=250, null=True, blank=True)
    content = models.TextField()
    user = models.ForeignKey(User, related_name="documents", on_delete=models.CASCADE)
    type_user = models.SmallIntegerField(choices=TYPE_USER)
    added_by = models.ForeignKey(User, related_name="documents_added_by", verbose_name="Ajouté par", on_delete=models.PROTECT)
    date_save = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")
    last_update_by = models.ForeignKey(User, related_name="documents_last_update_by", verbose_name="Dernière modification par", on_delete=models.PROTECT)
    last_update_date = models.DateTimeField(auto_now=True, editable=False, verbose_name="Dernière modification date")
    year = models.ForeignKey(AcademicYear, verbose_name="Année académique", related_name="documents", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Document"

    def __str__(self) -> str:
        return self.title