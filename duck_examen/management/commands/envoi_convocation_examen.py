# -*- coding: utf8 -*-
import datetime
import os
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from duck_examen.models import EtapeExamenModel, Etape, EtapeSettingsDerouleModel
import mimetypes

class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):

        today = datetime.date.today()
        for i in EtapeSettingsDerouleModel.objects.all():
            if (i.date_envoi_convocation and
                i.date_envoi_convocation >= datetime.date.today() and
                i.envoi_convocation_processed is False):
                recipients = [e.cod_ind.get_email(i.cod_anu)
                              for e in EtapeExamenModel.objects.get(cod_etp=i.etape.cod_etp).get_etudiant_presentiel(i.session).filter(rattachementcentreexamen__type_examen=i.type_examen)]
                body = u"Vous trouverez en pièce jointe les informations relatives à votre convocation."
                attachment1 = {'name': None,
                               'content': None,
                               'mimetype': None}
                attachment2 = {'name': os.path.basename(i.deroule.path),
                               'content': None,
                               'mimetype': mimetypes.guess_type(i.deroule.path)}
                with open(i.deroule.path, 'r') as f:
                    attachment2['context'] = f.read()

               # print attachment1, attachment2
                print i.deroule.url
                print recipients
                for r in recipients:
                    if settings.DEBUG:
                        r = settings.EMAIL_DEV

                    mail = EmailMessage(subject="Convocation examen", body=body,
                                        from_email="nepasrepondre@iedparis8.net",
                                        to=(r,))


                # i.envoi_convocation_processed = True
                # i.save()

        # for i in EtapeSettingsDerouleModel.objects.all():
        #     for e in EtapeExamenModel.objects.get(cod_etp=i.etape.cod_etp).get_etudiant_presentiel(i.session):
        #         print e.cod_ind.get_email(i.cod_anu)
