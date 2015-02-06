from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django_apogee.models import Pays
from duck_examen.models import CentreGestionExamenInitial, ExamCenter, CentreGestionException


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):

        for centre in CentreGestionExamenInitial.objects.using('pal2').only('label',
                                                                            'adresse',
                                                                            'adresse_envoi_materiel',
                                                                            'nom',
                                                                            'prenom',
                                                                            'email',
                                                                            'email_bis',
                                                                            'telephone',
                                                                            'fax',
                                                                            'pays'):
            ExamCenter.objects.create(
                label=centre.label,
                mailling_address=centre.adresse,
                sending_address=centre.adresse_envoi_materiel,
                last_name_manager=centre.nom,
                first_name=centre.prenom,
                email=centre.email,
                email_bis=centre.email_bis,
                phone=centre.telephone,
                fax=centre.fax,
                country_id=centre.pays_id
            )
        for centre in CentreGestionException.objects.using('pal2').all():
            ExamCenter.objects.create(
                label=centre.label,
                mailling_address=centre.adresse,
                has_incorporation=False
            )
        print 'fini'
