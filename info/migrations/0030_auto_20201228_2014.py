# Generated by Django 3.1.3 on 2020-12-28 19:14

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0029_auto_20201228_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_en',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_it',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='description1',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='page',
            name='description1_en',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='description1_it',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='description2',
            field=tinymce.models.HTMLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='page',
            name='description2_en',
            field=tinymce.models.HTMLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='description2_it',
            field=tinymce.models.HTMLField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='text_en',
            field=tinymce.models.HTMLField(null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='text_it',
            field=tinymce.models.HTMLField(null=True),
        ),
    ]
