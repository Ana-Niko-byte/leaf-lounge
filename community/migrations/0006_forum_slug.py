# Generated by Django 5.0.6 on 2024-08-18 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0005_forum_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
