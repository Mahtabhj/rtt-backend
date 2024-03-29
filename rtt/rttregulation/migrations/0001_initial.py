# Generated by Django 3.1.1 on 2020-10-19 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rttorganization', '0001_initial'),
        ('rttproduct', '0001_initial'),
        ('rttdocument', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssuingBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=3)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='MilestoneType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
                ('chemical_id', models.CharField(blank=True, max_length=40, null=True)),
                ('iso_name', models.CharField(blank=True, max_length=40, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, default=0.0, max_digits=9)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Regulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('review_status', models.CharField(choices=[('d', 'Draft'), ('o', 'Online')], default='d', max_length=1)),
                ('documents', models.ManyToManyField(blank=True, to='rttdocument.Document')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rttregulation.language')),
                ('material_categories', models.ManyToManyField(blank=True, related_name='regulation_material_categories', to='rttproduct.MaterialCategory')),
                ('product_categories', models.ManyToManyField(blank=True, related_name='regulation_product_categories', to='rttproduct.ProductCategory')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='RegulationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Regulatory Types',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Regulation Status',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('text', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('text',),
            },
        ),
        migrations.CreateModel(
            name='RegulatoryFramework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('review_status', models.CharField(choices=[('d', 'Draft'), ('o', 'Online')], default='d', max_length=1)),
                ('documents', models.ManyToManyField(blank=True, to='rttdocument.Document')),
                ('issuing_body', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='regulatory_framework_issuing_body', to='rttregulation.issuingbody')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='language_reg_framework', to='rttregulation.language')),
                ('material_categories', models.ManyToManyField(blank=True, related_name='material_cat_reg_framework', to='rttproduct.MaterialCategory')),
                ('product_categories', models.ManyToManyField(blank=True, related_name='product_cat_reg_framework', to='rttproduct.ProductCategory')),
                ('regions', models.ManyToManyField(blank=True, related_name='regulatory_framework_region', to='rttregulation.Region')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='regulatory_framework_status', to='rttregulation.status')),
                ('topics', models.ManyToManyField(blank=True, related_name='regulatory_framework_topics', to='rttregulation.Topic')),
                ('urls', models.ManyToManyField(blank=True, related_name='url_reg_framework', to='rttregulation.Url')),
            ],
            options={
                'verbose_name_plural': 'Regulatory Frameworks',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='RegulationMilestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('from_date', models.DateTimeField(blank=True, null=True)),
                ('to_date', models.DateTimeField(blank=True, null=True)),
                ('documents', models.ManyToManyField(blank=True, to='rttdocument.Document')),
                ('regulation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='regulation_milestone', to='rttregulation.regulation')),
                ('regulatory_framework', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='regulatory_framework_milestone', to='rttregulation.regulatoryframework')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='regulation_milestone_type', to='rttregulation.milestonetype')),
                ('urls', models.ManyToManyField(blank=True, to='rttregulation.Url')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='regulation',
            name='regulatory_framework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='regulation_regulatory_framework', to='rttregulation.regulatoryframework'),
        ),
        migrations.AddField(
            model_name='regulation',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rttregulation.status'),
        ),
        migrations.AddField(
            model_name='regulation',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='regulation_topics', to='rttregulation.Topic'),
        ),
        migrations.AddField(
            model_name='regulation',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='regulation_regulation_type', to='rttregulation.regulationtype'),
        ),
        migrations.AddField(
            model_name='regulation',
            name='urls',
            field=models.ManyToManyField(blank=True, to='rttregulation.Url'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('in_charge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rttorganization.organization')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rttregulation.questiontype')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='issuingbody',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rttregulation.region'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('answer_text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('answered_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rttregulation.question')),
                ('regulation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rttregulation.regulation')),
            ],
            options={
                'ordering': ('answer_text',),
            },
        ),
    ]
