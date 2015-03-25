# coding=utf-8
from django.conf.urls import patterns, url
from duck_examen.adminx import ImpresssionCentre, ImpresssionRecap, ImpressionEmargement, ImpressionEtiquetteEnveloppe, \
    ImpressionPv


urlpatterns = patterns(
    '',
    url(r'^impression_centre/(?P<cod_etp>\w+)/(?P<session>\w+)$',
        ImpresssionCentre.as_view(),
        name='impression_centre'),
    url(r'^impression_recap/(?P<cod_etp>\w+)/(?P<session>\w+)$',
        ImpresssionRecap.as_view(),
        name='impression_recap'),
    url(r'^impression_emargement/(?P<cod_etp>\w+)/(?P<type>\w+)/(?P<session>\w+)/(?P<type_examen>\w+)$',
        ImpressionEmargement.as_view(),
        name='impression_emargement'),
    url(r'^impression_envoi_centre/(?P<cod_etp>\w+)/(?P<type>\w+)/(?P<session>\w+)$',
        ImpressionEtiquetteEnveloppe.as_view(),
        name='impression_envoi_centre'),
    url(r'^impression_pv/(?P<cod_etp>\w+)/(?P<type>\w+)/(?P<session>\w+)$',
        ImpressionPv.as_view(),
        name='impression_pv'),
    )

