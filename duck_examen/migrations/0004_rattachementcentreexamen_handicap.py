# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0003_auto_20151217_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='rattachementcentreexamen',
            name='handicap',
            field=models.BooleanField(default=False),
        ),
    ]
