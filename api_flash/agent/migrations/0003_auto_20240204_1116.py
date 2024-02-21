# Generated by Django 3.2.20 on 2024-02-04 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config_global', '0004_auto_20240204_1116'),
        ('agent', '0002_agent_detained_dependent_child_agent_basic_salary_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='matricule',
        ),
        migrations.AlterField(
            model_name='agent',
            name='town_residence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='config_global.town', verbose_name='Ville de résidence'),
        ),
    ]
