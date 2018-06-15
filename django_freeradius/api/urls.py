from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^authorize/$', views.authorize, name='authorize'),
    url(r'^postauth/$', views.postauth, name='postauth'),
    url(r'^accounting/$', views.accounting, name='accounting'),
    url(r'^v1/batchCsv/$', views.batchCsv, name='batchCsv'),
    url(r'^v1/batchPrefix/$', views.batchPrefix, name='batchPrefix'),
]
