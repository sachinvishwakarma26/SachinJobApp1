# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'hydjobs', views.HydJobsCRUDCBV)
router.register(r'punejobs', views.PuneJobsCRUDCBV)
router.register(r'blorejobs', views.BloreJobsCRUDCBV)
router.register(r'chennaijobs', views.ChennaiJobsCRUDCBV)
router.register(r'noidajobs', views.NoidaJobsCRUDCBV)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', include(router.urls)),

    path(r'api-auth', include('rest_framework.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'^api/(?P<id>\d+)/$', views.PuneJobsCRUDCBV.as_view()),
    path(r'^api/(?P<id>\d+)/$', views.HydJobsCRUDCBV.as_view()),
    path(r'^api/(?P<id>\d+)/$', views.NoidaJobsCRUDCBV.as_view()),
    path(r'^api/(?P<id>\d+)/$', views.BloreJobsCRUDCBV.as_view()),
    path(r'^api/(?P<id>\d+)/$', views.ChennaiJobsCRUDCBV.as_view()),
    #path(r'api/punejobsinfo/(?P<pk>[^/.]+)\'[name='punejobs-detail']))
]