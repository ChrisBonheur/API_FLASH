from django.db import models
from academic_years.models import AcademicYear


class IdentifiantGlobal(models.Model):
    code = models.CharField(max_length=10, verbose_name="Code", unique=True)
    label = models.CharField(max_length=50, verbose_name="Nom", unique=True)
    class Meta:
        abstract=True

    def __str__(self) -> str:
        return self.label
    

class Identifiant(IdentifiantGlobal):
    ordering = models.PositiveSmallIntegerField(unique=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    class Meta:
        abstract=True


class Country(Identifiant):
    flag = models.ImageField(upload_to="country/flag", null=True, blank=True)
    nationality_label = models.CharField(max_length=255)

    class Meta:
        verbose_name="Pays"

    def __str__(self) -> str:
        return self.label


class Departement(Identifiant):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="Pays", related_name="departement")


class Town(Identifiant):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="town")
    
    class Meta:
        verbose_name="Ville"


class Bundle(models.Model):
    code = models.CharField(max_length=10)
    label = models.CharField(max_length=200, verbose_name="Libellé")

    class Meta:
        verbose_name="Liasse"

    def __str__(self) -> str:
        return self.code


class ChartOfAccount(models.Model):
    SENS_DC_CHOICES = [
        ('Debit', 'DEBIT'),
        ('credit', 'CREDIT'),
        ('debit & credit', 'DEBIT & CREDIT'),
    ]
    CHOICES = (
        (1, 'Classe 1'),
        (2, 'Classe 2'),
        (3, 'Classe 3'),
        (4, 'Classe 4'),
        (5, 'Classe 5'),
        (6, 'Classe 6'),
        (7, 'Classe 7'),
        (8, 'Classe 8'),
        (9, 'Classe 9'),
    )
    clase_number = models.IntegerField(choices=CHOICES, verbose_name="Classe")
    code = models.CharField(max_length=10, verbose_name="Numéro compte")
    label = models.CharField(max_length=200, verbose_name="Libellé")
    credit_balance = models.FloatField(default=0, verbose_name="Solde Crédit")
    debit_balance = models.FloatField(default=0, verbose_name="Solde Dédit")
    debit_bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, verbose_name="Liasse Dédit", related_name="chart_of_account_debit", null=True, blank=True)
    credit_bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, verbose_name="Liasse Crédit", related_name="chart_of_account_credit", null=True, blank=True)
    senc_dc = models.CharField(max_length=20, choices=SENS_DC_CHOICES, verbose_name="SENS_DC", null=True, blank=True)
    is_chapter = models.BooleanField(null=True, blank=True, verbose_name="Est compte chapitre")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, verbose_name="Année académique", related_name="chart_of_account")
    
    class Meta:
        verbose_name="Plan comptable"

    def __str__(self) -> str:
        return self.code


class Box(models.Model):
    code = models.CharField(max_length=20)
    label = models.CharField(max_length=255)
    max_withdrawal_per_period = models.FloatField(verbose_name="Retrait maximum par période")
    max_withdrawal_per_transaction = models.FloatField(verbose_name="Retrait maximum par opération")
    max_withdrawal_period = models.FloatField(verbose_name="Periode de Retrait maximum")
    payment_authorized = models.BooleanField(default=True, verbose_name="Versement autorisé")
    withdrawal_authorized = models.BooleanField(default=True, verbose_name="Retrait autorisé")
    withdrawal_authorized = models.BooleanField(default=True, verbose_name="Transfert intercaisse autorisé")
    inter_cash_transfer_authorized = models.BooleanField(default=True, verbose_name="Transfert intercaisse autorisé")
    cash_balance = models.BooleanField(default=0, verbose_name="Solde actuel")
    bank_withdrawal_transfer_authorized = models.BooleanField(default=True, verbose_name="Tansfert/retrait banque autorisé")
    is_actif = models.BooleanField(default=True, verbose_name="Actif")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, verbose_name="Année académique", related_name="box_year")
    chart_of_account = models.ForeignKey(ChartOfAccount, on_delete=models.PROTECT, verbose_name="Compte associé", related_name="box_chart")

    class Meta:
        verbose_name="Caisse"

    def __str__(self) -> str:
        return self.code
    

class Speciality(IdentifiantGlobal):
    class Meta:
        verbose_name = "Specialité"


class Echelon(IdentifiantGlobal):
    pass


class CategoryTeacher(IdentifiantGlobal):
    class Meta:
        verbose_name="Catégorie"


class Ladder(IdentifiantGlobal):
    class Meta:
        verbose_name="Echelle"


class Grade(IdentifiantGlobal):
    pass


class PersonalClass(IdentifiantGlobal):
    class Meta:
        verbose_name = "Classe personnelle"
