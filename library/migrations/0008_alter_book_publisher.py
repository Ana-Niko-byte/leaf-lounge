# Generated by Django 5.0.6 on 2024-07-11 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_book_publisher_book_rating_alter_author_nationality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(default='test publisher & co.', max_length=100),
            preserve_default=False,
        ),
    ]
