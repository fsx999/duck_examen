# coding=utf-8
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.views.decorators.cache import never_cache
from wkhtmltopdf.views import PDFTemplateView
from django_apogee.models import Pays, Etape
from duck_examen.models import EtapeExamen, RattachementCentreExamen, ExamCenter
import xadmin
from xadmin.filters import RelatedFieldListFilter
from xadmin.layout import Layout, Container, Col, Fieldset
from xadmin.views import filter_hook
from django.db import models
from xadmin import views


class ListImpressionView(views.Dashboard):
    base_template = 'duck_examen/list_impression_examen.html'
    widget_customiz = False
    title = 'Liste des impressions'
    @filter_hook
    def get_breadcrumb(self):
        return [{'url': self.get_admin_url('index'), 'title': 'Accueil'},
                {'url': self.get_admin_url('liste_impression_examen'), 'title': 'Liste des impressions'}]

    @filter_hook
    def get_context(self):
        context = super(ListImpressionView, self).get_context()
        context['etapes'] = Etape.objects.by_centre_gestion('IED').order_by('cod_cur')
        return context

    @never_cache
    def get(self, request, *args, **kwargs):
        self.widgets = self.get_widgets()
        return self.template_response(self.base_template, self.get_context())


xadmin.site.register_view(r'^list_impression_examen/$', ListImpressionView, 'liste_impression_examen')


class ImpresssionCentre(PDFTemplateView):
    filename = "Etiquettes.pdf"
    template_name = "duck_examen/etiquette_centre.html"
    cmd_options = {
        'orientation': 'landscape',
    }

    def get_context_data(self, **kwargs):
        cod_etp = self.kwargs.get('cod_etp', None)
        session = self.kwargs.get('session', None)
        context = super(ImpresssionCentre, self).get_context_data(**kwargs)
        context['centres_gestions'] = ExamCenter.objects.get_by_cod_etp_by_session(cod_etp, session).order_by('country__lib_pay')
        context['nb_etiquette'] = [x for x in range(3)]

        return context


class ImpresssionRecap(PDFTemplateView):
    filename = "Etiquettes.pdf"
    template_name = "duck_examen/recapitulatif_session_centre.html"
    cmd_options = {
        'orientation': 'landscape',
    }

    def get_context_data(self, **kwargs):
        cod_etp = self.kwargs.get('cod_etp', None)
        session = self.kwargs.get('session', None)
        context = super(ImpresssionRecap, self).get_context_data(**kwargs)
        centres_gestions = ExamCenter.objects.get_by_cod_etp_by_session(cod_etp, session).order_by('country__lib_pay')
        context['label'] = 'Session {} {}'.format(session, cod_etp)
        context['nb_centre'] = centres_gestions.count()
        resultat = []
        for i, centre in enumerate(centres_gestions):
            resultat.append(
                {'numero': i + 1, 'label': centre.name_by_pays(), 'nb_etudiant': centre.nb_etudiant(cod_etp, int(session)),
                 'email': centre.email})
        context['centres'] = resultat

        return context

class PaysFilter(RelatedFieldListFilter):
    def choices(self):
        etp = self.request.GET.get('_p_cod_etp__in', None)
        if etp:
            self.lookup_choices = [(x.pk, x.lib_pay) for x in Pays.objects.filter(
                examcenter__rattachementcentreexamen__inscription__cod_etp=etp).order_by('lib_pay').distinct()]
        else:
            self.lookup_choices = [(x.pk, x.lib_pay) for x in
                                   Pays.objects.filter(examcenter__isnull=False).order_by('lib_pay').distinct()]
        return super(PaysFilter, self).choices()


class DomTomFilter(RelatedFieldListFilter):
    def choices(self):
        self.lookup_choices = [(x.pk, x.label) for x in
                               ExamCenter.objects.filter(has_incorporation=False).order_by('label').distinct()]
        return super(DomTomFilter, self).choices()


class RattachementCentreExamenAdmin(object):
    model = RattachementCentreExamen
    style = 'table'
    extra = 2
    max_num = 2

    @filter_hook
    def formfield_for_dbfield(self, db_field, **kwargs):
        # If it uses an intermediary model that isn't auto created, don't show
        # a field in admin.

        if isinstance(db_field, models.ManyToManyField) and not db_field.rel.through._meta.auto_created:
            return None
        attrs = self.get_field_attrs(db_field, **kwargs)
        if db_field.name == 'centre' and self.request.GET.get('incorporation', 0) == '1':
            query = ExamCenter.objects.filter(has_incorporation=False)
            for x in self.model_instance.rattachementcentreexamen_set.all():
                query = query | ExamCenter.objects.filter(pk=x.centre_id)
            return db_field.formfield(queryset=query, **dict(attrs, **kwargs))
        return db_field.formfield(**dict(attrs, **kwargs))


class EtapeExamenAdmin(object):
    inlines = [RattachementCentreExamenAdmin]
    list_filter = [('rattachementcentreexamen__centre__country', PaysFilter), 'cod_etp',
                   ('rattachementcentreexamen__centre', DomTomFilter), 'rattachementcentreexamen__session']

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
                                           'force_encaissement',
                                           css_class="unsort no_title"),
                                       horizontal=True, span=12)))

    def queryset(self):
        return EtapeExamen.inscrits_condi.all()

    @filter_hook
    def model_admin_url(self, name, *args, **kwargs):
        url = super(EtapeExamenAdmin, self).model_admin_url(name, *args, **kwargs)
        extention = '?incorporation={}'.format(self.request.GET.get('incorporation', 0))
        return url + extention

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