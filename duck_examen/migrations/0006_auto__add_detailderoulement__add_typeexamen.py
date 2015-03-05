# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DetailDeroulement'
        db.create_table(u'duck_examen_detailderoulement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deroulement', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('type_examen', self.gf('django.db.models.fields.related.ForeignKey')(default='D', to=orm['duck_examen.TypeExamen'], null=True)),
        ))
        db.send_create_signal(u'duck_examen', ['DetailDeroulement'])

        # Adding model 'TypeExamen'
        db.create_table(u'duck_examen_typeexamen', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1, primary_key=True)),
        ))
        db.send_create_signal(u'duck_examen', ['TypeExamen'])


    def backwards(self, orm):
        # Deleting model 'DetailDeroulement'
        db.delete_table(u'duck_examen_detailderoulement')

        # Deleting model 'TypeExamen'
        db.delete_table(u'duck_examen_typeexamen')


    models = {
        u'django_apogee.anneeuni': {
            'Meta': {'ordering': "[u'-cod_anu']", 'object_name': 'AnneeUni', 'db_table': "u'ANNEE_UNI'"},
            'cod_anu': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True', 'db_column': "u'COD_ANU'"}),
            'eta_anu_iae': ('django.db.models.fields.CharField', [], {'default': "u'I'", 'max_length': '1', 'db_column': "u'ETA_ANU_IAE'"})
        },
        u'django_apogee.etape': {
            'Meta': {'object_name': 'Etape', 'db_table': "u'ETAPE'"},
            'cod_cur': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_CUR'"}),
            'cod_cyc': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_CYC'"}),
            'cod_etp': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True', 'db_column': "u'COD_ETP'"}),
            'lib_etp': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'db_column': "u'LIB_ETP'"})
        },
        u'django_apogee.individu': {
            'Meta': {'object_name': 'Individu', 'db_table': "u'INDIVIDU'"},
            'cod_cle_nne_ind': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_CLE_NNE_IND'"}),
            'cod_etb': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'db_column': "u'COD_ETB'"}),
            'cod_etu': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'COD_ETU'"}),
            'cod_fam': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_FAM'"}),
            'cod_ind': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "u'COD_IND'"}),
            'cod_ind_opi': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'COD_IND_OPI'"}),
            'cod_nne_ind': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'db_column': "u'COD_NNE_IND'"}),
            'cod_pay_nat': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_column': "u'COD_PAY_NAT'"}),
            'cod_sex_etu': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_SEX_ETU'"}),
            'cod_sim': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'COD_SIM'"}),
            'cod_thp': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'db_column': "u'COD_THP'"}),
            'cod_uti': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'db_column': "u'COD_UTI'"}),
            'daa_ens_sup': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'db_column': "u'DAA_ENS_SUP'"}),
            'daa_ent_etb': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'db_column': "u'DAA_ENT_ETB'"}),
            'daa_etb': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'db_column': "u'DAA_ETB'"}),
            'daa_lbt_ind': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'db_column': "u'DAA_LBT_IND'"}),
            'dat_cre_ind': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "u'DAT_CRE_IND'"}),
            'dat_mod_ind': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "u'DAT_MOD_IND'"}),
            'date_nai_ind': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "u'DATE_NAI_IND'"}),
            'dmm_lbt_ind': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'db_column': "u'DMM_LBT_IND'"}),
            'lib_nom_pat_ind': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'db_column': "u'LIB_NOM_PAT_IND'"}),
            'lib_nom_usu_ind': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'db_column': "u'LIB_NOM_USU_IND'"}),
            'lib_pr1_ind': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "u'LIB_PR1_IND'"}),
            'lib_pr2_ind': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "u'LIB_PR2_IND'"}),
            'lib_pr3_ind': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "u'LIB_PR3_IND'"}),
            'tem_date_nai_rel': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1', 'null': 'True', 'db_column': "u'TEM_DATE_NAI_REL'"})
        },
        u'django_apogee.insadmetp': {
            'Meta': {'object_name': 'InsAdmEtp', 'db_table': "u'INS_ADM_ETP_COPY'"},
            'cod_anu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.AnneeUni']"}),
            'cod_cge': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_column': "u'COD_CGE'"}),
            'cod_dip': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'db_column': "u'COD_DIP'"}),
            'cod_etp': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'db_column': "u'COD_ETP'"}),
            'cod_ind': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'etapes_ied'", 'db_column': "u'COD_IND'", 'to': u"orm['django_apogee.Individu']"}),
            'cod_pru': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'db_column': "u'COD_PRU'"}),
            'cod_vrs_vdi': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_column': "u'COD_VRS_VDI'"}),
            'cod_vrs_vet': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "u'COD_VRS_VET'"}),
            'dat_annul_res_iae': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "u'DAT_ANNUL_RES_IAE'"}),
            'dat_cre_iae': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "u'DAT_CRE_IAE'"}),
            'dat_mod_iae': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "u'DAT_MOD_IAE'"}),
            'demi_annee': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'eta_iae': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'ETA_IAE'"}),
            'eta_pmt_iae': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'ETA_PMT_IAE'"}),
            'exoneration': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'force_encaissement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'nbr_ins_cyc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'NBR_INS_CYC'"}),
            'nbr_ins_dip': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'NBR_INS_DIP'"}),
            'nbr_ins_etp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "u'NBR_INS_ETP'"}),
            'num_occ_iae': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'db_column': "u'NUM_OCC_IAE'"}),
            'tem_iae_prm': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "u'TEM_IAE_PRM'"})
        },
        u'django_apogee.pays': {
            'Meta': {'ordering': "[u'lic_pay']", 'object_name': 'Pays', 'db_table': "u'PAYS'"},
            'cod_pay': ('django.db.models.fields.CharField', [], {'max_length': '3', 'primary_key': 'True', 'db_column': "u'COD_PAY'"}),
            'cod_sis_pay': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "u'COD_SIS_PAY'"}),
            'lib_nat': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_NAT'"}),
            'lib_pay': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "u'LIB_PAY'"}),
            'lic_pay': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "u'LIC_PAY'"}),
            'tem_afl_dec_ind_pay': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_AFL_DEC_IND_PAY'"}),
            'tem_del': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_DEL'"}),
            'tem_en_sve_pay': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_EN_SVE_PAY'"}),
            'tem_ouv_drt_sso_pay': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "u'TEM_OUV_DRT_SSO_PAY'"})
        },
        u'duck_examen.deroulementexamenmodel': {
            'Meta': {'object_name': 'DeroulementExamenModel', 'db_table': "'core_deroulementexemenmodel'"},
            'date_examen': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deroulement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'etape': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.Etape']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nb_salle': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_table': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'salle_examen': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'duck_examen.detailderoulement': {
            'Meta': {'object_name': 'DetailDeroulement'},
            'deroulement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_examen': ('django.db.models.fields.related.ForeignKey', [], {'default': "'D'", 'to': u"orm['duck_examen.TypeExamen']", 'null': 'True'})
        },
        u'duck_examen.examcenter': {
            'Meta': {'object_name': 'ExamCenter'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.Pays']", 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'email_bis': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'has_incorporation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_main_center': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'last_name_manager': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'mailling_address': ('django.db.models.fields.TextField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'sending_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'duck_examen.rattachementcentreexamen': {
            'Meta': {'object_name': 'RattachementCentreExamen'},
            'centre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duck_examen.ExamCenter']"}),
            'ec_manquant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inscription': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.InsAdmEtp']"}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'duck_examen.recapitulatifexamenmodel': {
            'Meta': {'ordering': "['centre__country__lib_pay']", 'object_name': 'RecapitulatifExamenModel'},
            'anomalie': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'centre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['duck_examen.ExamCenter']"}),
            'date_envoie': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_reception': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'etape': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_apogee.Etape']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nb_colis': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_enveloppe': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'duck_examen.typeexamen': {
            'Meta': {'object_name': 'TypeExamen'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True'})
        }
    }

    complete_apps = ['duck_examen']