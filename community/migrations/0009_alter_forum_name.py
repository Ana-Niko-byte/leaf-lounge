# Generated by Django 5.0.6 on 2024-09-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0008_remove_community_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
