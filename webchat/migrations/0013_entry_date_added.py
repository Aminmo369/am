# Generated by Django 5.1.6 on 2025-02-20 18:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webchat', '0012_remove_entry_created_at_remove_entry_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
