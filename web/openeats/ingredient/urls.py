from django.conf.urls import url

from openeats.ingredient import views

urlpatterns = [
   url(r'^auto/$', views.autocomplete_ing),
]