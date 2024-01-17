# Generated by Django 3.1.1 on 2020-12-17 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttorganization', '0006_auto_20201217_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AddConstraint(
            model_name='organization',
            constraint=models.UniqueConstraint(fields=('name', 'active', 'country'), name='unique_organization'),
        ),
    ]