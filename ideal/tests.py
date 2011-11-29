from django.test import TestCase


A = """2011-11-10T11:56:24.000Z: DEBUG: sending to ssl://idealtest.secure-ing.com:443/ideal/iDeal: <?xml version="1.0" encoding="UTF-8"?>
<AcquirerTrxReq xmlns="http://www.idealdesk.com/Message" version="1.1.0">
<createDateTimeStamp>2011-11-10T11:56:24.000Z</createDateTimeStamp>
<Issuer>
<issuerID>0151</issuerID>
</Issuer>

<Merchant>
<merchantID>005041182</merchantID>
<subID>0</subID>
<authentication>SHA1_RSA</authentication>
<token>56D0F58D62F5D0B7655419983C1C23B5793B09DE</token>
<tokenCode>xPDNO9XKaUluh36mQpiESjN6j45UIfRTUnLBjNDBWwrENtCxNDgejF/xplPH8UsvuOSz/L7gAS59vCUZvpOvz7LGU1b2iSVOQkIBhs1nVuFqIkdhrAvbNl38xG7uVXg64pF1rkCrEzRMWbYcMDVaaQ7eHhSiXq2mE8QIkPvTtik=</tokenCode>
<merchantReturnURL>http://new.jeansconcurrent.nl</merchantReturnURL>
</Merchant>
<Transaction>
<purchaseID>432455</purchaseID>
<amount>100</amount>
<currency>EUR</currency>
<expirationPeriod>PT10M</expirationPeriod>
<language>nl</language>
<description>Your order</description>
<entranceCode>random</entranceCode>
</Transaction>
</AcquirerTrxReq>"""

B = """2011-11-10T11:56:25.000Z: DEBUG: receiving from https://idealtest.secure-ing.com:443/ideal/iDeal: <?xml version="1.0" encoding="UTF-8"?>
<AcquirerTrxRes xmlns="http://www.idealdesk.com/Message" version="1.1.0">
  <createDateTimeStamp>2011-11-10T11:56:25.654Z</createDateTimeStamp>
<Acquirer>
  <acquirerID>0050</acquirerID>
</Acquirer>
<Issuer>
  <issuerAuthenticationURL>https://idealtest.secure-ing.com/ideal/issuerSim.do?trxid=0050000053979195&amp;ideal=prob</issuerAuthenticationURL>
</Issuer>
<Transaction>
  <transactionID>0050000053979195</transactionID>
  <purchaseID>432455</purchaseID>
</Transaction>
</AcquirerTrxRes>"""

