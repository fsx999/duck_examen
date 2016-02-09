# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0006_rattachementcentreexamen_type_amenagement'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailderoulement',
            name='amenagement_examen',
            field=models.ForeignKey(default=b'N', to='duck_examen.AmenagementExamenModel'),
        ),
    ]
