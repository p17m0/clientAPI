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
                             blank=True,
                             related_name='orgs')
    org = models.CharField(verbose_name='Client_organization',
                           unique=True,
                           max_length=20)
    address = models.CharField(verbose_name='Client_address',
                               unique=True,
                               max_length=20)

    fraud_weight = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['address', 'org'],
                                    name='unique_address')]


class Bill(models.Model):
    name = models.ForeignKey(Client,
                             on_delete=models.CASCADE, related_name='bills')
    org = models.ForeignKey(ClientOrg,
                            on_delete=models.CASCADE,
                            )
    numberorg = models.IntegerField()
    sumcl = models.IntegerField()
    date = models.DateField()
    service = models.CharField(max_length=20)
    fraud_score = models.FloatField()
    service_class = models.IntegerField()
    service_name = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['numberorg', 'org'],
                                    name='unique_number')]
