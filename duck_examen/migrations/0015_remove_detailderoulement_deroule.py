# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0014_auto_20160220_0144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detailderoulement',
            name='deroule',
        ),
    ]
