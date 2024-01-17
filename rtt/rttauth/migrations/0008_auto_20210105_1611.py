# Generated by Django 3.1.1 on 2021-01-05 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rttauth', '0007_userinvite'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('pending', 'Pending'), ('accepted', 'Accepted'), ('deleted', 'Deleted')], default='created', max_length=10),
        ),
        migrations.AlterField(
            model_name='userinvite',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('pending', 'Pending'), ('accepted', 'Accepted'), ('deleted', 'Deleted')], default='pending', max_length=10),
        ),
    ]
