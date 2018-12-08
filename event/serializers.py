from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = (
            'uuid',
            'latitude',
            'longitude',
            'country_iso',
            'country_name',
            'city',
            'datetime_created',
            'source_ip'
        )
