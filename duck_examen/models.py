# coding=utf-8
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.db import models
from django_apogee.models import Pays, InsAdmEtp
# from apogee.models import Pays, INS_ADM_ETP_IED
# from core.managers.managers_examen import EtapeExamenManager
# from core.utils import paginator_etudiant



class EtapeExamen(InsAdmEtp):
    class Meta:
        proxy = True
        verbose_name = 'Etape examen'


@python_2_unicode_compatible
class ExamCenter(models.Model):
    u"""
    Centre de gestion : Présentiel, etranger et dom-tom
    is_open : ouvre à l'application
    has_demande_ratachement : pour les examens à l'etranger true
    is_centre_principal : indique les centres métropolitains
    """
    label = models.CharField("center name", max_length=200, null=True)
    mailling_address = models.TextField("Adresse du centre")
    sending_address = models.TextField(u"Adresse de l'envoi du matériel", blank=True, null=True)
    last_name_manager = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email_bis = models.EmailField(null=True, blank=True, verbose_name="second email")
    phone = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, null=True, blank=True)
    country = models.ForeignKey(Pays, verbose_name="pays", null=True)

    is_open = models.BooleanField(default=True, verbose_name='Ouvert')
    has_incorporation = models.BooleanField(default=True, verbose_name="Demande rattachement",
                                            help_text=u"l'étudiant doit faire une demande de rattachement")
    is_main_center = models.BooleanField(default=False)

    # @property
    # def adresse_envoi_html(self):
    #     return ''.join([x+'<br>' for x in self.adresse_envoi_materiel.splitlines()])[:-4]

    class Meta:
        verbose_name = "Centre examen"
        verbose_name_plural = "Centres examens"
        # ordering = ['pays__lib_pay']

    def __str__(self):
        return u"{} {}".format(smart_text(self.label), self.country)

    # def name_by_pays(self):
#         return u"{} {}".format(self.pays, smart_text(self.label))
#
#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#         if not self.adresse_envoi_materiel:
#             self.adresse_envoi_materiel = self.adresse
#
#         super(CentreGestionExamen, self).save(force_insert, force_update, using, update_fields)
#
#     def etudiant_by_step_session(self, step, session):
#         query = self.etudiantcentreexamen_set.filter(inscription__COD_ETP=step, session=session)
#         if step[0] == 'L' and int(step[1]) < 3:
#             code_etp = step[0] + str(int(step[1]) + 1) + step[2:]
#             query |= self.etudiantcentreexamen_set.filter(inscription__COD_ETP=code_etp,
#                                                           session=session,
#                                                           ec_manquant=True)
#         return query.order_by('inscription__COD_IND__LIB_NOM_PAT_IND').distinct()
#
#     def nb_etudiant(self, step, session):
#         return self.etudiant_by_step_session(step, session).count()
#
#



class RattachementCentreExamen(models.Model):
    inscription = models.ForeignKey(InsAdmEtp)
    session = models.CharField(max_length=2, choices=(('1', 'Première session'), ('2', 'Seconde session')))
    centre = models.ForeignKey(ExamCenter)
    ec_manquant = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return u"{} session : {} ec manquant : {}".format(self.centre, self.session, "oui" if self.ec_manquant else 'non')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.ec_manquant:
            code_etp_actuel = self.inscription.cod_etp
            if code_etp_actuel[0] == 'L' and code_etp_actuel != 'L3NEDU':
                if code_etp_actuel[1] in ['2', '3']:
                    code_etp_anterieur = code_etp_actuel[0] + str(int(code_etp_actuel[1]) - 1) + code_etp_actuel[2:]
                    cod_ind = self.inscription.cod_ind
                    etp = InsAdmEtp.inscrits_condi.filter(cod_ind=cod_ind, cod_etp=code_etp_anterieur).first()
                    if etp:
                        RattachementCentreExamen.objects.get_or_create(inscription=etp, session=self.session, centre=self.centre)

        super(RattachementCentreExamen, self).save(force_insert, force_update, using, update_fields)


# @python_2_unicode_compatible
# class CentreGestionException(models.Model):
#     label = models.CharField("Nom du centre", max_length=200, null=True)
#     adresse = models.TextField("Adresse du centre", null=True, blank=True)
#
#     class Meta:
#         verbose_name = "Centre autre"
#         verbose_name_plural = "Centres autres"
#         db_table = 'core_centregestionexception'
#
#     def __str__(self):
#         return "{}".format(self.label)
# # #
#
# @python_2_unicode_compatible
# class EtudiantCentreExamen(models.Model):
#     inscription = models.ForeignKey(INS_ADM_ETP_IED)
#     session = models.CharField(max_length=2, choices=(('1', 'Première session'), ('2', 'Seconde session')))
#     centre = models.ForeignKey(CentreGestionExamen)
#     ec_manquant = models.BooleanField(default=False, blank=True)
#
#     def get_label_dict(self):
#         return {
#             'nom': self.inscription.COD_IND.LIB_NOM_PAT_IND,
#             'epoux': self.inscription.COD_IND.LIB_NOM_USU_IND,
#             'prenom': self.inscription.COD_IND.LIB_PR1_IND,
#             'num_etu': self.inscription.COD_IND.COD_ETU
#         }
#
#     class Meta:
#         app_label = 'core'
#         ordering = ['inscription__COD_IND__LIB_NOM_PAT_IND']
#
#     def __str__(self):
#         return "{} {} {}".format(self.inscription, self.session, self.centre)
#
#
# @python_2_unicode_compatible
# class EtudiantCentreExamenException(models.Model):
#     inscription = models.ForeignKey(INS_ADM_ETP_IED)
#     session = models.CharField(max_length=2, choices=(('1', 'Première session'), ('2', 'Seconde session')))
#     centre = models.ForeignKey(CentreGestionException)
#     ec_manquant = models.BooleanField(default=False, blank=True)
#
#     class Meta:
#         app_label = 'core'

#     def get_label_dict(self):
#         return {
#             'nom': self.inscription.COD_IND.LIB_NOM_PAT_IND,
#             'epoux': self.inscription.COD_IND.LIB_NOM_USU_IND,
#             'prenom': self.inscription.COD_IND.LIB_PR1_IND,
#             'num_etu': self.inscription.COD_IND.COD_ETU
#         }
#
#     def __str__(self):
#         return "{} {} {}".format(self.inscription, self.session, self.centre)
#
#
# @python_2_unicode_compatible
# class Inscription(INS_ADM_ETP_IED):
#
#     def _label(self):
#         return "{} {} {}".format(self.COD_IND.COD_ETU, self.COD_IND.LIB_NOM_PAT_IND, self.COD_IND.LIB_PR1_IND)
#     _label.allow_tags = True
#     _label.short_description = "Identité"
#
#     label = property(_label)
#
#     class Meta:
#         app_label = 'core'
#         proxy = True
#
#     def __str__(self):
#         label = "{} {} {}".format(self.COD_IND.COD_ETU, self.COD_IND.LIB_NOM_PAT_IND, self.COD_IND.LIB_PR1_IND)
#         for e in self.etudiantcentreexamen_set.all().order_by('session'):
#             label += ' {} : {} ,'.format(e.session, e.centre)
#         return label
#
#
# @python_2_unicode_compatible
# class InscriptionException(INS_ADM_ETP_IED):
#
#     def _label(self):
#
#         return "{} {} {}".format(self.COD_IND.COD_ETU, self.COD_IND.LIB_NOM_PAT_IND, self.COD_IND.LIB_PR1_IND)
#     _label.allow_tags = True
#     _label.short_description = "Identité"
#
#     label = property(_label)
#
#     class Meta:
#         app_label = 'core'
#         proxy = True
#
#     def __str__(self):
#         label = "{} {} {}".format(self.COD_IND.COD_ETU, self.COD_IND.LIB_NOM_PAT_IND, self.COD_IND.LIB_PR1_IND)
#         for e in self.etudiantcentreexamen_set.all().order_by('session'):
#             label += ' {} : {} ,'.format(e.session, e.centre)
#         return label
#
#
# class EtapeExamenModel(Etape):
#     """
#     utiliser pour les examen
#     """
#     objects = EtapeExamenManager()
#
#     def get_centre_exament_etranger(self):
#
#         query = CentreGestionExamen.objects.filter(etudiantcentreexamen__inscription__COD_ETP=self.cod_etp)
#         if self.cod_etp[0] == 'L' and int(self.cod_etp[1]) < 3:
#             code_etp = self.cod_etp[0] + str(int(self.cod_etp[1]) + 1) + self.cod_etp[2:]
#             query |= CentreGestionExamen.objects.filter(etudiantcentreexamen__inscription__COD_ETP=code_etp,
#                                                         etudiantcentreexamen__ec_manquant=True)
#         return query.distinct()
#
#     def get_centre(self, session):
#         query = CentreGestionExamen.objects.filter(etudiantcentreexamen__inscription__COD_ETP=self.cod_etp,
#                                                    etudiantcentreexamen__session=session)
#         if self.cod_etp[0] == 'L' and int(self.cod_etp[1]) < 3:
#             code_etp = self.cod_etp[0] + str(int(self.cod_etp[1]) + 1) + self.cod_etp[2:]
#             query |= CentreGestionExamen.objects.filter(etudiantcentreexamen__inscription__COD_ETP=code_etp,
#                                                         etudiantcentreexamen__ec_manquant=True,
#                                                         etudiantcentreexamen__session=session)
#         return query.distinct()
#
#     def get_centre_premier_session(self):
#         return self.get_centre(1)
#
#     def get_centre_deuxieme_session(self):
#         return self.get_centre(2)
#
#     def get_centre_exception(self, session):
#         query = CentreGestionException.objects.filter(etudiantcentreexamenexception__inscription__COD_ETP=self.cod_etp,
#                                                       etudiantcentreexamenexception__session=session)
#         if self.cod_etp[0] == 'L' and int(self.cod_etp[1]) < 3:
#             code_etp = self.cod_etp[0] + str(int(self.cod_etp[1]) + 1) + self.cod_etp[2:]
#             query |= CentreGestionException.objects.filter(
#                 etudiantcentreexamenexception__inscription__COD_ETP=code_etp,
#                 etudiantcentreexamenexception__ec_manquant=True, etudiantcentreexamenexception__session=session)
#         return query.distinct()
#
#     def get_centre_exception_premiere_session(self):
#         return self.get_centre_exception(1)
#
#     def get_centre_exception_deuxieme_session(self):
#         return self.get_centre_exception(2)
#
#     def get_etudiant_presentiel(self, session):
#         qs = INS_ADM_ETP_IED.inscrits_condi.filter(COD_ETP=self.cod_etp)\
#             .exclude(etudiantcentreexamenexception__session=session).exclude(etudiantcentreexamen__session=session)
#         return qs.distinct()
#
#     def get_etudiant_presentiel_pagine(self, session, nb_amphi, nb_table):
#         t = []
#         result = paginator_etudiant(self.get_etudiant_presentiel(session).order_by('COD_IND__LIB_NOM_PAT_IND'), nb_amphi)
#         for x in result:
#             t.extend(paginator_etudiant(x.object_list, nb_table))
#         return t
#
#     def has_centre_exament_etranger(self):
#         return True if self.get_centre_exament_etranger().count() else False
#
#     def get_url_pdf_centre_etranger(self):
#         return reverse('pdf_centre_etranger', kwargs={'etape': self.cod_etp})
#
#     def get_url_pdf_centre_etranger_recap_premiere_session(self):
#         return reverse('pdf_centre_etranger_recap', kwargs={'etape': self.cod_etp, 'session': 1})
#
#     def get_url_pdf_centre_etranger_recap_deuxieme_session(self):
#         return reverse('pdf_centre_etranger_recap', kwargs={'etape': self.cod_etp, 'session': 2})
#
#     def get_url_pdf_centre_etranger_emargement_premiere_session(self):
#         return reverse('pdf_centre_etranger_emargement', kwargs={'etape': self.cod_etp, 'session': 1})
#
#     def get_url_pdf_centre_etranger_emargement_deuxieme_session(self):
#         return reverse('pdf_centre_etranger_emargement', kwargs={'etape': self.cod_etp, 'session': 2})
#
#     def get_url_pdf_centre_dom_tom_emargement_premiere_session(self):
#         return reverse('pdf_centre_dom_tom_emargement', kwargs={'etape': self.cod_etp, 'session': 1})
#
#     def get_url_pdf_centre_dom_tom_emargement_deuxieme_session(self):
#         return reverse('pdf_centre_dom_tom_emargement', kwargs={'etape': self.cod_etp, 'session': 2})
#
#     def get_url_pdf_paris_emargement_premiere_session(self):
#         return reverse('pdf_paris_emargement', kwargs={'etape': self.cod_etp, 'session': 1})
#
#     def get_url_pdf_paris_emargement_deuxieme_session(self):
#         return reverse('pdf_paris_emargement', kwargs={'etape': self.cod_etp, 'session': 2})
#
#     class Meta:
#         proxy = True
#         ordering = ['cod_etp']
#
#
# @python_2_unicode_compatible
# class DeroulementExamenModel(models.Model):
#     etape = models.ForeignKey(Etape)
#     session = models.CharField(max_length=2, choices=(('1', 'Première session'), ('2', 'Seconde session')))
#     nb_salle = models.IntegerField('nombre de salle', null=True, blank=True)
#     nb_table = models.IntegerField('nombre de table par salle', null=True, blank=True)
#     deroulement = models.TextField('Le déroulement', help_text='chaque ec doit être séparé par un |', null=True,
#                                    blank=True)
#     date_examen = models.TextField('Date examen', null=True, blank=True)
#     salle_examen = models.TextField('salles examens', null=True, blank=True)
#
#     class Meta:
#         app_label = 'core'
#         verbose_name = "Deroulement"
#         verbose_name_plural = "Deroulements"
#         db_table = 'core_deroulementexemenmodel'  # faute ortho déjà mis en prod
#
#     def deroulement_parse(self):
#         if not self.deroulement:
#             return []
#         text = self.deroulement.encode('utf-8')
#         resultat = []
#         r = []
#         for i, x in enumerate(re.split(r'(\[[^]]*])', text)):
#             x = x.strip()
#             if i % 2:
#                 r = [x[1:-1]]
#             else:
#                 if len(x):
#                     result = []
#                     for a in x.split('|'.encode('utf-8')):
#                         b = a.strip()
#                         if not len(b):
#                             continue
#                         c = []
#                         for text in re.split(r'(<[^>]*>)', b):
#                             if text:
#                                 text = text.strip()
#                                 text = text.strip('< >'.encode('utf-8'))
#                                 text = '<br>'.encode('utf-8').join([i for i in text.splitlines()])
#                                 c.append(text)
#                         result.append(c)
#                     r.append(result)
#
#                     resultat.append(r)
#         return resultat
#
#     def __str__(self):
#         return '{} {}'.format(self.etape, self.session)
#
#
# @python_2_unicode_compatible
# class RecapitulatifExamenModel(models.Model):
#     etape = models.ForeignKey(Etape)
#     session = models.CharField(max_length=2, choices=(('1', 'Première session'), ('2', 'Seconde session')))
#     centre = models.ForeignKey(CentreGestionExamen)
#     date_envoie = models.DateField("date envoie des envellopes", null=True, blank=True)
#     date_reception = models.DateField("date réception des enveloppes", null=True, blank=True)
#     anomalie = models.CharField('anomalie', max_length=200, null=True, blank=True)
#     nb_enveloppe = models.IntegerField(null=True, blank=True)
#     nb_colis = models.IntegerField(null=True, blank=True)
#
#     class Meta:
#         app_label = 'core'
#         verbose_name = 'Recap envoie'
#         verbose_name_plural = 'Recaps envoie'
#         ordering = ['centre__pays__lib_pay']
#
#     def __str__(self):
#         return '{} {} {}'.format(self.centre.name_by_pays(), self.etape_id, self.session)
#
# class CentreGestionExamenInitial(models.Model):
#     '''
#     uniquement pour l'import Todo a supprimer
#     '''
#     label = models.CharField("Nom du centre", max_length=200, null=True)
#     adresse = models.TextField("Adresse du centre")
#     adresse_envoi_materiel = models.TextField("Adresse de l'envoi du matériel", blank=True, null=True)
#     nom = models.CharField(max_length=30, null=True, blank=True)
#     prenom = models.CharField(max_length=30, null=True, blank=True)
#     email = models.EmailField(null=True, blank=True)
#     email_bis = models.EmailField(null=True, blank=True, verbose_name="second email")
#     telephone = models.CharField(max_length=30, blank=True, null=True)
#     fax = models.CharField(max_length=30, null=True, blank=True)
#
#     pays = models.ForeignKey(Pays, verbose_name="pays")
#
#     class Meta:
#         verbose_name = "Centre examen"
#         verbose_name_plural = "Centres examens"
#         # ordering = ['pays__lib_pay']
#         db_table = 'core_centregestionexamen'
#         managed = False
