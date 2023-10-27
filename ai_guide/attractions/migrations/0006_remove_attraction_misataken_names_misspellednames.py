# Generated by Django 4.2 on 2023-10-01 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0005_attraction_misataken_names'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attraction',
            name='misataken_names',
        ),
        migrations.CreateModel(
            name='MisspelledNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('misspelled_name', models.CharField(db_index=True, max_length=254, unique=True, verbose_name='Misspelled name')),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attraction', to='attractions.attraction', verbose_name='Attraction')),
            ],
        ),
    ]
