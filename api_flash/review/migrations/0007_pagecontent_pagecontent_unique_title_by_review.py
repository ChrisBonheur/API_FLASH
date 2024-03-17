# Generated by Django 5.0.2 on 2024-03-17 14:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_review_eissn_review_issn'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True, null=True)),
                ('date_update', models.DateTimeField(auto_now_add=True)),
                ('pdf_file', models.TextField(blank=True, null=True)),
                ('order', models.SmallIntegerField(default=1)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='review.review')),
            ],
        ),
        migrations.AddConstraint(
            model_name='pagecontent',
            constraint=models.UniqueConstraint(fields=('review', 'title'), name='unique_title_by_review'),
        ),
    ]
