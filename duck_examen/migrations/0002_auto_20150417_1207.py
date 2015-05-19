# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examcenter',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='examcenter',
            name='email_bis',
            field=models.EmailField(max_length=254, null=True, verbose_name=b'second email', blank=True),
        ),
    ]
