# Generated by Django 3.1.2 on 2021-04-13 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210404_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='describtion',
            field=models.TextField(null=True),
        ),
    ]
