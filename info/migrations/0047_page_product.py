# Generated by Django 3.1.3 on 2021-04-03 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20210327_1933'),
        ('info', '0046_auto_20210403_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page', to='products.product'),
        ),
    ]