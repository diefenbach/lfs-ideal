from django.db import models


class IdealDirectory(models.Model):
    directory_timestamp = models.DateTimeField(blank=True, null=True)


class IdealIssuer(models.Model):
    issuer_id = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    list_type = models.CharField(max_length=15)
    directory = models.ForeignKey(IdealDirectory)

    def __unicode__(self):
        return "%s (%s)" % (self.issuer_name, self.issuer_id)


class IdealTransaction(models.Model):
    STATUS_CHOICES = (
            (0, 'IDEAL_TX_STATUS_INVALID'),
            (1, 'IDEAL_TX_STATUS_SUCCESS'),
            (2, 'IDEAL_TX_STATUS_CACNELLED'),
            (3, 'IDEAL_TX_STATUS_EXPIRED'),
            (4, 'IDEAL_TX_STATUS_FAILURE'),
            (5, 'IDEAL_TX_STATUS_OPEN'),
            )
    transaction_id = models.CharField(max_length=16)
    authentication_url = models.CharField(max_length=255)
    purchase_id = models.CharField(max_length=20)
    amount = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=5)
    entrance_code = models.CharField(max_length=8)
    consumer_name = models.CharField(max_length=100, blank=True, null=True)
    consumer_account = models.CharField(max_length=25, blank=True, null=True)
    consumer_city = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "Transaction (%s) of order %s for %.2f" % (
                self.transaction_id, self.purchase_id, float(self.amount) / 100
                )
