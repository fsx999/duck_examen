# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_apogee', '0003_auto_20151009_1115'),
        ('duck_examen', '0007_detailderoulement_amenagement_examen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(default=b'NO NAME', max_length=256)),
                ('etape', models.ForeignKey(to='django_apogee.Etape')),
            ],
        ),
    ]
