# Generated by Django 3.1.1 on 2023-04-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttdocumentManagement', '0003_auto_20230208_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentmanagement',
            name='attachment_document',
            field=models.FileField(blank=True, max_length=256, null=True, upload_to='media/attachment_document'),
        ),
    ]
