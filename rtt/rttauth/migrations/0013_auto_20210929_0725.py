# Generated by Django 3.1.1 on 2021-09-29 07:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rttauth', '0012_auto_20210705_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_pass_created_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last password changed timestamp'),
        ),
    ]
