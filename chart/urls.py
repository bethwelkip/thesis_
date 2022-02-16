from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.temperature, name=''),
    url(r'^update/(?P<co2>\d{3,5})/(?P<temp>\d{1,3})/(?P<hum>\d{1,2})$', views.update, name='update'),
]