# Generated by Django 3.1.3 on 2021-02-28 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0041_auto_20210228_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_fb_link_md',
            field=models.ImageField(default='', upload_to='info/category'),
        ),
        migrations.AddField(
            model_name='category',
            name='image_fb_link_sm',
            field=models.ImageField(default='', upload_to='info/category'),
        ),
        migrations.AlterField(
            model_name='splashimage',
            name='image_fb_link',
            field=models.ImageField(upload_to='info/carousel'),
        ),
        migrations.AlterField(
            model_name='splashimage',
            name='image_fb_link_md',
            field=models.ImageField(default='', upload_to='info/carousel'),
        ),
        migrations.AlterField(
            model_name='splashimage',
            name='image_fb_link_sm',
            field=models.ImageField(default='', upload_to='info/carousel'),
        ),
        migrations.AlterField(
            model_name='splashimage',
            name='image_tw_header',
            field=models.ImageField(upload_to='info/carousel'),
        ),
        migrations.AlterField(
            model_name='splashimage',
            name='image_tw_header_md',
            field=models.ImageField(default='', upload_to='info/carousel'),
        ),
        migrations.AlterField(
            model_name='splashimage',
            name='image_tw_header_sm',
            field=models.ImageField(default='', upload_to='info/carousel'),
        ),
    ]