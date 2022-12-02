# Generated by Django 4.1.2 on 2022-10-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_tags_active_alter_tags_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='products.tags'),
        ),
    ]
