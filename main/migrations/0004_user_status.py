# Generated by Django 3.1.2 on 2020-12-24 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201222_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('s', 's'), ('i', 'i')], default='s', max_length=5),
        ),
    ]
