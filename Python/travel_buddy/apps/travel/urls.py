from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^add_travel$',views.add_travel), #takes you to the add destination page
    url(r'^destination/(?P<destination_id>\d+)$', views.destination), #displays the destination profile
    url(r'^add$',views.add),#submits destination form
    url(r'^join/(?P<destination_id>\d+)$', views.join)#allows user to join a trip
]
