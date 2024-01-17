# Generated by Django 3.1.1 on 2022-03-15 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rttsubstance', '0012_merge_20220107_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='substanceuploadlog',
            name='traceback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UserSubstanceAddLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('file_name', models.TextField()),
                ('uses_and_application', models.TextField(blank=True, null=True)),
                ('substance_count', models.PositiveIntegerField(default=0)),
                ('process_type', models.CharField(choices=[('substance_add', 'Substance Add')], default='substance_add', max_length=100)),
                ('status', models.CharField(choices=[('success', 'Success'), ('in_progress', 'In Progress'), ('fail', 'Fail')], default='in_progress', max_length=20)),
                ('file_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('traceback', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Substance Add Log',
                'db_table': 'rttsubstance_user_substance_add_log',
                'ordering': ('-id',),
            },
        ),
    ]