# Generated by Django 3.1.3 on 2020-12-16 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0017_auto_20201216_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailinfo',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='info.category'),
        ),
    ]
