# Generated by Django 5.0.2 on 2024-04-16 06:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("academic_years", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=250, verbose_name="Titre")),
                (
                    "description",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("content", models.TextField()),
                (
                    "type_user",
                    models.SmallIntegerField(
                        choices=[(2, "AGENT"), (3, "ENSEIGNANT"), (4, "ETUDIANT")]
                    ),
                ),
                (
                    "date_save",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date d'enregistrement"
                    ),
                ),
                (
                    "last_update_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Dernière modification date"
                    ),
                ),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="documents_added_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Ajouté par",
                    ),
                ),
                (
                    "last_update_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="documents_last_update_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Dernière modification par",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "year",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="documents",
                        to="academic_years.academicyear",
                        verbose_name="Année académique",
                    ),
                ),
            ],
            options={
                "verbose_name": "Document",
            },
        ),
    ]
