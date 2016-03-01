# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0005_amenagementexamenmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='rattachementcentreexamen',
            name='type_amenagement',
            field=models.ForeignKey(default=b'N', to='duck_examen.AmenagementExamenModel'),
        ),
    ]
