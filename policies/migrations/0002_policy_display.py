# Generated by Django 3.1.8 on 2021-05-05 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='display',
            field=models.BooleanField(default=True),
        ),
    ]
