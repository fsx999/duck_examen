# -*- coding: utf8 -*-
import datetime
import os
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from mailrobot.models import Mail
from django_apogee.models import InsAdmEtp
from duck_examen.models import EtapeExamenModel, Etape, EtapeSettingsDerouleModel, DeroulementExamenModel, \
    RattachementCentreExamen
import mimetypes
from duck_utils.models import EtapeSettings, TemplateHtmlModel
from duck_utils.utils import get_recipients


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        today = datetime.date.today()
        template = TemplateHtmlModel.objects.get(name='convocation_examen')
        template_mail = Mail.objects.get(name='mail_envoi_convocation')
        for esd in EtapeSettingsDerouleModel.objects.filter(session='1',
                                                            envoi_convocation_processed=False,
                                                            date_envoi_convocation__gte=today):

            etape_settings = EtapeSettings.objects.get(etape=esd.etape, cod_anu=esd.cod_anu)
            deroules = {}
            for de in esd.etape.deroulementexamenmodel_set.all(): #DeroulementExamenModel.objects.filter(etape=esd.etape):
                deroules[de.session] = de.get_deroulement_detail(esd.type_examen)

            coordonnee_de_contact = etape_settings.contact_info
            debug_start = 0

            for inscription in InsAdmEtp.inscrits_condi.filter(cod_etp=esd.etape.cod_etp,
                                            rattachementcentreexamen__type_examen=esd.type_examen,
                                            cod_anu=esd.cod_anu,
                                            rattachementcentreexamen__isnull=False).distinct():

                recipients = get_recipients(inscription.cod_ind, inscription.cod_anu)
                mail = template_mail.make_message(recipients=recipients)
                for r in inscription.rattachementcentreexamen_set.all():
                    context = {
                        'annee': today.year - 1,
                        'session': r.session,
                        'coordonnee_de_contact': coordonnee_de_contact,
                        'inscription': inscription,
                        'jours': ", ".join(deroules[r.session].get_jours()),
                        'salles': r.get_salle(),
                        'deroule': deroules[r.session].deroulement_parse(),
                        'centre': r.centre.label
                    }
                    pdf = template.get_pdf_file(context)
                    mail.attach(filename="convocation_{}.pdf".format(r.session),
                                content=pdf)
                mail.send()
                if settings.DEBUG: # On envoit 10 mails au max en debug
                    debug_start += 1
                    if debug_start == 10:
                        break
