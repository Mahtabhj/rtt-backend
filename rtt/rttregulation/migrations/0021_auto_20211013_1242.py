# Generated by Django 3.1.1 on 2021-10-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttdocument', '0006_auto_20210104_1709'),
        ('rttregulation', '0020_merge_20210921_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulationmilestone',
            name='documents',
            field=models.ManyToManyField(blank=True, related_name='documents_regulation_milestone', to='rttdocument.Document'),
        ),
        migrations.AlterField(
            model_name='regulationmilestone',
            name='urls',
            field=models.ManyToManyField(blank=True, related_name='urls_regulation_milestone', to='rttregulation.Url'),
        ),
    ]
