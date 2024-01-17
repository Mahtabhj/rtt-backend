# Generated by Django 3.1.1 on 2022-03-03 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rttregulation', '0022_auto_20211201_1210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='questiontype',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='answer',
            name='edited',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='pin_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_regulation_pin_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answered_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_regulation_answer_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='questiontype',
            name='name',
            field=models.TextField(),
        ),
    ]
