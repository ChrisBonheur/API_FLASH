# Generated by Django 5.0.2 on 2024-08-19 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdocument',
            name='type_user',
            field=models.SmallIntegerField(choices=[(2, 'AGENT'), (3, 'ENSEIGNANT'), (5, 'ETUDIANT')]),
        ),
    ]
