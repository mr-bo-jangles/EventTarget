from django.apps import AppConfig


class EventConfig(AppConfig):
    name = 'event'

    def ready(self):
        super(EventConfig, self).ready()
