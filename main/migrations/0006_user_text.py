# Generated by Django 5.1.4 on 2025-03-05 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='text',
            field=models.CharField(default='aaa', max_length=255),
        ),
    ]
