# Generated by Django 3.1.1 on 2022-08-24 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rttorganization', '0012_merge_20211221_1319'),
        ('rttregulation', '0029_merge_20220804_0451'),
    ]

    operations = [
        migrations.CreateModel(
            name='MilestoneMute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_muted', models.BooleanField(default=False)),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='milestone_mute_milestone', to='rttregulation.regulationmilestone')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='milestone_mute_org', to='rttorganization.organization')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddConstraint(
            model_name='milestonemute',
            constraint=models.UniqueConstraint(fields=('organization', 'milestone'), name='unique_org_milestone_milestone_mute'),
        ),
    ]
