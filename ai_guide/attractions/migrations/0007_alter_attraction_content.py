# Generated by Django 4.2.6 on 2023-10-17 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0006_remove_attraction_misataken_names_misspellednames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attraction',
            name='content',
            field=models.TextField(max_length=10000, verbose_name='Description'),
        ),
    ]