# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    AmenagementExamenModel = apps.get_model("duck_examen", "AmenagementExamenModel")
    db_alias = schema_editor.connection.alias
    AmenagementExamenModel.objects.using(db_alias).bulk_create([
        AmenagementExamenModel(type_amenagement="N"),
        AmenagementExamenModel(type_amenagement="T"),
    ])

def reverse_func(apps, schema_editor):
    AmenagementExamenModel = apps.get_model("duck_examen", "AmenagementExamenModel")
    db_alias = schema_editor.connection.alias
    AmenagementExamenModel.objects.using(db_alias).get('N').delete()
    AmenagementExamenModel.objects.using(db_alias).get('T').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0004_rattachementcentreexamen_handicap'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmenagementExamenModel',
            fields=[
                ('type_amenagement', models.CharField(default=b'N', max_length=2, serialize=False, primary_key=True, choices=[(b'N', b'Normal'), (b'T', b'Tiers-temps')])),
            ],

        ),
        # migrations.RunPython(forwards_func, reverse_func),


    ]
