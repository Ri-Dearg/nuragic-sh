# Generated by Django 3.1.12 on 2021-06-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_product_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='times_purchased',
            field=models.IntegerField(default=0),
        ),
    ]
