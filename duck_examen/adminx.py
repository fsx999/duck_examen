# coding=utf-8
from django.utils.encoding import smart_unicode
from django_apogee.models import Pays
from duck_examen.models import EtapeExamen, RattachementCentreExamen, ExamCenter
import xadmin
from xadmin.filters import RelatedFieldListFilter
from xadmin.layout import Layout, Container, Col, Fieldset
from xadmin.views import filter_hook
from django.db import models
from xadmin.views.list import EMPTY_CHANGELIST_VALUE
from django.utils.translation import ugettext as _


class PaysFilter(RelatedFieldListFilter):
    def choices(self):
        self.lookup_choices = [(x.pk, x.lib_pay) for x in Pays.objects.filter(examcenter__isnull=False).order_by('lib_pay').distinct()]
        return super(PaysFilter, self).choices()

class RattachementCentreExamenAdmin(object):
    model = RattachementCentreExamen
    style = 'table'
    extra = 2
    max_num = 2


class EtapeExamenAdmin(object):
    inlines = [RattachementCentreExamenAdmin]
    list_filter = [('rattachementcentreexamen__centre__country', PaysFilter), 'cod_etp']
    fields = [
        'get_nom', 'get_prenom',
        'get_cod_etu', 'get_adresse',
        'cod_etp', 'cod_cge',
        'get_eta_iae']
    readonly_fields = [
        'get_nom', 'get_prenom',
        'get_cod_etu', 'get_adresse',
        'cod_etp', 'cod_cge',
        'get_eta_iae', 'get_centre']
    list_display = ('__str__', 'get_nom', 'get_prenom', 'cod_etp', 'get_centre')
    search_fields = ['cod_ind__cod_etu', "cod_ind__lib_nom_pat_ind", 'cod_ind__lib_pr1_ind']
    hidden_menu = True
    show_bookmarks = False
    site_title = u'Gestion examen'
    list_per_page = 20
    form_layout = Layout(Container(Col('full',
                Fieldset(
                    "",
                    'get_nom', 'get_prenom',
                    'get_cod_etu', 'get_adresse',
                    'cod_etp', 'cod_cge',
                    'get_eta_iae', 'exoneration',
                    'demi_annee',
                    'force_encaissement'
                    , css_class="unsort no_title"), horizontal=True, span=12)
            ))

    def get_nom(self, obj):
        return obj.cod_ind.lib_nom_pat_ind
    get_nom.short_description = 'Nom'
    get_nom.allow_tags = True

    def get_prenom(self, obj):
        return '{}'.format(obj.cod_ind.lib_pr1_ind)
    get_prenom.short_description = 'Prenom'
    get_prenom.allow_tags = True

    def get_cod_etu(self, obj):
        return '{}'.format(obj.cod_ind.cod_etu)
    get_cod_etu.short_description = 'Code étudiant'
    get_cod_etu.allow_tags = True

    def get_cod_opi(self, obj):
        return '{}'.format(obj.cod_ind.cod_ind_opi)
    get_cod_opi.short_description = 'Code opi'
    get_cod_opi.allow_tags = True

    def get_adresse(self, obj):
        return '{}'.format(obj.cod_ind.get_full_adresse(obj.cod_anu.cod_anu))
    get_adresse.short_description = 'Adresse'
    get_adresse.allow_tags = True

    def get_eta_iae(self, obj):
        return '{}'.format(obj.annulation())
    get_eta_iae.short_description = 'Etat de l\'inscription administrative'
    get_eta_iae.allow_tags = True

    def get_centre(self, obj):
        txt = u""
        for rattachement in obj.rattachementcentreexamen_set.all():
            txt += str(rattachement)
        return txt
    get_centre.short_description = 'Centre'

class ExamenCenterAdmin(object):
    hidden_menu = True
    show_bookmarks = False
    search_fields = ['label', 'country__lib_pay']
    ordering = ['country__lib_pay']
    list_filter = [('country', PaysFilter)]



xadmin.site.register(EtapeExamen, EtapeExamenAdmin)
xadmin.site.register(ExamCenter, ExamenCenterAdmin)