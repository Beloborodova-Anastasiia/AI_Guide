# Generated by Django 4.2 on 2023-09-30 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0003_rename_name_attraction_object_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attraction',
            name='object_name',
            field=models.CharField(db_index=True, max_length=256, unique=True, verbose_name='Name'),
        ),
    ]
