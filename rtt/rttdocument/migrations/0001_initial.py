# Generated by Django 3.1.1 on 2020-10-19 14:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Document Types',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='media/documents')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='document_type', to='rttdocument.documenttype')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
    ]
