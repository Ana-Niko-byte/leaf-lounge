# Generated by Django 5.0.6 on 2024-08-09 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_author_d_o_b'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='d_o_b',
            field=models.DateField(verbose_name='Birth Date'),
        ),
    ]
