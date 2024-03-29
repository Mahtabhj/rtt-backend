# Generated by Django 3.1.1 on 2021-08-26 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


def forwards(apps, schema_editor):
    NewsRelevanceLog = apps.get_model('rttnews', 'newsrelevancelog')
    NewsRelevance = apps.get_model('rttnews', 'newsrelevance')

    rating_list = NewsRelevance.objects.all()
    NewsRelevanceLog.objects.bulk_create(
        NewsRelevanceLog(organization=x.organization,
                         news=x.news,
                         relevancy=x.relevancy,
                         comment=x.comment,
                         user=x.user)
        for x in rating_list
    )

    NewsRelevance.objects.all().delete()
    rating_list = NewsRelevanceLog.objects.all().distinct('organization_id', 'news_id') \
        .order_by('organization_id', 'news_id', '-created')

    NewsRelevance.objects.bulk_create(
        NewsRelevance(organization=x.organization,
                      news=x.news,
                      relevancy=x.relevancy,
                      comment=x.comment,
                      user=x.user)
        for x in rating_list
    )


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rttorganization', '0008_organization_industries'),
        ('rttnews', '0008_newsrelevance_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsRelevanceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                                      verbose_name='modified')),
                ('relevancy', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('news',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='news_relevance_log',
                                   to='rttnews.news')),
                ('organization',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rttorganization.organization')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('relevancy',),
            },
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
