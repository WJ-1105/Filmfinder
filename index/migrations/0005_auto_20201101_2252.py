# Generated by Django 3.1.2 on 2020-11-01 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_auto_20201101_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='average_rate',
            field=models.FloatField(default=0),
        ),
    ]