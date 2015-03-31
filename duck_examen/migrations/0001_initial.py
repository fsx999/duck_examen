# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_apogee', '0001_initial'),
        ('duck_utils', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeroulementExamenModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session', models.CharField(max_length=2, choices=[(b'1', b'Premi\xc3\xa8re session'), (b'2', b'Seconde session')])),
                ('nb_salle', models.IntegerField(null=True, verbose_name=b'nombre de salle', blank=True)),
                ('nb_table', models.IntegerField(null=True, verbose_name=b'nombre de table par salle', blank=True)),
                ('deroulement', models.TextField(help_text=b'chaque ec doit \xc3\xaatre s\xc3\xa9par\xc3\xa9 par un |', null=True, verbose_name=b'Le d\xc3\xa9roulement', blank=True)),
                ('date_examen', models.TextField(null=True, verbose_name=b'Date examen', blank=True)),
                ('salle_examen', models.TextField(null=True, verbose_name=b'salles examens', blank=True)),
                ('etape', models.ForeignKey(to='django_apogee.Etape')),
            ],
            options={
                'db_table': 'core_deroulementexemenmodel',
                'verbose_name': 'Deroulement',
                'verbose_name_plural': 'Deroulements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetailDeroulement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deroulement_contenu', models.TextField(help_text=b'chaque ec doit \xc3\xaatre s\xc3\xa9par\xc3\xa9 par un |', null=True, verbose_name=b'Le d\xc3\xa9roulement', blank=True)),
                ('deroulement', models.ForeignKey(to='duck_examen.DeroulementExamenModel', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EtapeSettingsDerouleModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cod_anu', models.CharField(default=b'2014', max_length=4)),
                ('deroule', models.FileField(null=True, upload_to=b'deroule_examen', blank=True)),
                ('date_envoi_convocation', models.DateField(null=True, blank=True)),
                ('envoi_convocation_processed', models.BooleanField(default=False)),
                ('session', models.CharField(max_length=2, choices=[(b'1', b'Premi\xc3\xa8re session'), (b'2', b'Seconde session')])),
                ('etape', models.ForeignKey(to='django_apogee.Etape')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExamCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=200, null=True, verbose_name=b'center name')),
                ('mailling_address', models.TextField(verbose_name=b'Adresse du centre')),
                ('sending_address', models.TextField(null=True, verbose_name="Adresse de l'envoi du mat\xe9riel", blank=True)),
                ('last_name_manager', models.CharField(max_length=30, null=True, blank=True)),
                ('first_name', models.CharField(max_length=30, null=True, blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('email_bis', models.EmailField(max_length=75, null=True, verbose_name=b'second email', blank=True)),
                ('phone', models.CharField(max_length=30, null=True, blank=True)),
                ('fax', models.CharField(max_length=30, null=True, blank=True)),
                ('is_open', models.BooleanField(default=True, verbose_name=b'Ouvert')),
                ('has_incorporation', models.BooleanField(default=True, help_text="l'\xe9tudiant doit faire une demande de rattachement", verbose_name=b'Demande rattachement')),
                ('is_main_center', models.BooleanField(default=False)),
                ('country', models.ForeignKey(verbose_name=b'pays', to='django_apogee.Pays', null=True)),
            ],
            options={
                'verbose_name': 'Centre examen',
                'verbose_name_plural': 'Centres examens',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RattachementCentreExamen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session', models.CharField(max_length=2, choices=[(b'1', b'Premi\xc3\xa8re session'), (b'2', b'Seconde session')])),
                ('ec_manquant', models.BooleanField(default=False)),
                ('centre', models.ForeignKey(to='duck_examen.ExamCenter')),
                ('inscription', models.ForeignKey(to='django_apogee.InsAdmEtp')),
                ('salle', models.ForeignKey(blank=True, to='duck_utils.Salle', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecapitulatifExamenModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session', models.CharField(max_length=2, choices=[(b'1', b'Premi\xc3\xa8re session'), (b'2', b'Seconde session')])),
                ('date_envoie', models.DateField(null=True, verbose_name=b'date envoie des envellopes', blank=True)),
                ('date_reception', models.DateField(null=True, verbose_name=b'date r\xc3\xa9ception des enveloppes', blank=True)),
                ('anomalie', models.CharField(max_length=200, null=True, verbose_name=b'anomalie', blank=True)),
                ('nb_enveloppe', models.IntegerField(null=True, blank=True)),
                ('nb_colis', models.IntegerField(null=True, blank=True)),
                ('centre', models.ForeignKey(to='duck_examen.ExamCenter')),
                ('etape', models.ForeignKey(to='django_apogee.Etape')),
            ],
            options={
                'ordering': ['centre__country__lib_pay'],
                'verbose_name': 'Recap envoie',
                'verbose_name_plural': 'Recaps envoie',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeExamen',
            fields=[
                ('name', models.CharField(max_length=3, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rattachementcentreexamen',
            name='type_examen',
            field=models.ForeignKey(default=b'D', to='duck_examen.TypeExamen'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='etapesettingsderoulemodel',
            name='type_examen',
            field=models.ForeignKey(to='duck_examen.TypeExamen'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detailderoulement',
            name='type_examen',
            field=models.ForeignKey(default=b'D', to='duck_examen.TypeExamen', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='EtapeExamen',
            fields=[
            ],
            options={
                'verbose_name': 'Etape examen',
                'proxy': True,
            },
            bases=('django_apogee.insadmetp',),
        ),
        migrations.CreateModel(
            name='EtapeExamenModel',
            fields=[
            ],
            options={
                'ordering': ['cod_etp'],
                'proxy': True,
            },
            bases=('django_apogee.etape',),
        ),
    ]
