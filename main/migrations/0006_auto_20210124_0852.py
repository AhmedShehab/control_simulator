# Generated by Django 3.1.2 on 2021-01-24 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_instructor_major'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='describtion',
            field=models.TextField(default='haha'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='simulator',
            field=models.CharField(max_length=64, null=True),
        ),
    ]