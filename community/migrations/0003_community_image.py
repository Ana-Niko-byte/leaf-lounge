# Generated by Django 5.0.6 on 2024-08-06 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_alter_community_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
