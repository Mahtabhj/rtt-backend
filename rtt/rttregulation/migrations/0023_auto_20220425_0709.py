# Generated by Django 3.1.1 on 2022-04-25 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttregulation', '0022_auto_20211201_1210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='latitude',
            new_name='regulation_latitude',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='longitude',
            new_name='regulation_longitude',
        ),
        migrations.AddField(
            model_name='region',
            name='news_latitude',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='region',
            name='news_longitude',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
    ]
