# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0010_auto_20160205_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rattachementcentreexamen',
            name='parcours',
            field=models.ForeignKey(blank=True, to='duck_examen.Parcours', null=True),
        ),
    ]
