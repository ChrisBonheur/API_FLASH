# Generated by Django 5.0.2 on 2024-08-19 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_alter_numero_sommaire_pdf_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title_ang',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title_fr',
            field=models.TextField(),
        ),
    ]
