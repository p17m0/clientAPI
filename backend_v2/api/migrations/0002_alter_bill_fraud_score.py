# Generated by Django 4.0.6 on 2022-07-05 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='fraud_score',
            field=models.FloatField(),
        ),
    ]
