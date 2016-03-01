# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0008_parcours'),
    ]

    operations = [
        migrations.AddField(
            model_name='rattachementcentreexamen',
            name='parcours',
            field=models.ForeignKey(default=None, to='duck_examen.Parcours', null=True),
        ),

    ]
