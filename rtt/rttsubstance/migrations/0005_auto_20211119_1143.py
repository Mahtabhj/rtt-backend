# Generated by Django 3.1.1 on 2021-11-19 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttsubstance', '0004_substanceuploadlog_file_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='substance',
            name='cas_no',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='substance',
            name='ec_no',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]