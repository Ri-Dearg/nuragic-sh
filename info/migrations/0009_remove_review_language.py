# Generated by Django 3.1.3 on 2020-12-10 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0008_auto_20201210_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='language',
        ),
    ]