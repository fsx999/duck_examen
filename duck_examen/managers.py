# coding=utf-8
from django.db import models


class ExamenCenterManager(models.Manager):

    def get_by_cod_etp_by_session(self, cod_etp, session, amenagement_examen=None, parcours=-1):
        # type (int, int, AmenagementExamenModel,Parcours) -> django.db.models.query.QuerySet
        """
        Récupere tout les centres en fonction du cod_etp, session
        comme le parcours peut valoir None, on le met à -1 (valeur non transmisse)

        """

        filters = {
            'rattachementcentreexamen__inscription__cod_etp': cod_etp,
            'rattachementcentreexamen__inscription__cod_anu':  2015,
            'rattachementcentreexamen__session': session,
        }
        if amenagement_examen:
            filters['rattachementcentreexamen__type_amenagement'] = amenagement_examen
        if parcours != -1:
            filters['rattachementcentreexamen__parcours'] = parcours

        return self.filter(**filters).distinct()

    def get_incorporation_by_cod_etp_by_session(self, cod_etp, session, amenagement_examen=None, parcours=-1):
        # type (int, int, AmenagementExamenModel,Parcours) -> django.db.models.query.QuerySet
        return self.get_by_cod_etp_by_session(cod_etp, session, amenagement_examen, parcours).filter(has_incorporation=True).distinct()

    def get_autre_by_cod_etp_by_session(self, cod_etp, session,  amenagement_examen=None, parcours=-1):
        # type (int, int, AmenagementExamenModel,Parcours) -> django.db.models.query.QuerySet
        return self.get_by_cod_etp_by_session(cod_etp, session, amenagement_examen, parcours).filter(has_incorporation=False, is_main_center=False).distinct()

    def get_main_center_by_cod_etp_by_session(self, cod_etp, session,  amenagement_examen=None, parcours=-1):
        # type (int, int, AmenagementExamenModel,Parcours) -> django.db.models.query.QuerySet
        return self.get_by_cod_etp_by_session(cod_etp, session, amenagement_examen, parcours).filter(is_main_center=True).distinct()
