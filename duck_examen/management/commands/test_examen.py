# coding=utf-8
from time import sleep
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from mailrobot.models import Mail
from django_apogee.models import Pays, InsAdmEtp, Etape
from duck_examen.models import DeroulementExamenModel, RattachementCentreExamen
from duck_utils.utils import make_pdf, get_recipients


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        template_mail = Mail.objects.get(name='mail_envoi_convocation')
        adresse = """
Université de Saint-Denis
<br> 2 rue de la Liberté
<br> 93200 – Saint-Denis
<br> (Métro Ligne n°13 – Station Saint-Denis Université)
        """
        for cod_etp in ['L2NPSY']:
            etape = Etape.objects.get(cod_etp=cod_etp).lib_etp
            deroule_sesion1 = DeroulementExamenModel.objects.get(etape__cod_etp=cod_etp, session=1)

            deroule_sesion2 = DeroulementExamenModel.objects.get(etape__cod_etp=cod_etp, session=2)
            deroule_anterieur_session_1 = deroule_sesion1.deroulement_etape_anterieur()
            deroule_anterieur_session_2 = deroule_sesion2.deroulement_etape_anterieur()
            if deroule_anterieur_session_1:
                etape_ant = deroule_anterieur_session_1.etape.lib_etp

            inscriptions = InsAdmEtp.inscrits.filter(cod_etp=cod_etp).first()
            i=0
            for ins in inscriptions:
                context = dict()
                context['ins'] = ins
                context['etape'] = etape
                context['etape_ant'] = etape_ant
                context['etape1'] = dict()
                context['etape2'] = dict()
                if deroule_anterieur_session_1:
                    context['etape_bis'] = deroule_anterieur_session_1

                for rattachement in ins.rattachementcentreexamen_set.all():
                    if rattachement.session == '1':
                        context['etape1']['salle1'] = rattachement.get_salle()
                        context['etape1']['adresse1'] = adresse if rattachement.centre.is_main_center else 'Voir centre'
                        context['etape2']['adresse1'] = adresse if rattachement.centre.is_main_center else 'Voir centre'
                        context['etape1']['date1'] = '\n'.join(self.get_dates(deroule_sesion1, rattachement))
                        if deroule_anterieur_session_1:
                            context['etape2']['date1'] = '\n'.join(self.get_dates(deroule_anterieur_session_1, rattachement))
                            context['etape2']['salle1'] = self.get_salles(deroule_anterieur_session_1, rattachement)
                    else:
                        context['etape1']['salle2'] = rattachement.get_salle()
                        context['etape1']['adresse2'] = adresse if rattachement.centre.is_main_center else 'Voir centre'
                        context['etape2']['adresse2'] = adresse if rattachement.centre.is_main_center else 'Voir centre'
                        context['etape1']['date2'] = '\n'.join(self.get_dates(deroule_sesion2, rattachement))
                        if deroule_anterieur_session_2:
                            context['etape2']['date2'] = '\n'.join(self.get_dates(deroule_anterieur_session_2, rattachement))
                            context['etape2']['salle2'] = self.get_salles(deroule_anterieur_session_2, rattachement)


                recipients = get_recipients(ins.cod_ind, ins.cod_anu)
                mail = template_mail.make_message(recipients=recipients)
                pdf = make_pdf("duck_examen/convocation_examen_bis.html", context)
                mail.attach(filename="convocation_{}.pdf".format(cod_etp),
                                content=pdf)
                mail.send()
                if i == 100:
                    sleep(1)
                    i = 0
                i += 1


    def get_dates(self, deroule, rattachement):
        d = deroule.get_deroulement_parse(rattachement.type_examen)
        return [date['date'] for date in d]

    def get_salles(self, deroule, rattachement):
        if rattachement.salle:
            return rattachement.salle.label
        elif not rattachement.centre.is_main_center:
            return "Voir le centre"
        else:
            return deroule.salle_examen