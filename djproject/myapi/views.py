from rest_framework import viewsets
from testapp.models import hydjobs, punejobs, blorejobs, chennaijobs, noidajobs
from testapp.api.serializers import HydJobsSerializer, PuneJobsSerializer, ChennaiJobsSerializer, BloreJobsSerializer,\
     NoidaJobSerializer


class HydJobsCRUDCBV(viewsets.ModelViewSet):
    serializer_class = HydJobsSerializer
    queryset = hydjobs.objects.all().order_by('company')
    lookup_field = 'id'


class PuneJobsCRUDCBV(viewsets.ModelViewSet):
    serializer_class = PuneJobsSerializer
    queryset = punejobs.objects.all().order_by('company')
    lookup_field = 'id'


class ChennaiJobsCRUDCBV(viewsets.ModelViewSet):
    serializer_class = ChennaiJobsSerializer
    queryset = chennaijobs.objects.all().order_by('company')
    lookup_field = 'id'


class BloreJobsCRUDCBV(viewsets.ModelViewSet):
    serializer_class = BloreJobsSerializer
    queryset = blorejobs.objects.all().order_by('company')
    lookup_field = 'id'


class NoidaJobsCRUDCBV(viewsets.ModelViewSet):
    serializer_class = NoidaJobSerializer
    queryset = noidajobs.objects.all().order_by('company')
    lookup_field = 'id'
