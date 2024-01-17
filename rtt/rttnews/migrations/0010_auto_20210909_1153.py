# Generated by Django 3.1.1 on 2021-09-09 11:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rttsubstance', '0001_initial'),
        ('rttnews', '0009_auto_20210810_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='substances',
            field=models.ManyToManyField(blank=True, related_name='substances_news', to='rttsubstance.Substance'),
        ),
        migrations.CreateModel(
            name='SubstanceNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_substance_relation', to='rttnews.news')),
                ('substance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='substance_news_relation', to='rttsubstance.substance')),
            ],
            options={
                'verbose_name_plural': 'Substance News',
                'ordering': ('-id',),
            },
        ),
        migrations.AddConstraint(
            model_name='substancenews',
            constraint=models.UniqueConstraint(fields=('substance', 'news'), name='unique_substance_news'),
        ),
    ]