import pandas as pd
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db import IntegrityError

from .serializers import UploadSerializer, BillsSerializer
from .models import (FileUpload,
                     Bill,
                     Client,
                     ClientOrg)


class UploadBillViewSet(ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = UploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if request.data['file'] is None:
            return Response({"error": "No File Found"},
                            status=status.HTTP_400_BAD_REQUEST)

        if (str(request.data['file']) == 'bills.xlsx' and
           serializer.is_valid(raise_exception=True)):
            data = request.data.get('file')
            xl = pd.read_excel(data)
            columns = list(xl.columns.values)

            name, org, numer, sum, date, service = (columns[0], columns[1],
                                                    columns[2], columns[3],
                                                    columns[4], columns[5])
            instances = [
                Bill(
                    name=row[name],
                    org=row[org],
                    numer=row[numer],
                    sum=row[sum],
                    date=row[date],
                    service=row[service],)
                for index, row in xl.iterrows()
                    ]
            Bill.objects.bulk_create(instances)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UploadClientOrgViewSet(ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = UploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if request.data['file'] is None:
            return Response({"error": "No File Found"},
                            status=status.HTTP_400_BAD_REQUEST)

        if (str(request.data['file']) == 'client_org.xlsx' and
           serializer.is_valid(raise_exception=True)):
            data = request.data.get('file')

            xl_clients = pd.read_excel(data, sheet_name='client')
            xl_org = pd.read_excel(data, sheet_name='organization',
                                   skiprows=[0])

            columns_clients = list(xl_clients.columns.values)
            columns_org = list(xl_org.columns.values)

            name = columns_clients[0]
            namecl, org, address = (columns_org[0],
                                    columns_org[1],
                                    columns_org[2],)
            try:
                instances_cl = [
                    Client(name=row[name],)
                    for index, row in xl_clients.iterrows()
                        ]
                Client.objects.bulk_create(instances_cl)
            except IntegrityError:
                print("error")
            print('--------')
            print(namecl)
            print('--------')
            print(Client.objects.get(name=namecl))
            instances_org = [
                ClientOrg(name=row[Client.objects.filter(name=namecl).get()],
                           org=row[org],
                           address=f'Адрес: {row[address]}',)
                for index, row in xl_org.iterrows()
                    ]

            ClientOrg.objects.bulk_create(instances_org)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class ListClient(viewsets.ModelViewSet):
#     serializer_class = BillsSerializer

#     def get_queryset(self):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, pk=title_id)
#         new_queryset = title.reviews.all()
#         return new_queryset