# Generated by Django 3.1.2 on 2021-03-31 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210331_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='assignments',
            field=models.ManyToManyField(blank=True, related_name='assignments', to='main.Assignment'),
        ),
    ]
