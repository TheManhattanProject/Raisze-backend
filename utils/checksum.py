import paytmchecksum
from django.conf import settings

data = {'ORDERID': 'PAY2ME20220711ODR17', 'MID': 'waJxHx32224764812860', 'TXNID': '20220711111212800110168564903891272',
        'TXNAMOUNT': '122.00', 'PAYMENTMODE': 'CC', 'CURRENCY': 'INR', 'TXNDATE': '2022-07-11 12:39:55.0', 'STATUS': 'TXN_SUCCESS',
        'RESPCODE': '01', 'RESPMSG': 'Txn Success', 'GATEWAYNAME': 'HDFC', 'BANKTXNID': '777001965037051',
        'BANKNAME': 'JPMorgan Chase Bank',
        'CHECKSUMHASH': 'gztRh8UjxpcvaeAlfBpM0cZU3rLTIyjw8YT0a6bwnV/TgSrx47W7seF6ZQAnLFqtswIEGueVa9b1VT7dWcNT8tLz3r2haBkuIujAKC0vJfI='}


print(paytmchecksum.verifySignature(
    data, settings.PAYTM_SECRET_KEY, data['CHECKSUMHASH']))
