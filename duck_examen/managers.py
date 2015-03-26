__author__ = 'paulguichon'
from django.db import models


class ExamenCenterManager(models.Manager):

    def get_by_cod_etp_by_session(self, cod_etp, session, type_examen):
        return self.filter(rattachementcentreexamen__inscription__cod_etp=cod_etp,
                           rattachementcentreexamen__session=session, rattachementcentreexamen__type_examen__name=type_examen).distinct()

    def get_incorporation_by_cod_etp_by_session(self, cod_etp, session, type_examen):
        return self.get_by_cod_etp_by_session(cod_etp, session, type_examen).filter(has_incorporation=True).distinct()

    def get_autre_by_cod_etp_by_session(self, cod_etp, session, type_examen):
        return self.get_by_cod_etp_by_session(cod_etp, session, type_examen).filter(has_incorporation=False, is_main_center=False).distinct()

    def get_main_center_by_cod_etp_by_session(self, cod_etp, session, type_examen):
        return self.get_by_cod_etp_by_session(cod_etp, session, type_examen).filter(is_main_center=True).distinct()