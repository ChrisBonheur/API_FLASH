from django.db import models
from django.contrib.auth.models import User
from api_flash.exceptions import CustomValidationError
from django.core.exceptions import ValidationError

class Review(models.Model):
    title = models.CharField(max_length=500)
    logo = models.TextField(null=True, blank=True)
    editorial_slint = models.TextField()
    editorial_slint_pdf = models.TextField()
    code = models.CharField(max_length=20)
    author = models.OneToOneField(User, on_delete=models.PROTECT, related_name="review")
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    issn = models.CharField(max_length=50, null=True, blank=True)
    eissn = models.CharField(max_length=50, null=True, blank=True)
    copyright = models.TextField(null=True, blank=True)


class TypeSource(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Volume(models.Model):
    index = models.SmallIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    year = models.CharField(max_length=4)
    pages_count = models.SmallIntegerField(null=True, blank=True, default=0)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="volumes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('review', 'index'), name="unique_index_by_review"),
            models.UniqueConstraint(fields=('review', 'year'), name="unique_year_by_review"),
        ]
        ordering = ["-index"]


class Numero(models.Model):
    volume = models.ForeignKey(Volume, on_delete=models.PROTECT, related_name="numeros")
    date_created = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    index = models.SmallIntegerField()
    sommaire_title = models.CharField(max_length=1000)
    sommaire_label = models.CharField(max_length=200, null=True, blank=True)
    sommaire_presentation = models.TextField()
    sommaire_cover = models.TextField(null=True, blank=True)
    sommaire_pdf = models.TextField()
    sommaire_authors = models.ManyToManyField(User, related_name="sommaires")

    def save(self, *args, **kwargs) -> None:
        self.label = f"N॰ {self.index} du vol {self.volume.index}"
        self.sommaire_label = f"Sommaire du n॰ {self.index} du vol {self.volume.index}"
        return super().save(*args, **kwargs)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('index', 'volume',), name="unique_in_num_review")
        ]


class Author(models.Model):
    SEXE_CHOICES = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('autre', 'Autre'),
    ]
    adress = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=30, null=True, blank=True)
    civility = models.CharField(max_length=10, choices=SEXE_CHOICES, verbose_name="Sexe")
    function = models.CharField(max_length=255, null=True, blank=True)
    institution = models.CharField(max_length=255, null=True, blank=True)
    about = models.CharField(max_length=255, null=True, blank=True)
    photo = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="author")


class Reference(models.Model):
    volume = models.CharField(max_length=255, null=True, blank=True)
    publication = models.CharField(max_length=255, null=True, blank=True)
    page_begin = models.IntegerField(null=True, blank=True)
    page_end = models.IntegerField(null=True, blank=True)
    edition_ref = models.CharField(max_length=255, null=True, blank=True)
    source_authors = models.CharField(max_length=255, null=True, blank=True)
    source_title = models.CharField(max_length=255, null=True, blank=True)
    source_city = models.CharField(max_length=50, null=True, blank=True)
    source_year_publication = models.CharField(max_length=4, null=True, blank=True)
    source_editor = models.CharField(max_length=255, null=True, blank=True)
    type_source = models.ForeignKey(TypeSource, on_delete=models.PROTECT, null=True, blank=True)


class Article(models.Model):
    class State(models.IntegerChoices):
        INITIALISATION = 1
        PARRUTION = 2
        PUBLICATION = 3
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="articles_owner")
    title_fr = models.CharField(max_length=500)
    title_ang = models.CharField(max_length=500, null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_accept = models.DateTimeField(null=True, blank=True)
    date_publication = models.DateTimeField(null=True, blank=True)
    abstract_fr = models.TextField()
    abstract_ang = models.TextField(null=True, blank=True)
    file_submit = models.TextField(null=True, blank=True)
    pdf_file = models.TextField(null=True, blank=True)
    numero = models.ForeignKey(Numero, on_delete=models.CASCADE, null=True, blank=True, related_name="articles")
    keywords_fr = models.TextField(null=True, blank=True)
    keywords_ang = models.TextField(null=True, blank=True)
    state = models.IntegerField(choices=State.choices, default=State.INITIALISATION)
    authors = models.ManyToManyField(User, related_name='articles')
    page_begin = models.IntegerField(null=True, blank=True)
    page_end = models.IntegerField(null=True, blank=True)
    doi_link = models.TextField(null=True, blank=True)
    orcid_link = models.CharField(max_length=255, null=True, blank=True)
    counter_download = models.IntegerField(default=0)
    image_cover = models.TextField(null=True, blank=True)
    references = models.ManyToManyField(Reference, blank=True, related_name="articles")


class PageContent(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(null=True, blank=True)
    date_update = models.DateTimeField(auto_now_add=True)
    pdf_file = models.TextField(null=True, blank=True)
    order = models.SmallIntegerField(default=1)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="pages")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('review', 'title'), name="unique_title_by_review"),
            models.UniqueConstraint(fields=('review', 'order'), name="unique_order_by_review"),
        ]