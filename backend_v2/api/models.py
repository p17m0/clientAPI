from django.db import models


class FileUpload(models.Model):
    """Represents file upload model class."""

    file = models.FileField(upload_to='xlsx/%y/%m')


class Client(models.Model):
    name = models.CharField(verbose_name='Client_name',
                            unique=True,
                            max_length=20,
                            primary_key=True)

    def __str__(self):
        return self.name


class ClientOrg(models.Model):
    name = models.ForeignKey(Client,
                             on_delete=models.CASCADE,
                             blank=True,)
    org = models.CharField(verbose_name='Client_organization',
                           unique=True,
                           max_length=20)
    address = models.CharField(verbose_name='Client_address',
                               unique=True,
                               max_length=20)


class Bill(models.Model):
    name = models.ForeignKey(Client,
                             on_delete=models.CASCADE)
    org = models.ForeignKey(ClientOrg,
                            on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True)
    sum = models.IntegerField()
    date = models.DateField()
    service = models.CharField(max_length=20)
