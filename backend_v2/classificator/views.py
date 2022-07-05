from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer

from .models import MyExampleModel
from .serializers import MyExampleSerializer

class MyExampleViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    queryset = MyExampleModel.objects.all()
    serializer_class = MyExampleSerializer
    renderer_classes = (XLSXRenderer,)
    filename = 'my_export.xlsx'