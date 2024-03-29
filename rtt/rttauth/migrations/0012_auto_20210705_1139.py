# Generated by Django 3.1.1 on 2021-07-05 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rttauth', '0011_auto_20210406_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_pass_created_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp'),
        ),
        migrations.CreateModel(
            name='FailedLoginAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='failed_login_attempt_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
