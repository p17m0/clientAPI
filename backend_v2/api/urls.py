from posixpath import basename
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('upload_bills', UploadBillViewSet, basename='uploadbills')
router.register('upload_client_org', UploadClientOrgViewSet, basename='uploadclient')
router.register('client_info', InfoViewSet, basename='client_info')


# Wire up our API using automatic URL routing.
urlpatterns = [
    path('v1/bills/', BillsListView.as_view()),
    path('v1/', include(router.urls)),
]
