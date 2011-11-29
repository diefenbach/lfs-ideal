from django.core.management.base import BaseCommand, CommandError
from ideal.models import IdealIssuer, IdealDirectory
from ideal.paydeal.ideal import iDEALConnector
import datetime
import sys


class Command(BaseCommand):
    help = 'Retrieve a list of issuers and cache them in the db.'

    def convert_iso_time(self, dt_str):
        dt, _, us = dt_str.partition(".")
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        us = int(us.rstrip("Z"), 10)
        return dt + datetime.timedelta(microseconds=us)

    def handle(self, *args, **options):
        oIDC = iDEALConnector()
        issuers = oIDC.GetIssuerList()

        # we have a list of issuers (banks), or an error
        if issuers.IsResponseError():
            # debug in error, printout the message
            raise CommandError('%s: %s' % (issuers.getErrorMessage(),
                issuers.getErrorCode()))

        try:
            directory = IdealDirectory.objects.latest(
                field_name='directory_timestamp')
        except IdealDirectory.DoesNotExist:
            # First time we run it
            directory = IdealDirectory()
            directory.directory_timestamp = datetime.datetime(1970, 1, 1)
            directory.save()

        directory_timestamp = self.convert_iso_time(
                issuers.getDirectoryDateTimeStamp())

        if directory_timestamp > directory.directory_timestamp:
            sys.stdout.write('New directory found.\n')
            directory = IdealDirectory()
            directory.directory_timestamp = directory_timestamp
            directory.save()

            dIssuers = issuers.getIssuerFullList()
            for sIS, oIS in dIssuers.items():
                issuer, created = IdealIssuer.objects.get_or_create(
                        name=oIS.getIssuerName(), directory=directory)
                issuer.issuer_id = oIS.getIssuerID()
                issuer.list_type = oIS.getIssuerListType()
                issuer.name = oIS.getIssuerName()
                try:
                    issuer.save()
                except:
                    raise CommandError('Couldn\'t save issuer.')

                sys.stdout.write('Issuer %s (%s) added\n' % (issuer.name,
                    issuer.issuer_id
                 ))
        else:
            sys.stdout.write('No changes to the directory.\n')
