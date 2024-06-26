# Generated by Django 5.0.4 on 2024-05-25 17:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0003_subject_students'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='students',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_student': True}, related_name='subjects', to=settings.AUTH_USER_MODEL),
        ),
    ]
