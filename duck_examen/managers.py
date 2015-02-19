__author__ = 'paulguichon'
from django.db import models


class ExamenCenterManager(models.Manager):

    def get_by_cod_etp_by_session(self, cod_etp, session):
        return self.filter(rattachementcentreexamen__inscription__cod_etp=cod_etp,
                           rattachementcentreexamen__session=session,
                           has_incorporation=True).distinct()