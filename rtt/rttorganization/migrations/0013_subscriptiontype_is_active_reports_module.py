# Generated by Django 3.1.1 on 2022-11-17 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttorganization', '0012_merge_20211221_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptiontype',
            name='is_active_reports_module',
            field=models.BooleanField(default=False),
        ),
    ]