# Generated by Django 3.1.3 on 2020-12-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0022_auto_20201223_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailinfo',
            name='desc_title1_en',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='detailinfo',
            name='desc_title1_it',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='detailinfo',
            name='desc_title2_en',
            field=models.CharField(default='', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='detailinfo',
            name='desc_title2_it',
            field=models.CharField(default='', max_length=60, null=True),
        ),
    ]
