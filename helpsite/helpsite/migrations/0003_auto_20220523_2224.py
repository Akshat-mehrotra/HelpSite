# Generated by Django 3.2.11 on 2022-05-23 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpsite', '0002_post_solved'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='PH',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]