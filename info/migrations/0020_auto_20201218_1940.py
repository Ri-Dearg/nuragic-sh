# Generated by Django 3.1.3 on 2020-12-18 19:40

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0019_auto_20201216_1934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order'], 'verbose_name': 'Categorie'},
        ),
        migrations.AddField(
            model_name='detailinfo',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='detailinfo',
            name='order',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='detailinfo',
            name='desc_image',
            field=models.ImageField(blank=True, upload_to='info/detail'),
        ),
        migrations.AlterField(
            model_name='detailinfo',
            name='title_image',
            field=models.ImageField(upload_to='info/detail'),
        ),
    ]
