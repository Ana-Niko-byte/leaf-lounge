# Generated by Django 5.0.6 on 2024-08-09 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='d_o_b',
            field=models.DateField(default='Unknown', verbose_name='Birth Date'),
        ),
    ]
