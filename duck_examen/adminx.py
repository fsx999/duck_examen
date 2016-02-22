# coding=utf-8
import datetime
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from wkhtmltopdf.views import PDFTemplateView
from django_apogee.models import Pays, Etape
from duck_examen.forms import EnvoiEMailCenterViewForm
from duck_examen.models import EtapeExamen, RattachementCentreExamen, ExamCenter, DeroulementExamenModel, \
    RecapitulatifExamenModel, EtapeExamenModel, DetailDeroulement, TypeExamen, EtapeSettingsDerouleModel, Parcours, \
    AmenagementExamenModel
from duck_examen.utils import get_etudiant_pagine
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
        etapes = []
        for etape in Etape.objects.by_centre_gestion('IED').order_by('cod_cur'):
            try:
                etape.types_examen_1 = etape.deroulementexamenmodel_set.get(annee=2015, session=1).derouler_par_parcours()
                etape.types_examen_2 = etape.deroulementexamenmodel_set.get(annee=2015, session=2).derouler_par_parcours()
            except DeroulementExamenModel.DoesNotExist:
                pass

            etapes.append(etape)
        context['etapes'] = etapes

        return context

    @never_cache
    def get(self, request, *args, **kwargs):
        self.widgets = self.get_widgets()
        return self.template_response(self.base_template, self.get_context())


xadmin.site.register_view(r'^list_impression_examen/$', ListImpressionView, 'liste_impression_examen')


class ImpresssionCentre(PDFTemplateView):
    filename = "Etiquettes_{}_{}.pdf"
    template_name = "duck_examen/etiquette_centre.html"
    cmd_options = {
        'orientation': 'landscape',
    }

    def get_filename(self):
        return self.filename.format(self.kwargs.get('cod_etp', 'Anomalie'), self.kwargs.get('session', 'Anomalie'))

    def get_context_data(self, **kwargs):
        cod_etp = self.kwargs.get('cod_etp', None)
        session = self.kwargs.get('session', None)
        context = super(ImpresssionCentre, self).get_context_data(**kwargs)
        context['centres_gestions'] = ExamCenter.objects.get_incorporation_by_cod_etp_by_session(cod_etp, session).order_by('country__lib_pay')
        context['nb_etiquette'] = [x for x in range(3)]

        return context


class ImpresssionRecap(PDFTemplateView):
    filename = "RecapExamen_{}_{}.pdf"
    template_name = "duck_examen/recapitulatif_session_centre.html"
    cmd_options = {
        'orientation': 'landscape',
    }

    def get_filename(self):
        return self.filename.format(self.kwargs.get('cod_etp', 'Anomalie'), self.kwargs.get('session', 'Anomalie'))

    def get_context_data(self, **kwargs):
        cod_etp = self.kwargs.get('cod_etp', None)
        session = self.kwargs.get('session', None)
        context = super(ImpresssionRecap, self).get_context_data(**kwargs)
        centres_gestions = ExamCenter.objects.get_incorporation_by_cod_etp_by_session(cod_etp, session).order_by('country__lib_pay')
        context['label'] = 'Session {} {}'.format(session, cod_etp)
        context['nb_centre'] = centres_gestions.count()
        resultat = []
        for i, centre in enumerate(centres_gestions):
            resultat.append(
                {'numero': i + 1, 'label': centre.name_by_pays(), 'nb_etudiant': centre.nb_etudiant(cod_etp, int(session)),
                 'email': centre.email})
        context['centres'] = resultat

        return context


class ImpressionEmargement(PDFTemplateView):
    filename = "emargement_{}_{}_{}.pdf"
    template_name = "duck_examen/liste_emargement.html"
    cmd_options = {
        'orientation': 'landscape',
        'page-size': 'A3'
    }
    type = {
        'E': 'etranger',
        'P': 'presentiel',
        'A': 'autre'
    }

    def get_filename(self):
        return self.filename.format(self.kwargs.get('cod_etp', 'Anomalie'), self.kwargs.get('session', 'Anomalie'),
                                     self.type[self.kwargs.get('type', None)])

    def etranger(self, cod_etp, session, parcours):
        return ExamCenter.objects.get_incorporation_by_cod_etp_by_session(
            cod_etp=cod_etp,
            session=session,
            parcours=parcours).order_by('country__lib_pay')

    def autre(self, cod_etp, session, parcours):
        return ExamCenter.objects.get_autre_by_cod_etp_by_session(cod_etp=cod_etp, session=session, parcours=parcours)

    def presentiel(self, cod_etp, session, type_examen):
        etape = EtapeExamenModel.objects.get(cod_etp=cod_etp)
        return get_etudiant_pagine(etape.get_etudiant_presentiel(session, type_examen), nb_amphi=3, nb_table=3)

    def get_context_data(self, **kwargs):
        cod_etp = self.kwargs.get('cod_etp', None)
        session = self.kwargs.get('session', None)
        type = self.kwargs.get('type', None)
        pk = self.kwargs.get('pk')
        context = super(ImpressionEmargement, self).get_context_data(**kwargs)
        f_centre_examen = getattr(self, self.type[type])
        deroulement = DetailDeroulement.objects.get(pk=pk)
        context['deroulements'] = deroulement.deroulement_parse2()
        nb_matiere = 0
        for jour in context['deroulements']:
            nb_matiere += len(jour['matieres'])
        context['nb_matiere'] = [0] * nb_matiere

        if type != 'P':

            centres_gestions = f_centre_examen(cod_etp, session, parcours=deroulement.parcours)

            for centre in centres_gestions:

                centre.etudiants = centre.etudiant_by_step_session(cod_etp, session)
                centre.nb_etudiant = centre.etudiants.count()
                centre.nb_ligne_vide = [nb + centre.nb_etudiant + 1 for nb in range(15-centre.nb_etudiant)]
            context['centres'] = centres_gestions

        else: # if type == 'P'
            etape = EtapeExamenModel.objects.get(cod_etp=cod_etp)
            self.template_name = "duck_examen/liste_emargement_presentiel.html"
            if deroulement.amenagement_examen.type_amenagement == 'T':
                context['pages'] = get_etudiant_pagine(etape.get_etudiant_presentiel(session, deroulement.amenagement_examen),
                                                   nb_amphi=1, nb_table=1)
            else:
                context['pages'] = get_etudiant_pagine(etape.get_etudiant_presentiel(session, deroulement.amenagement_examen),
                                                       nb_amphi=deroulement.deroulement.nb_salle,
                                                       nb_table=deroulement.deroulement.nb_table)

        context['session'] = session
        context['label'] = Etape.objects.get(cod_etp=cod_etp).lib_etp

        return context


class ImpressionEtiquetteEnveloppe(ImpressionEmargement):
    filename = "impression_centre_{}_{}_{}.pdf"
    template_name = "duck_examen/etiquette_envoi_centre.html"


class ImpressionPv(ImpressionEtiquetteEnveloppe):
    filename = "impression_centre_{}_{}_{}.pdf"
    template_name = "duck_examen/pv_centre.html"
    cmd_options = {
    }
    def get_context_data(self, **kwargs):
        cod_etp = self.kwargs.get('cod_etp', None)
        session = self.kwargs.get('session', None)
        type = self.kwargs.get('type', None)
        type_examen = self.kwargs.get('type_examen', 'D')
        context = super(ImpressionEmargement, self).get_context_data(**kwargs)

        centres_gestions = getattr(self, self.type[type])(cod_etp, session, type_examen)
        # try:
        deroulement = DeroulementExamenModel.objects.get(etape__cod_etp=cod_etp, session=session)
        context['deroulements'] = deroulement.get_deroulement_parse(TypeExamen.objects.get(name=type_examen))
        # except IndexError:
        #     pass
        nb_matiere = 0
        for jour in context['deroulements']:
            nb_matiere += len(jour['matieres'])
        context['nb_matiere'] = [0] * nb_matiere

        if type != 'P':
            for centre in centres_gestions:

                centre.etudiants = centre.etudiant_by_step_session(cod_etp, session, type_examen)
                centre.nb_etudiant = centre.etudiants.count()
                centre.nb_ligne_vide = [nb + centre.nb_etudiant + 1 for nb in range(15-centre.nb_etudiant)]
            context['centres'] = centres_gestions

        else: # if type == 'P'
            etape = EtapeExamenModel.objects.get(cod_etp=cod_etp)
            centre = ExamCenter.objects.get(is_main_center=True)
            centre.nb_etudiant = centre.etudiant_by_step_session(cod_etp, session, type_examen).count()
            context['centres'] = [centre]
            if type_examen == 'H':
                context['pages'] = get_etudiant_pagine(etape.get_etudiant_presentiel(session, type_examen),
                                                   nb_amphi=1, nb_table=1)
            else:
                context['pages'] = get_etudiant_pagine(etape.get_etudiant_presentiel(session, type_examen),
                                                   nb_amphi=deroulement.nb_salle, nb_table=deroulement.nb_table)

        context['session'] = session
        context['label'] = Etape.objects.get(cod_etp=cod_etp).lib_etp

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

    #exclude = ['type_examen',] # Etre sur qu'il est bien devenu inutile

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
        if db_field.name == 'type_examen':
            type_examen = EtapeSettingsDerouleModel.objects.filter(etape__cod_etp=self.org_obj.cod_etp).distinct('type_examen').values_list('type_examen', flat=True)
            query = TypeExamen.objects.filter(name__in=type_examen)
            return db_field.formfield(queryset=query,  **dict(attrs, **kwargs))
        if db_field.name == 'parcours':
            query=Parcours.objects.filter(etape__cod_etp=self.org_obj.cod_etp)
            return db_field.formfield(queryset=query,  **dict(attrs, **kwargs))

        return db_field.formfield(**dict(attrs, **kwargs))

    @property
    def exclude(self):
        exclude = ['type_examen']
        if not Parcours.objects.filter(etape__cod_etp=self.org_obj.cod_etp).count():
            return exclude + ['parcours']
        else:
            return exclude


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
        query = EtapeExamen.inscrits_condi.all()
        if not self.user.is_superuser:
            return query.filter(cod_etp__in=self.user.setting_user.etapes.values_list('cod_etp', flat=True))
        return query

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


class DetailDeroulementAdmin(object):
    model = DetailDeroulement
    extra = 0
    # readonly_fields = ['type_examen']

    @property
    def exclude(self):
        exclude = []
        if not Parcours.objects.filter(etape__cod_etp=self.org_obj.etape.cod_etp).count():
            return exclude + ['parcours']
        else:
            return exclude


    @filter_hook
    def formfield_for_dbfield(self, db_field, **kwargs):
        attrs = self.get_field_attrs(db_field, **kwargs)
        if db_field.name == 'parcours':
            query=Parcours.objects.filter(etape__cod_etp=self.org_obj.etape.cod_etp)
            return db_field.formfield(queryset=query,  **dict(attrs, **kwargs))
        return db_field.formfield(**dict(attrs, **kwargs))

class DeroulementAdmin(object):
    hidden_menu = True
    # readonly_fields = ['etape', 'session']
    form_layout = Layout(Container(Col('full',
                                       Fieldset(
                                           "",
                                           'etape', 'session', 'annee',
                                           'nb_salle', 'nb_table',
                                           'date_examen',
                                           'salle_examen',
                                           css_class="unsort no_title"),
                                       horizontal=True, span=12)))
    inlines = [DetailDeroulementAdmin]

    @filter_hook
    def get_readonly_fields(self):
        if self.user.is_superuser:
            return []
        else:
            return self.readonly_fields

    @filter_hook
    def get_list_queryset(self):
        query = super(DeroulementAdmin, self).get_list_queryset()
        if not self.user.is_superuser:
            query = query.filter(etape__in=self.user.setting_user.etapes.all())
        return query


class EnvoiEMailCenterView(views.FormAdminView):
    form = EnvoiEMailCenterViewForm
    title = 'Envoi email centre examen'

    def get_redirect_url(self):
        return self.get_admin_url('envoi_email_center')

    def post(self, request, *args, **kwargs):
        self.instance_forms()
        self.setup_forms()
        if self.valid_forms():
            data = self.form_obj.cleaned_data
            exam_centers = ExamCenter.objects.get_incorporation_by_cod_etp_by_session(data['etape'].cod_etp, data['session'])
            if not exam_centers:
                self.message_user('Il n\'y a pas de centre pour cette étape.', 'error')
                return self.get_response()

            if exam_centers.filter(email__isnull=True).exists():
                msg = ''
                for center in exam_centers.filter(email__isnull=True):
                    msg += "Le centre {} n'a pas d'email. <br />".format(center.label)
                self.message_user(msg, 'error')
                return self.get_response()

            idx = 0
            if data['attachment']:
                name = data['attachment'].name
                content = data['attachment'].read()
                mimetype = data['attachment'].content_type
            for center in exam_centers:

                if settings.DEBUG:
                    recipients = (settings.EMAIL_DEV,)
                else:
                    if center.email:
                        recipients = (center.email,)
                    elif center.email_bis:
                        recipients = (center.email_bis,)

                mail = EmailMessage(subject=data['subject'], body=data['text'],
                                    from_email='nepasrepondre@iedparis8.net',
                                    to=recipients, bcc=['examens@iedparis8.net'])
                if data['attachment']:
                    mail.attach(filename=name,
                                content=content,
                                mimetype=mimetype)

                mail.send()
                if settings.DEBUG: # we send at most 5 mail
                    if idx == 5:
                        break
                    else:
                        idx += 1


            self.message_user('Email envoyé.', 'success')
            return HttpResponseRedirect(self.get_redirect_url())

        return self.get_response()

    def get_context(self):
        context = super(EnvoiEMailCenterView, self).get_context()
        context['has_file_field'] = True
        return context

xadmin.site.register_view(r'^examen/mail/$', EnvoiEMailCenterView, 'envoi_email_center')


def date_envoi(modeladmin, request, queryset):
    queryset.update(date_envoie=datetime.date.today())
date_envoi.short_description = "Valider la date d'envoi"


def date_reception(modeladmin, request, queryset):
    queryset.update(date_reception=datetime.date.today())
date_reception.short_description = "Valider la date de reception"


class EtapeFilter(RelatedFieldListFilter):
    def choices(self):
        self.lookup_choices = [(x.pk, x.lib_etp) for x in Etape.objects.by_centre_gestion('IED').all().order_by('lib_etp')]
        return super(EtapeFilter, self).choices()


class RecapitulatifExamenAdmin(object):
    hidden_menu = True
    actions = [date_envoi, date_reception]
    list_filter = [('etape', EtapeFilter), 'session']
    list_display = ('__str__', 'date_envoie', 'date_reception', 'nb_enveloppe', 'nb_colis', 'anomalie')
    list_editable = ('nb_enveloppe', 'anomalie', 'date_envoie', 'nb_colis')
    list_per_page = 20
    readonly_fields = ['etape', 'session', 'centre']
    remove_permissions = ['delete', 'add']
    show_bookmarks = False


class EtapeSettingsDerouleModelAdmin(object):
    list_filter = [('etape', EtapeFilter), 'session']

    def queryset(self):
        qs = super(EtapeSettingsDerouleModelAdmin, self).queryset().filter(cod_anu=2015)
        if not self.user.is_superuser:
            qs = qs.filter(etape__in=self.user.setting_user.etapes.all())

        return qs

    @filter_hook
    def get_field_attrs(self, db_field, **kwargs):
        if db_field.name == 'etape':
            return {'queryset': Etape.objects.by_centre_gestion('IED')}
        return super(EtapeSettingsDerouleModelAdmin, self).get_field_attrs(db_field, **kwargs)

    def get_readonly_fields(self):
        if self.user.is_superuser:
            return []

        return ['etape', 'cod_anu', 'type_examen', 'session', 'envoi_convocation_processed']

xadmin.site.register(EtapeSettingsDerouleModel, EtapeSettingsDerouleModelAdmin)
xadmin.site.register(EtapeExamen, EtapeExamenAdmin)
xadmin.site.register(ExamCenter, ExamenCenterAdmin)
xadmin.site.register(DeroulementExamenModel, DeroulementAdmin)
xadmin.site.register(RecapitulatifExamenModel, RecapitulatifExamenAdmin)
xadmin.site.register(TypeExamen)


class ExamentDashboard(views.Dashboard):
    base_template = "duck_examen/examen_dashboard.html"
    widget_customiz = False

    def get_context(self):
        context = super(ExamentDashboard, self).get_context()
        return context

    @filter_hook
    def get_breadcrumb(self):
        return [{'url': self.get_admin_url('index'), 'title': 'Accueil'},]

    @never_cache
    def get(self, request, *args, **kwargs):
        self.widgets = self.get_widgets()
        return self.template_response(self.base_template, self.get_context())

xadmin.site.register_view(r'^examens/$', ExamentDashboard, 'examens_dashboard')

class ParcoursAdmin(object):
    @filter_hook
    def formfield_for_dbfield(self, db_field, **kwargs):
        attrs = self.get_field_attrs(db_field, **kwargs)
        if db_field.name == 'etape':
            query = Etape.objects.filter(etpgerercge__cod_cmp='034').order_by('cod_etp')
            return db_field.formfield(queryset=query,  **dict(attrs, **kwargs))

        return db_field.formfield(**dict(attrs, **kwargs))

xadmin.site.register(Parcours, ParcoursAdmin)
