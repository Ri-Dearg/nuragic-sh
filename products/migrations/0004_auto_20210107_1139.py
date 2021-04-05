# Generated by Django 3.1.3 on 2021-01-07 11:39

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210104_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_it',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title_en',
            field=models.CharField(default='', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title_it',
            field=models.CharField(default='', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='shopcategory',
            name='title_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='shopcategory',
            name='title_it',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
