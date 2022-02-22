from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    url(r'^$', views.temperature, name=''), 
    path('update/<str:co>/<str:temp>/<str:hum>/', views.update),
]