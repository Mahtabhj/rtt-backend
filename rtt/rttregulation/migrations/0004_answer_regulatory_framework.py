# Generated by Django 3.1.1 on 2020-12-15 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rttregulation', '0003_auto_20201118_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='regulatory_framework',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rttregulation.regulatoryframework'),
        ),
    ]
