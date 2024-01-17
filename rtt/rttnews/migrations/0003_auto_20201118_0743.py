# Generated by Django 3.1.1 on 2020-11-18 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttregulation', '0002_regulationrating_regulatoryframeworkrating'),
        ('rttnews', '0002_auto_20201019_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='regulatory_frameworks',
            field=models.ManyToManyField(blank=True, related_name='news_regulatory_frameworks', to='rttregulation.RegulatoryFramework'),
        ),
    ]
