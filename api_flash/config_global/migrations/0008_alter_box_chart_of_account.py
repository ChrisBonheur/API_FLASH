# Generated by Django 3.2.20 on 2024-02-17 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config_global', '0007_auto_20240217_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='chart_of_account',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='config_global.chartofaccount'),
            preserve_default=False,
        ),
    ]
