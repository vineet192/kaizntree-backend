# Generated by Django 4.1.13 on 2024-02-11 22:44

from django.db import migrations, models
import django.utils.timezone
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('sku', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('tags', djongo.models.fields.JSONField(blank=True, default=[], null=True)),
                ('category', models.CharField(default='', max_length=100)),
                ('in_stock', models.FloatField()),
                ('available_stock', models.FloatField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
