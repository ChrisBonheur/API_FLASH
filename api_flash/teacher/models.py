from django.db import models
from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from config_global.models import Town, Country, Box, Speciality, CategoryTeacher, Ladder, Grade, PersonalClass, Echelon
from api_flash.utils import generate_qr_code_with_text, gen_matricule, generate_number, sendemail, set_each_first_letter_in_upper


class Teacher(models.Model):
    SEXE_CHOICES = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('autre', 'Autre'),
    ]
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="teacher", null=True, blank=True)
    birth_city = models.ForeignKey(Town, on_delete=models.PROTECT, verbose_name="Ville de naissance", related_name="teacher_birth_city")
    cityArea = models.CharField(max_length=255, null=True, blank=True)
    adress = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="Nationalité")
    town_residence = models.ForeignKey(Town, on_delete=models.PROTECT, verbose_name="Ville de résidence")
    photo = models.TextField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name="Dernières mise à jour")
    civility = models.CharField(max_length=10, choices=SEXE_CHOICES, verbose_name="Sexe")
    birth_date = models.DateField(verbose_name="Date de naissance")
    contact = models.CharField(max_length=30)
    qrcode_img = models.TextField(null=True, blank=True)
    quality = models.CharField(max_length=50, null=True, blank=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT, verbose_name="Specialité", null=True, blank=True)
    ladder = models.ForeignKey(Ladder, on_delete=models.PROTECT, verbose_name="Echelle", null=True, blank=True)
    echelon = models.ForeignKey(Echelon, on_delete=models.PROTECT, verbose_name="Echelon", null=True, blank=True)
    category = models.ForeignKey(CategoryTeacher, on_delete=models.PROTECT, verbose_name="Categorie", null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, verbose_name="Grade", null=True, blank=True)
    personal_class = models.ForeignKey(PersonalClass, on_delete=models.PROTECT, verbose_name="Classe Personelle", null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Ajouté par", related_name="agent_creating")
    last_modified_by = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Dernière modif par", related_name="last_modifier")


    def save(self, *args, **kwargs) -> None:
        if not self.id:
            super(Teacher, self).save(*args, **kwargs)
            self.qrcode_img = generate_qr_code_with_text(self.id, "")
        else:
            if not self.qrcode_img:
                self.qrcode_img = generate_qr_code_with_text(self.id, '')
            super(Teacher, self).save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.last_name + " " + self.first_name
    
    """
    def __create_user(*args, **kwargs):
        for k, v in kwargs.items():
            if k in ["username", "last_name", "first_name", "email", "password"]"""
