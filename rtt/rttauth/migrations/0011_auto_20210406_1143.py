# Generated by Django 3.1.1 on 2021-04-06 11:43

from django.db import migrations, models
import rttauth.models.models


class Migration(migrations.Migration):

    dependencies = [
        ('rttauth', '0010_passwordreset'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', rttauth.models.models.CustomUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='passwordreset',
            name='code',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
