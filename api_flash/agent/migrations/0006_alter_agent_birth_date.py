# Generated by Django 5.0.1 on 2024-03-13 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agent", "0005_agent_about"),
    ]

    operations = [
        migrations.AlterField(
            model_name="agent",
            name="birth_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date de naissance"
            ),
        ),
    ]
