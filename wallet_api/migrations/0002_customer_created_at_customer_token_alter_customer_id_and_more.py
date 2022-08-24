# Generated by Django 4.1 on 2022-08-24 14:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='token',
            field=models.CharField(max_length=42, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator]),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='enabled_at',
            field=models.DateTimeField(blank=True),
        ),
    ]
