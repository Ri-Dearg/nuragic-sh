# Generated by Django 3.1.3 on 2021-01-04 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0009_auto_20201216_1927'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailhistory',
            options={'ordering': ['email_address'], 'verbose_name_plural': 'Email Histories'},
        ),
    ]
