# Generated by Django 5.0.7 on 2024-08-29 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_space_type_id_spacetype_type_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('Close', 'Close'), ('Available', 'Available')], default='Available', max_length=10),
        ),
    ]
