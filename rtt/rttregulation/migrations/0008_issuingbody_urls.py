# Generated by Django 3.1.1 on 2020-12-29 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttregulation', '0007_auto_20201217_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuingbody',
            name='urls',
            field=models.ManyToManyField(blank=True, related_name='issuing_body_urls', to='rttregulation.Url'),
        ),
    ]
