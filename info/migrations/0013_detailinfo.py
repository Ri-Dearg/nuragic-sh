# Generated by Django 3.1.3 on 2020-12-16 18:20

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0012_auto_20201216_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('summary', models.CharField(max_length=400)),
                ('description1', models.TextField()),
                ('description2', models.TextField()),
                ('title_image', models.ImageField(upload_to='info/detail/title')),
                ('desc_image', models.ImageField(blank=True, upload_to='info/detail/desc')),
                ('gallery', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.ImageField(blank=True, upload_to=''), default=list, size=None)),
            ],
        ),
    ]
