# Generated by Django 3.1.3 on 2020-11-28 17:37

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_homeinfo_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=5)),
                ('reviewer_name', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('display', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterModelOptions(
            name='homeinfo',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='homeinfo',
            name='order',
            field=models.SmallIntegerField(default=12, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
