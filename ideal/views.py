

from paydeal.ideal import iDEALConnector, IDEAL_TX_STATUS_SUCCESS
from ideal.models import IdealTransaction
from lfs.order.settings import SUBMITTED, PAID
from lfs.order.models import Order

# django imports
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
import lfs.core.signals

import lfs.order.utils
import uuid
import datetime
import locale


def process(request):
    # make instance of idealconnector
    oIDC = iDEALConnector()

    order = lfs.order.utils.add_order(request)
    amount = int(order.price * 100)

    purchaseId = order.id
    description = "Your order"
    entranceCode = str(uuid.uuid1())[:8]

    #FIXME: Determine issuerID by the incoming request
    issuerID = request.POST['issuerId'] 

    #iDEALConnector make a new transaction for this payment
    req = oIDC.RequestTransaction(issuerId=issuerID, purchaseId=purchaseId,
            amount=amount, description=description, entranceCode=entranceCode)

    # the request gives us a url, acces theis by using the
    # 'getIssuerAuthenticationURL' method
    sUrl = req.getIssuerAuthenticationURL()

    transaction = IdealTransaction()
    transaction.transaction_id = req.getTransactionID()
    transaction.authentication_url = sUrl
    transaction.purchase_id = purchaseId
    transaction.amount = amount
    transaction.entrance_code = entranceCode
    transaction.save()

    order.pay_link = sUrl
    order.state = SUBMITTED
    order.save()

    # return and send the client to pay
    return {
            'accepted': True,
            'next-url': sUrl,
            }


def check_payment(request):
    # this method should check the payment,
    # the bank (issuer) returns the client to the merchant via the return-url
    # given in the configuration config.conf
    trxid = request.GET['trxid']
    ec = request.GET['ec']

    # again make a instance of the connector
    oIDC = iDEALConnector()

    # what is the status?
    req_status = oIDC.RequestTransactionStatus(trxid)

    if not req_status.IsResponseError():
        # this is good, the pooling-request had no error, the trxid was found
        # hit the database and update the payment status
        try:
            trx = IdealTransaction.objects.get(transaction_id=trxid,
                    entrance_code=ec)
        except:
            # here, do anything needed to inform the user about the incorrect
            # payment or transport
            # by now this is left empty (bad practice of software design)
            return HttpResponseRedirect('/ideal_error/')
        else:
            # do update payment things.
            order = Order.objects.get(id=trx.purchase_id)
            print req_status.getStatus()
            trx.status = int(req_status.getStatus())
            trx.consumer_name = req_status.getConsumerName()
            trx.consumer_account = req_status.getConsumerAccountNumber()
            trx.consumer_city = req_status.getConsumerCity()
            trx.status = req_status.getStatus()

            if trx.status == IDEAL_TX_STATUS_SUCCESS:
                order.state = PAID
                trx.finished = datetime.datetime.now()
            order.save()
            trx.save()
    else:
        # an error has occured, show an error page?
        error_code = req_status.getErrorCode()
        error_msg = req_status.getErrorMessage()
        consumer_msg = req_status.getConsumerMessage()
        # an error has occured, show an error page?
        return render_to_response('ideal_error.html', {
	    'request': request,
            'error_code': error_code,
            'error_msg': error_msg,
            'consumer_msg': consumer_msg}
                )

    locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')
    amount = locale.currency(( trx.amount / 100 ))
    #FIXME: Enable this when done
    lfs.core.signals.order_sent.send({"order": order, "request": request})

    if trx.status == IDEAL_TX_STATUS_SUCCESS:
    	return render_to_response(
            'ideal_success.html',
            {
		'request': request,
                'order': order,
                'trx': trx,
		'amount': amount,
                'status_req': req_status,
                # the req_status object contains more methods, and useful for
                # giving the user status
            }
    	)
    else:
	if trx.status == 2:
		status = "De betaling is afgebroken."
	elif trx.status == 3:
		status = "De betaling is verlopen."
	elif trx.status == 4:
		status = "Er is iets fout gegaan met de betaling."
	elif trx.status == 5:
		status = "De betaling is niet gelukt en staat nog open."
	return render_to_response(
            'ideal_failure.html',
            {
                'request': request,
                'order': order,
                'trx': trx,
                'amount': amount,
                'error': req_status.errorMessage,
		'status': status,
                # the req_status object contains more methods, and useful for
                # giving the user status
            }
        )


def ideal_error(request):
    pass
