# Generated by Django 4.1 on 2022-08-24 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_api', '0007_wallet_disabled_at_alter_wallet_enabled_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='disabled_at',
            field=models.DateTimeField(null=True),
        ),
    ]
