# Generated by Django 3.1.9 on 2021-06-07 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='billing_postcode',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_postcode',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
