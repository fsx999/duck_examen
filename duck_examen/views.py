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


    # def list(self, request):
    #     if request.GET.get('cod_anu', None):
    #         self.queryset = InsAdmEtpInitial.objects.using('oracle').filter(cod_cge="IED",
    #                                                                         cod_anu__in=request.GET.getlist('cod_anu'))
    #
    #     return super(DuckExamenViewSet, self).list(request)

class RattachementCentreExamenViewSet(viewsets.ModelViewSet):
    queryset = RattachementCentreExamen.objects.all()
    serializer_class = RattachementCentreExamenSerializer
    paginate_by = 100

class ExamCenterViewSet(viewsets.ModelViewSet):
    queryset = ExamCenter.objects.all()
    serializer_class = ExamCenterSerializer

class RattachementAppViewSet(viewsets.ViewSet):
#     """
#     Example empty viewset demonstrating the standard
#     actions that will be handled by a router class.

#     If you're using format suffixes, make sure to also include
#     the `format=None` keyword argument for each action.
#     """
    queryset = Individu.objects.using('oracle').all()
    # permission_classes = () # CA POSE PROBLEME ...
    def list(self, request):
        elems = []


        return Response(['coucou'])

#     def create(self, request):
#         print('create > {}'.format(request))
#         return Response("COUCOUCOU")

#     def retrieve(self, request, pk=None):
#         print('retrieve > {}'.format(request.method))
#         return Response("COUCOUCOU")


#     def update(self, request, pk=None):
#         print('update > {}'.format(request.method))
#         return Response("COUCOUCOU")


#     def partial_update(self, request, pk=None):
#         print('partial_update > {}'.format(request))
#         return Response("COUCOUCOU")


#     def destroy(self, request, pk=None):
#         print('destroy > {}'.format(request))
#         return Response("COUCOUCOU")