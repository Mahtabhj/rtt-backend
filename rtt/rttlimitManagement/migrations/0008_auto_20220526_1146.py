# Generated by Django 3.1.1 on 2022-05-26 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rttlimitManagement', '0007_auto_20220412_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='limituploadlog',
            name='traceback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='limituploadlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='limituploadlog',
            name='status',
            field=models.CharField(choices=[('in_queue', 'In Queue'), ('in_progress', 'In Progress'), ('success', 'Success'), ('fail', 'Fail')], default='in_progress', max_length=20),
        ),
    ]