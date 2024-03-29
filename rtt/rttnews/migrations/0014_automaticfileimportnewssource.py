# Generated by Django 3.1.1 on 2022-04-04 11:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rttdocument', '0006_auto_20210104_1709'),
        ('rttnews', '0013_auto_20220311_0814'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomaticFileImportNewsSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rttdocument.documenttype')),
                ('news_source', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='rttnews.source')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
