# Generated by Django 3.1.3 on 2021-01-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210107_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_it',
            field=models.TextField(null=True),
        ),
    ]