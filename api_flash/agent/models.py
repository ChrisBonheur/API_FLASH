from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from config_global.models import Town, Country, Box, Speciality, CategoryTeacher, Ladder, Grade, PersonalClass, Echelon
from api_flash.utils import generate_qr_code_with_text, gen_matricule, generate_number, sendemail, set_each_first_letter_in_upper
from academic_years.models import AcademicYear
from rest_framework.response import Response
import asyncio

class Agent(models.Model):
    SEXE_CHOICES = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('autre', 'Autre'),
    ]
    birth_city = models.ForeignKey(Town, on_delete=models.PROTECT, verbose_name="Ville de naissance", related_name="agent_birth_city")
    cityArea = models.CharField(max_length=255, null=True, blank=True)
    adress = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="Nationalité")
    town_residence = models.ForeignKey(Town, on_delete=models.PROTECT, verbose_name="Ville de résidence")
    photo = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name="Dernières mise à jour")
    civility = models.CharField(max_length=10, choices=SEXE_CHOICES, verbose_name="Sexe")
    birth_date = models.DateField(verbose_name="Date de naissance", null=True, blank=True)
    contact = models.CharField(max_length=30)
    qrcode_img = models.TextField(null=True, blank=True)
    box = models.ForeignKey(Box, on_delete=models.PROTECT, verbose_name="Caisse", null=True, blank=True, related_name="agent_caisse")
    quality = models.CharField(max_length=50, null=True, blank=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT, verbose_name="Specialité", null=True, blank=True)
    ladder = models.ForeignKey(Ladder, on_delete=models.PROTECT, verbose_name="Echelle", null=True, blank=True)
    echelon = models.ForeignKey(Echelon, on_delete=models.PROTECT, verbose_name="Echelon", null=True, blank=True)
    category = models.ForeignKey(CategoryTeacher, on_delete=models.PROTECT, verbose_name="Categorie", null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, verbose_name="Grade", null=True, blank=True)
    personal_class = models.ForeignKey(PersonalClass, on_delete=models.PROTECT, verbose_name="Classe Personelle", null=True, blank=True)
    basic_salary = models.FloatField(default=0, verbose_name="Rémunération de base",)
    retained_insurance = models.FloatField(default=0, verbose_name="Retenue Assurance")
    retained_cnss = models.FloatField(default=0, verbose_name="Retenue CNSS")
    retained_social_case = models.FloatField(default=0, verbose_name="Retenue Cas Social")
    retained_other = models.FloatField(default=0, verbose_name="Autre retenue")
    monthly_indaminitis = models.FloatField(default=0, verbose_name="Indaminité mensuel")
    Detained_dependent_child = models.FloatField(default=0, verbose_name="Retenue Enfant Charge")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Ajouté par", related_name="agent_creating")
    last_modified_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Dernière modif par", related_name="last_modifier")
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="agent")
    institution = models.CharField(max_length=255, null=True, blank=True, default="Marien Ngouabi")
    about = models.CharField(max_length=255, null=True, blank=True)
    function = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        self.user.last_name = self.user.last_name.upper()
        self.user.first_name = set_each_first_letter_in_upper(self.user.first_name)
        if not self.id:
            password = f"{generate_number(5)}"
            self.password = password
            super(Agent, self).save(*args, **kwargs)
            matricule = gen_matricule(self.id, "FLASH", length=1000)
            self.qrcode_img = generate_qr_code_with_text(self.id, self.user.username)
            asyncio.run(sendemail("Mot de passe", f"Information de connexion FLASH-APPLICATION \nlogin: {matricule}\nMot de passe: {password}", [self.user.email]))
        else:
            if not self.qrcode_img:
                self.qrcode_img = generate_qr_code_with_text(self.id, self.user.username)
            super(Agent, self).save(*args, **kwargs)

    
    def __str__(self) -> str:
        return self.user.last_name + " " + self.user.first_name
    
