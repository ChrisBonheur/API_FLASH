# Generated by Django 5.0.2 on 2024-04-17 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("config_global", "0004_auto_20240417_1036"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nivel",
            name="cycle",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nivel",
                to="config_global.cycle",
            ),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name="nivel",
            constraint=models.UniqueConstraint(
                fields=("cycle", "order"), name="unique_order_cycle"
            ),
        ),
        migrations.AddConstraint(
            model_name="nivel",
            constraint=models.UniqueConstraint(
                fields=("cycle", "label"), name="unique_label_cycle"
            ),
        ),
        migrations.AddConstraint(
            model_name="nivel",
            constraint=models.UniqueConstraint(
                fields=("cycle", "code"), name="unique_code_cycle"
            ),
        ),
    ]
