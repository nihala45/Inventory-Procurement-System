# Generated by Django 5.1.6 on 2025-05-07 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_itequipmentdetails_officesupplydetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itequipmentdetails',
            name='request',
        ),
        migrations.RemoveField(
            model_name='officesupplydetails',
            name='request',
        ),
        migrations.AddField(
            model_name='procurementrequest',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.itequipmentdetails'),
        ),
    ]
