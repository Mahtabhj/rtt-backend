# Generated by Django 3.1.1 on 2021-09-29 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttsubstance', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='prioritizationstrategy',
            constraint=models.UniqueConstraint(fields=('organization',), name='unique_organization_strategy'),
        ),
    ]
