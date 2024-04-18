from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from config_global.models import Town, GeneralBacSeries, Parcours, Nivel, ClassRoom
from academic_years.models import AcademicYear
from api_flash.enum import type_inscription


class Student(models.Model):
    SEXE_CHOICES = [
        (1, 'Fille'),
        (2, 'Garçon')
    ]
    user = models.OneToOneField(User, related_name="student", on_delete=models.PROTECT)
    birth_city = models.ForeignKey(Town, verbose_name="Lieu de naissance", related_name="student_birth_city", on_delete=models.PROTECT)
    origin_city = models.ForeignKey(Town, verbose_name="Ville d'origine", related_name="student_origin_city", on_delete=models.PROTECT)
    adress = models.CharField(max_length=255, null=True, blank=True)
    sex = models.SmallIntegerField(choices=SEXE_CHOICES)
    baccalaureat_option = models.ForeignKey(GeneralBacSeries, on_delete=models.PROTECT, related_name='students')
    contact1 = models.CharField(max_length=100)
    contact2 = models.CharField(max_length=100, null=True, blank=True)


class Inscription(models.Model):
    STATUS_CHOICES = [
        (type_inscription.PREINSCRIPTION_INIT.value, 'Préinscription initiale'),
        (type_inscription.PREINSCRIPTION_VALID.value, 'Préinscription validée'),
        (type_inscription.INSCRIPTION_VALID.value, 'Inscription validée'),
        (type_inscription.DISABLE.value, 'Inactif'),
        (type_inscription.RADIATION.value, 'Radiation'),
    ]
    parcours_suggest = models.ManyToManyField(Parcours, verbose_name="Parcours souhaités par l'étudiant", related_name="student_favourites")
    parcours = models.ForeignKey(Parcours, verbose_name="Parcours", on_delete=(models.PROTECT), null=True, blank=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.PROTECT, related_name="inscriptions", verbose_name="Niveau")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, verbose_name="Année académique", related_name="inscriptions")
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="inscriptions", verbose_name="Etudiant")
    class_room = models.ForeignKey(ClassRoom, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Classe")
    created = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    code_folder = models.CharField(max_length=20, null=True, blank=True)

    preinscription_valid_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="preinscriptions_valid", verbose_name="Presinscription validée par", editable=False)
    date_preinscription_valid = models.DateTimeField(null=True, blank=True, editable=False)

    inscription_valid_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="inscriptions_valid", verbose_name="Inscription validée par", editable=False)
    date_inscription_valid = models.DateTimeField(null=True, blank=True, editable=False)

    disabled_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="inscriptions_deactivate", verbose_name="Désactivée par", editable=False)
    date_disabled = models.DateTimeField(null=True, blank=True, editable=False)

    radiation_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="inscriptions_radiation", verbose_name="Radiée par", editable=False)
    date_radiation = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('student', 'academic_year',), name="unique_student_by_year_in_insc")
        ]

    def save(self, *args, **kwargs) -> None:
        super().save(args, kwargs)
        if len(self.student.user.first_name) > 2 and len(self.student.user.last_name) > 2:
            self.code_folder = f"FLASH-{self.student.user.first_name[0:2]}-{self.student.user.last_name[0:2]}-{self.id}"
        self.code_folder = f"FLASH-FOLD-{self.id}"
        super().save(args, kwargs)