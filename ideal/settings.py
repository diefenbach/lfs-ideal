import os
DIRNAME = os.path.dirname(__file__)

IDEAL_SECURE_PATH = os.path.join(DIRNAME, 'paydeal/includes/')
IDEAL_PRIVATEKEY = 'priv.pem'
IDEAL_PRIVATEKEYPASS = 'PRIVATEPASS'
IDEAL_PRIVATECERT = 'cert.cer'
IDEAL_CERTIFICATE0 = 'ideal.cer'
IDEAL_ACQUIRERURL = 'ssl://idealtest.secure-ing.com:443/ideal/iDeal'
#IDEAL_ACQUIRERURL = 'ssl://ideal.secure-ing.com:443/ideal/iDeal'
IDEAL_ACQUIRERTIMEOUT = '10'
IDEAL_MERCHANTID = 'MERCHANTID'
IDEAL_SUBID = '0'
IDEAL_MERCHANTRETURNURL = 'http://www.yourwebsite.com/ideal_status'
IDEAL_EXPIRATIONPERIOD = 'PT10M'
IDEAL_LOGFILE = 'log.log'
IDEAL_TRACELEVEL = 'DEBUG,ERROR'
