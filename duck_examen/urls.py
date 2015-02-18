# coding=utf-8
from django.conf.urls import patterns, url
from duck_examen.adminx import ImpresssionCentre, ImpresssionRecap


urlpatterns = patterns(
    '',
    url(r'^impression_centre/(?P<cod_etp>\w+)/(?P<session>\w+)$',
        ImpresssionCentre.as_view(),
        name='impression_centre'),
    url(r'^impression_recap/(?P<cod_etp>\w+)/(?P<session>\w+)$',
        ImpresssionRecap.as_view(),
        name='impression_recap'),
    )

