# Generated by Django 5.0.6 on 2024-09-11 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_review_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
