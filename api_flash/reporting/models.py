from django.db import models
from agent.models import Agent
from academic_years.models import AcademicYear

class AgentDocument(models.Model):
    title = models.CharField(max_length=250, verbose_name="Titre")
    description = models.CharField(max_length=250, null=True, blank=True)
    content = models.TextField()
    agent = models.ForeignKey(Agent, related_name="documents", on_delete=models.CASCADE)
    added_by = models.ForeignKey(Agent, related_name="documents_added_by", verbose_name="Ajouté par", on_delete=models.PROTECT)
    date_save = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")
    last_update_by = models.ForeignKey(Agent, related_name="documents_last_update_by", verbose_name="Dernière modification par", on_delete=models.PROTECT)
    last_update_date = models.DateTimeField(auto_now=True, editable=False, verbose_name="Dernière modification date")
    year = models.ForeignKey(AcademicYear, verbose_name="Année académique", related_name="agent_documents", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Document"

    def __str__(self) -> str:
        return self.title