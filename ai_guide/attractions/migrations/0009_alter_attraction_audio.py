# Generated by Django 4.2.6 on 2023-10-16 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0008_alter_attraction_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attraction',
            name='audio',
            field=models.FilePathField(blank=True),
        ),
    ]