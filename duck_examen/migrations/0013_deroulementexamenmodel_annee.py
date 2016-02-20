# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0012_auto_20160220_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='deroulementexamenmodel',
            name='annee',
            field=models.CharField(default=2015, max_length=4),
        ),
    ]
