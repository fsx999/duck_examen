# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0002_auto_20150417_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etapesettingsderoulemodel',
            name='cod_anu',
            field=models.CharField(default=b'2015', max_length=4),
        ),
        migrations.AlterField(
            model_name='rattachementcentreexamen',
            name='centre',
            field=models.ForeignKey(to='duck_examen.ExamCenter', null=True),
        ),
    ]
