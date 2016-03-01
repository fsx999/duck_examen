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
    help = "TEST envoi une convocation à un seul étudiant ou plusieurs nominativement TEST"

    #   args = numeros etudiants
    #   options pourraient servir à differencier les informations transmises en args: numero etudiant, numero de dossier, code etape, etc

    def handle(self, *args, **options):
        today = datetime.date.today()
        template = TemplateHtmlModel.objects.get(name='convocation_examen')
        template_mail = Mail.objects.get(name='mail_envoi_convocation')
        deroules = {}
        for code_individu in args:

            for inscription in InsAdmEtp.inscrits_condi.filter(cod_ind__cod_etu=code_individu,
                                                                        ).distinct():
                recipients = get_recipients(inscription.cod_ind, inscription.cod_anu)
                rattachement = RattachementCentreExamen.objects.filter(inscription=inscription)
                deroulement = DeroulementExamenModel.objects.filter(etape__cod_etp=inscription.cod_etp)

                for de in deroulement.etape.deroulementexamenmodel_set.all(): #DeroulementExamenModel.objects.filter(etape=esd.etape):
                    deroules[de.session] = de.get_deroulement_detail(rattachement.type_amenagement, rattachement.parcours)

                    etape_settings = EtapeSettings.objects.get(etape=inscription.etape, cod_anu=inscription.cod_anu)
                    coordonnee_de_contact = etape_settings.contact_info

                    debug_start = 0

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





