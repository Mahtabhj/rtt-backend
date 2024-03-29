# Generated by Django 3.1.1 on 2021-12-15 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rttsubstance', '0006_auto_20211201_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='substancefamily',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_substance', to='rttsubstance.substance'),
        ),
        migrations.AlterField(
            model_name='substancefamily',
            name='substance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='substance_family', to='rttsubstance.substance'),
        ),
    ]
