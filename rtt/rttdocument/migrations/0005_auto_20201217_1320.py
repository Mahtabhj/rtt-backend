# Generated by Django 3.1.1 on 2020-12-17 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttdocument', '0004_auto_20201215_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='help',
            name='documents',
            field=models.ManyToManyField(blank=True, related_name='help_documents', to='rttdocument.Document'),
        ),
    ]