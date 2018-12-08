from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from uuid import uuid4


class Event(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    source_ip = models.GenericIPAddressField(help_text="The IP we recorded the event record coming from")
    name = models.TextField(help_text="The type of event that is being recorded, for example 'Signup'")
    city = models.TextField(help_text="The resolved city for the event source IP address")
    country_iso = models.TextField(help_text="The resolved country code for the event source IP address")
    country_name = models.TextField(help_text="The resolved human usable country name for the event source IP address")
    latitude = models.TextField(help_text="How far north/south the event source is estimated to be")
    longitude = models.TextField(help_text="How far east/west the event source is estimated to be")
    data = JSONField(help_text="A JSON object containing all your additional parameters")

    datetime_created = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Event)
def queue_geolocate_event(sender, instance, **kwargs):
    from .tasks import geolocate_event
    geolocate_event.delay(
        event_id=str(instance.pk)
    )

