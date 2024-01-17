# Generated by Django 3.1.1 on 2021-08-26 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttregulation', '0015_regulationratinglog'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='regulationrating',
            constraint=models.UniqueConstraint(fields=('organization', 'regulation'), name='unique_regulation_organization_relevancy'),
        ),
    ]
