# Generated by Django 3.1.2 on 2021-07-05 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20210630_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='simulator',
            field=models.CharField(choices=[('Cruise Control', 'Cruise Control'), ('Servo Motor', 'Servo Motor')], max_length=64, null=True),
        ),
    ]
