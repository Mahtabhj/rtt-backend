# Generated by Django 3.1.1 on 2021-06-14 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rttregulation', '0014_auto_20210609_0809'),
        ('rttproduct', '0005_industry_topics'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationAlert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=500)),
                ('content', models.CharField(choices=[('news', 'News'), ('regulatory_updates', 'Regulatory updates'), ('assessments', 'Assessments')], max_length=255)),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('material_categories', models.ManyToManyField(blank=True, to='rttproduct.MaterialCategory')),
                ('product_categories', models.ManyToManyField(blank=True, to='rttproduct.ProductCategory')),
                ('regions', models.ManyToManyField(blank=True, to='rttregulation.Region')),
                ('regulatory_frameworks', models.ManyToManyField(blank=True, to='rttregulation.RegulatoryFramework')),
                ('topics', models.ManyToManyField(blank=True, to='rttregulation.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notification_alert', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notification Alerts',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='NotificationAlertLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(max_length=500)),
                ('filter_criteria', models.TextField(blank=True, null=True)),
                ('notification_alert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rttnotification.notificationalert')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notification Alert Logs',
                'ordering': ('-notification_alert',),
            },
        ),
    ]
