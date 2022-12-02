# Generated by Django 4.1.2 on 2022-10-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_slug_alter_products_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='tags',
            field=models.ManyToManyField(blank=True, to='products.tags'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True),
        ),
    ]