from django_apogee.models import InsAdmEtpInitial, Individu
from rest_framework import filters
from rest_framework import viewsets
from duck_examen.serializers import (DuckExamenSerializer,
                                     RattachementCentreExamenSerializer,
                                     ExamCenterSerializer,
                                     )
from models import RattachementCentreExamen, ExamCenter


class DuckExamenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InsAdmEtpInitial.objects.using('oracle').filter(cod_cge="IED", cod_anu=2015)
    serializer_class = DuckExamenSerializer
    paginate_by = 5

    filter_backends = (filters.SearchFilter,)
    search_fields = ('cod_ind__cod_etu',
                     'cod_ind__lib_nom_pat_ind',
                     'cod_ind__lib_nom_usu_ind',
                     'cod_ind__lib_pr1_ind',
                     'cod_ind__lib_pr2_ind',
                     'cod_ind__lib_pr3_ind',
                     'cod_etp'
                     )


class RattachementCentreExamenViewSet(viewsets.ModelViewSet):
    queryset = RattachementCentreExamen.objects.all()
    serializer_class = RattachementCentreExamenSerializer
    paginate_by = 100


class ExamCenterViewSet(viewsets.ModelViewSet):
    queryset = ExamCenter.objects.all()
    serializer_class = ExamCenterSerializer


class RattachementAppViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Individu.objects.using('oracle').all()
