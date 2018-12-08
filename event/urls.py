from django.conf.urls import url
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from event import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Event API",
      default_version='v1',
      description="Simple event storage target",
      terms_of_service="https://example.com/terms",
      contact=openapi.Contact(email="contact@events.local"),
      license=openapi.License(name="BSD License"),
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
