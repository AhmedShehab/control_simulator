# Generated by Django 3.1.2 on 2021-05-14 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_submission_parameters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='score',
            field=models.FloatField(null=True),
        ),
    ]