# Generated by Django 3.2.20 on 2024-02-17 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0008_alter_agent_last_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='photo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
