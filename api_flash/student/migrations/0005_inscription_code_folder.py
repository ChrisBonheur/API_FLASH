# Generated by Django 5.0.2 on 2024-04-17 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0004_inscription_parcours_suggest_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="inscription",
            name="code_folder",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
