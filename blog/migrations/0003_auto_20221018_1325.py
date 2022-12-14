# Generated by Django 3.2.16 on 2022-10-18 13:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_section'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='date_create',
            new_name='date_create',
        ),
        migrations.AddField(
            model_name='post',
            name='date_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='section',
            name='url',
            field=models.CharField(default='/', max_length=100),
        ),
    ]
