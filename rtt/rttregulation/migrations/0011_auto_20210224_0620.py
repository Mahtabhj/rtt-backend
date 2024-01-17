# Generated by Django 3.1.1 on 2021-02-24 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttdocument', '0006_auto_20210104_1709'),
        ('rttregulation', '0010_auto_20210107_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulatoryframework',
            name='documents',
            field=models.ManyToManyField(blank=True, related_name='framework_documents', to='rttdocument.Document'),
        ),
    ]
