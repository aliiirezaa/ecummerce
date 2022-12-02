# Generated by Django 4.1.2 on 2022-10-25 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent', to='products.tags'),
        ),
    ]