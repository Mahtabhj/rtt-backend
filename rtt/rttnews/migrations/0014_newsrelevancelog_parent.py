# Generated by Django 3.1.1 on 2022-03-14 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rttnews', '0013_newsrelevancelog_prev_relevancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsrelevancelog',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rttnews.newsrelevancelog'),
        ),
    ]
