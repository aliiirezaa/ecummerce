# Generated by Django 4.1.2 on 2022-10-24 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField()),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('vote_down', models.ManyToManyField(related_name='vote_down', to=settings.AUTH_USER_MODEL)),
                ('vote_up', models.ManyToManyField(related_name='vote_up', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votesModules',
            },
        ),
        migrations.AddIndex(
            model_name='vote',
            index=models.Index(fields=['content_type', 'object_id'], name='vote_vote_content_a520b4_idx'),
        ),
    ]
