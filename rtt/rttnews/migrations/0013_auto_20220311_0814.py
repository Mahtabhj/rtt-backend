# Generated by Django 3.1.1 on 2022-03-11 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttnews', '0012_merge_20210921_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]