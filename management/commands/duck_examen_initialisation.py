from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django_apogee.models import Pays, Etape
from duck_examen.models import DeroulementExamenModel, RattachementCentreExamen, DetailDeroulement, \
    EtapeSettingsDerouleModel


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):

        # for centre in CentreGestionExamenInitial.objects.using('pal2').only('label',
        #                                                                     'adresse',
        #                                                                     'adresse_envoi_materiel',
        #                                                                     'nom',
        #                                                                     'prenom',
        #                                                                     'email',
        #                                                                     'email_bis',
        #                                                                     'telephone',
        #                                                                     'fax',
        #                                                                     'pays'):
        #     ExamCenter.objects.create(
        #         label=centre.label,
        #         mailling_address=centre.adresse,
        #         sending_address=centre.adresse_envoi_materiel,
        #         last_name_manager=centre.nom,
        #         first_name=centre.prenom,
        #         email=centre.email,
        #         email_bis=centre.email_bis,
        #         phone=centre.telephone,
        #         fax=centre.fax,
        #         country_id=centre.pays_id
        #     )
        # for centre in CentreGestionException.objects.using('pal2').all():
        #     ExamCenter.objects.create(
        #         label=centre.label,
        #         mailling_address=centre.adresse
        #         has_incorporation=False
        #     )
        # for d in DeroulementExamenModel.objects.using('pal2').all():
        #     d.save(using='default')
        # for x in RattachementCentreExamen.objects.all():
        #     x.save()
        # print 'fini'
        # for x in DeroulementExamenModel.objects.all():
        #     DetailDeroulement.objects.get_or_create(deroulement=x, deroulement_contenu=x.deroulement)
            # DetailDeroulement.objects.get_or_create(deroulement=x, deroulement_contenu=x.deroulement, type_examen_id='H')
        for x in Etape.objects.by_centre_gestion('IED'):
            a = EtapeSettingsDerouleModel.objects.get_or_create(etape=x, session=1, cod_anu=2015)[0]
            b = EtapeSettingsDerouleModel.objects.get_or_create(etape=x, session=2, cod_anu=2015)[0]
            if x.parcours_set.count():
                for p in x.parcours_set.all():
                    for derou in x.deroulementexamenmodel_set.filter(annee=2015):
                        DetailDeroulement.objects.get_or_create(parcours=p, deroulement=derou, amenagement_examen_id='N')
                        DetailDeroulement.objects.get_or_create(parcours=p, deroulement=derou, amenagement_examen_id='T')
        #     else:
        #         for derou in x.deroulementexamenmodel_set.filter(annee=2015):
        #             DetailDeroulement.objects.get_or_create(deroulement=derou, amenagement_examen_id='N')
        #             DetailDeroulement.objects.get_or_create(deroulement=derou, amenagement_examen_id='T')
        # # for x in EtapeSettingsDerouleModel.objects.all():
        #     x.save()
