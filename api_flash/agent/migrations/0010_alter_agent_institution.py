# Generated by Django 5.0.2 on 2024-03-18 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0009_alter_agent_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='institution',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
