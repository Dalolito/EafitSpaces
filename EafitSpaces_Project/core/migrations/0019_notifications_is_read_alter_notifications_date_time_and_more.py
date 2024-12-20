# Generated by Django 5.0.7 on 2024-10-17 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_reservation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.reservation'),
        ),
    ]
