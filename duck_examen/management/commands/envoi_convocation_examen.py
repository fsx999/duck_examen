# -*- coding: utf8 -*-
import datetime
import os
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from duck_examen.models import EtapeExamenModel, Etape, EtapeSettingsDerouleModel, DeroulementExamenModel, \
    RattachementCentreExamen
import mimetypes
from duck_utils.models import EtapeSettings


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        # il faut générer le template duck_examen/templates/duck_examen/convocation_examen.html
        # il faut recuper les données necessaire pour le template.
        # le fonctionnement :
        # c'est la même convocation pour la session 1 et 2 (on en envoie qu'une en fait)
        # pour cela
        #
        # today = datetime.date.today()
        #
        # for etape in Etape.objects.by_centre_gestion('IED').filter(deroulementexamenmodel__deroulement__isnull=False): # Pour toute les étapes de l'ied qui ont un déroule (donc droit, psycho, desu)
        #     deroule1 =
        #     deroule2 =
        #     # pour chaque étape il faut recuper les variable pour le context (voir le template)
        #     # for e in EtapeExamenModel.objects.get(cod_etp=etape.cod_etp).get_etudiant_presentiel(1).filter(rattachementcentreexamen__type_examen=i.type_examen):
        # for i in EtapeSettingsDerouleModel.objects.all():
        #     if (i.date_envoi_convocation and
        #         i.date_envoi_convocation >= datetime.date.today() and
        #         i.envoi_convocation_processed is False):
        #         # recipients = [e.cod_ind.get_email(i.cod_anu)
        #         deroulement = i.get_deroulement()
        #         deroulement_parse = i.get_deroulement_parse()
        #         for e in EtapeExamenModel.objects.get(cod_etp=i.etape.cod_etp).get_etudiant_presentiel(i.session).filter(rattachementcentreexamen__type_examen=i.type_examen):
        #             body = u"Vous trouverez en pièce jointe les informations relatives à votre convocation."
        #
        #

        from pprint import pprint
        today = datetime.date.today()
        for esd in EtapeSettingsDerouleModel.objects.filter(session='1',
                                                            envoi_convocation_processed=False,
                                                            date_envoi_convocation__gte=today):

            etape_settings = EtapeSettings.objects.get(etape=esd.etape, cod_anu=esd.cod_anu).contact_info
            deroules = {}
            etudiants = {}
            for de in esd.etape.deroulementexamenmodel_set.all(): #DeroulementExamenModel.objects.filter(etape=esd.etape):
                deroules[de.session] = de.get_deroulement_detail(esd.type_examen)

            coordonnee_de_contact = etape_settings.contact_info
            for r in RattachementCentreExamen.objects.filter(inscription__cod_etp=esd.etape.cod_etp,
                                                             type_examen=esd.type_examen,
                                                             inscription__cod_anu=esd.cod_anu):
                for i in ['1', '2']:
                    context = {
                        'session': i,
                        'coordonnee_de_contact': coordonnee_de_contact,
                        'inscription': r.inscription,
                        'jours': deroules[i].get_jours(),
                        'salles': r.get_salle()
                    }





                if not etudiants.get(r.inscription):
                    etudiants[r.inscription] = {}
                etudiants[r.inscription][r.session] = r

            pprint(deroules)
            # pprint(etudiants)

            for e in etudiants:
                context = {'coordonnee_de_contact': EtapeSettings.objects.get(etape=esd.etape,
                                                                              cod_anu=esd.cod_anu).contact_info,
                           'individu': e,
                           'jours1': deroules['1'].get_jours(),
                           'salle1': etudiants[e]['1'].get_salle(),
                           'jours2': deroules['2'].get_jours(),
                           'salle2': etudiants[e]['2'].get_salle()}

        #     #pprint(deroules)
