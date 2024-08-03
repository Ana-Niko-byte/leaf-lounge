# Generated by Django 5.0.6 on 2024-08-03 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
        ('library', '0002_alter_genre_community'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='community',
            field=models.ForeignKey(blank=True, help_text='This field will be auto-filled after save.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='genre_community', to='community.community'),
        ),
    ]
