# Generated by Django 3.1.8 on 2021-05-18 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20210504_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='popularity',
            field=models.DecimalField(decimal_places=20, default=0, editable=False, max_digits=20),
        ),
    ]
