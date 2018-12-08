import random
import requests
from celery import shared_task
from django.conf import settings

from event.models import Event


@shared_task(rate_limit='5/m', bind=True)
def geolocate_event(self, event_id):
    event = Event.objects.get(pk=event_id)
    response = requests.get(
        url=settings.GEOLOCATE_API_ENDPOINT,
        params={
            'ip': event.source_ip
        },
        timeout=10
    )
    if response.status_code == requests.codes.ok:
        response_json = response.json()
        country = response_json.get("country", {})
        location = response_json.get("location", {})
        event.city = response_json.get('city', None)
        event.country_iso = country.get('iso_code', None)
        event.country_name = country.get('name', None)
        event.latitude = location.get('latitude', None)
        event.longitude = location.get('longitude', None)
        event.save()
    elif response.status_code == requests.codes.too_many_requests:
        response_json = response.json()
        raise self.retry(
            args=(event_id,),
            countdown=int(random.uniform(response_json["period_remaining"], 60) ** self.request.retries)
        )
    elif response.status_code == requests.codes.bad_request:
        raise ValueError(f"The given url {response.url} was rejected by the GeoLocation API")
    elif response.status_code == requests.codes.server_error:
        raise ValueError("The geo location API couldn't resolve the IP address")
    else:
        raise ValueError(response)
