# Generated by Django 3.1.1 on 2021-08-10 13:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rttorganization', '0008_organization_industries'),
        ('rttnews', '0008_newsrelevance_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsAssessmentWorkflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(choices=[('to_be_assessed', 'To Be Assessed'), ('completed', 'Completed')], default='to_be_assessed', max_length=30)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rttnews.news')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rttorganization.organization')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddConstraint(
            model_name='newsassessmentworkflow',
            constraint=models.UniqueConstraint(fields=('news', 'organization'), name='unique_news_organization'),
        ),
    ]