# Generated by Django 4.1.2 on 2022-10-27 16:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='vote_down',
            field=models.ManyToManyField(blank=True, null=True, related_name='vote_down', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote_up',
            field=models.ManyToManyField(blank=True, null=True, related_name='vote_up', to=settings.AUTH_USER_MODEL),
        ),
    ]