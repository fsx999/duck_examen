# coding=utf-8
from django.conf.urls import patterns, url
from rest_framework import routers

from duck_examen.adminx import ImpresssionCentre, ImpresssionRecap, ImpressionEmargement, ImpressionEtiquetteEnveloppe, \
    ImpressionPv
from duck_examen.views import DuckExamenViewSet, ExamCenterViewSet, RattachementCentreExamenViewSet

router = routers.SimpleRouter()
router.register(r'api/v1/DuckExamen', DuckExamenViewSet)
router.register(r'api/v1/ExamCenter', ExamCenterViewSet)
router.register(r'api/v1/RattachementCentreExamen', RattachementCentreExamenViewSet)

#urlpatterns = router.urls

urlpatterns = patterns(
    '',
    url(r'^impression_centre/(?P<cod_etp>\w+)/(?P<session>\w+)$',
        ImpresssionCentre.as_view(),
        name='impression_centre'),
    url(r'^impression_recap/(?P<cod_etp>\w+)/(?P<session>\w+)$',
        ImpresssionRecap.as_view(),
        name='impression_recap'),
    url(r'^impression_emargement/(?P<cod_etp>\w+)/(?P<type>\w+)/(?P<session>\w+)/(?P<pk>\w+)$',
        ImpressionEmargement.as_view(),
        name='impression_emargement'),
    url(r'^impression_envoi_centre/(?P<cod_etp>\w+)/(?P<type>\w+)/(?P<session>\w+)/(?P<pk>\w+)$$',
        ImpressionEtiquetteEnveloppe.as_view(),
        name='impression_envoi_centre'),
    url(r'^impression_pv/(?P<cod_etp>\w+)/(?P<type>\w+)/(?P<session>\w+)$',
        ImpressionPv.as_view(),
        name='impression_pv'),
    )

urlpatterns += router.urls
