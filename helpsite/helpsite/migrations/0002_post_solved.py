# Generated by Django 3.2.11 on 2022-05-20 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='solved',
            field=models.BooleanField(default=False),
        ),
    ]
