# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_examen', '0013_deroulementexamenmodel_annee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailderoulement',
            name='amenagement_examen',
            field=models.ForeignKey(default=b'N', blank=True, to='duck_examen.AmenagementExamenModel'),
        ),
        migrations.AlterField(
            model_name='detailderoulement',
            name='deroulement',
            field=models.ForeignKey(blank=True, to='duck_examen.DeroulementExamenModel', null=True),
        ),
        migrations.AlterField(
            model_name='detailderoulement',
            name='parcours',
            field=models.ForeignKey(default=None, blank=True, to='duck_examen.Parcours', null=True),
        ),
    ]
