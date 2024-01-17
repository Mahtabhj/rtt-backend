# Generated by Django 3.1.1 on 2022-06-23 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttsubstance', '0016_auto_20220513_0846'),
        ('rtttaskManagement', '0006_merge_20220512_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='substances',
            field=models.ManyToManyField(blank=True, related_name='task_substances', to='rttsubstance.Substance'),
        ),
    ]