# Generated by Django 3.1.3 on 2021-01-26 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20210107_1839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopcategory',
            options={'ordering': ['title'], 'verbose_name_plural': 'Shop Categories'},
        ),
    ]
