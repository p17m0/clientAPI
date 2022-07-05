import pandas as pd
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db import IntegrityError
from django.db.models import Sum, Count

from .serializers import UploadSerializer, BillsSerializer, BillsSerializerShow
from .models import (FileUpload,
                     Bill,
                     Client,
                     ClientOrg)
from .services import detector, classificator


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

            name, org, number, sum, date, service = (columns[0], columns[1],
                                                     columns[2], columns[3],
                                                     columns[4], columns[5])

            instances = []
            for _, row in xl.iterrows():
                service_class, service_name = classificator(service)
                fraud_score=detector(service)
                instances.append(
                Bill(name=Client.objects.filter(name=row[name]).get(),
                org=ClientOrg.objects.filter(org=row[org]).get(),
                number=row[number],
                sum=row[sum],
                date=row[date],
                service=row[service],
                fraud_score = fraud_score + 1 if fraud_score >= 0.9 else fraud_score,
                service_class=service_class,
                service_name=service_name))
            
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
            xl_org = pd.read_excel(data, sheet_name='organization',)

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
            instances_org = [
                ClientOrg(name=Client.objects.filter(name=row[namecl]).get(),
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


class InfoViewSet(ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillsSerializerShow

    def get_queryset(self):
        clients = Client.objects.all()
        print(clients)
        return [Bill.objects.annotate(
            orgcount=Count('numberorg'),
            sumclcount=Sum('sumcl').filter(name=client.name)) for client in clients]


class BillsViewSet(ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillsSerializer

    def get_queryset(self):
        clients = Client.objects.all()
        pass