import json
from django.test import TestCase, Client

from django.urls import reverse

from event.models import Event
from event.tasks import geolocate_event


class EventAPITestCase(TestCase):

    def check_event_list_count(self, expected=0, message="The list view is returning results when they're not expected"):
        post_check = self.client.get(
            reverse('event-list'),
            content_type='application/json',
        )
        count = post_check.data.get('count')
        results = post_check.data.get('results')
        self.assertEqual(post_check.status_code, 200)
        self.assertEqual(count, expected, message)
        return results

    def test_geolocation_of_event(self):
        self.assertFalse(Event.objects.exists(), "The database isn't empty")

        event = Event.objects.create(name="asidfja", source_ip="109.150.106.87", data={"test": "data"})

        self.assertTrue(Event.objects.exists(), "Required Event wasn't created as expected")

        geolocate_event(event_id=event.pk)

        event = Event.objects.get(pk=event.pk)
        self.assertEqual(event.city, "Willenhall")

    def test_list_events(self):
        self.check_event_list_count()
        Event.objects.create(name="asidfja", source_ip="109.150.106.87", data={"test": "data"})
        self.check_event_list_count(1, message="The list view is not picking up the new objects we created")

    def test_create_event(self):
        self.check_event_list_count()
        event_json = {
            "name": "join",
            "data": {
                "extra": "values",
                "that": "are not",
                "defined": "already"
            }
        }
        response = self.client.post(
            reverse('event-list'),
            content_type='application/json',
            data=event_json
        )
        self.assertEqual(response.status_code, 201, response.json())

        results = self.check_event_list_count(1, "There should be one item created, but that didn't show on the list view")
        result = results[0]
        self.assertEqual(result['name'], event_json['name'], "The name of the object we saved and the object we got are not the same")
        self.assertDictEqual(result['data'], event_json['data'], "The data of the object we saved and the object we got are not the same")

    def test_delete_events(self):
        self.check_event_list_count()
        Event.objects.create(name="asidfja", source_ip="109.150.106.87", data={"test": "data"})

        self.check_event_list_count(1, "The view isn't picking up saved objects, or objects are no longer being saved with .create()")

        event = Event.objects.first()
        response = self.client.delete(
            reverse('event-detail', kwargs={'pk': event.pk})
        )

        self.assertEqual(response.status_code, 204, "We weren't expecting any content back from a delete request")
        self.check_event_list_count()
