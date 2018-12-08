# Create your views here.
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from ipware import get_client_ip
from rest_framework import viewsets, status
from rest_framework.response import Response

from event.filters import EventFilter, DjangoFilterDescriptionInspector
from event.models import Event
from event.serializers import EventSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
   filter_inspectors=[DjangoFilterDescriptionInspector]
))
class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be created, viewed or edited.
    """
    queryset = Event.objects.all().order_by('-datetime_created')
    serializer_class = EventSerializer
    filterset_class = EventFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        source_ip, _ = get_client_ip(request)
        serializer.save(source_ip=source_ip)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
