# Generated by Django 3.1.1 on 2022-06-23 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttproduct', '0007_auto_20220425_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
