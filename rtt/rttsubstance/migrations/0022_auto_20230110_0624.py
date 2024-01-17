# Generated by Django 3.1.1 on 2023-01-10 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttsubstance', '0021_auto_20221208_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='prioritizationstrategy',
            name='default_org_strategy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name='prioritizationstrategy',
            constraint=models.UniqueConstraint(condition=models.Q(default_org_strategy=True), fields=('organization', 'default_org_strategy'), name='unique_organization_default_org_strategy'),
        ),
    ]