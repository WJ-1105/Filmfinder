# Generated by Django 3.1.2 on 2020-11-02 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_review_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_movie_rate',
            name='integer_rate',
            field=models.IntegerField(default=0),
        ),
    ]