# Generated by Django 3.1.3 on 2021-04-03 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0044_auto_20210301_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='product_button_text',
            field=models.CharField(blank=True, default='Learn More', max_length=30),
        ),
    ]