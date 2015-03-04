from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django_apogee.models import Pays, InsAdmEtp
from duck_examen.models import DeroulementExamenModel, RattachementCentreExamen
from duck_examen.utils import get_etudiant_pagine


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        from duck_examen.models import EtapeExamenModel

        # get_etudiant_pagine(EtapeExamen.objects.get_etudiant_presentiel(session_1), nb_salle, nb_table)
        ## get_etudiant_pagine(mon_etape.get_etudiant_presentiel(session_1), nb_salle, nb_table)
        # mom_etape.get_etudiant_presentiel_pagine(session1, nb_salle, nb_table)
        # print "Coucou", EtapeExamenModel.objects.all()[0].get_etudiant_presentiel
        #InsAdmEtp.inscrits.first().save()
        # for i in InsAdmEtp.inscrits.all():
        #     i.save()
        etape = EtapeExamenModel.objects.get(cod_etp='L1NPSY')
        l = get_etudiant_pagine(etape.get_etudiant_presentiel(1), nb_amphi=3, nb_table=3)
        print l[0].object_list