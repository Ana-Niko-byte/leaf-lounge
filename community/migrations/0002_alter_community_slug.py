# Generated by Django 5.0.6 on 2024-08-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
