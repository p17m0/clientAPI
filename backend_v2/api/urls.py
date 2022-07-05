from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('upload_bills', UploadBillViewSet)
router.register('upload_client_org', UploadClientOrgViewSet)
router.register('bills', BillViewSet, basename='bills')

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('v1/', include(router.urls)),
]
