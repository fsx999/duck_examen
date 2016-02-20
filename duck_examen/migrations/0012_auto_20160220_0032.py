# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0011_auto_20160208_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detailderoulement',
            name='type_examen',
        ),
        migrations.RemoveField(
            model_name='etapesettingsderoulemodel',
            name='deroule',
        ),
        migrations.RemoveField(
            model_name='etapesettingsderoulemodel',
            name='type_examen',
        ),
        migrations.AddField(
            model_name='detailderoulement',
            name='deroule',
            field=models.FileField(null=True, upload_to=b'deroule_examen', blank=True),
        ),
    ]
