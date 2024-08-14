import collections
import hashlib
from urllib.parse import quote_plus
import logging

class Params:
    def __init__(self):
        # 以下皆是測試環境
        self.params = {
            "MerchantID" : '3002599',
            "HashKey" : 'spPjZn66i0OhqJsQ',
            "HashIV" : 'hT5OJckN45isQTTs',
            "action_url" : 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'
        }

    @classmethod
    def get_params(cls):
        logging.info(f'get_params: \n{cls().params}')
        return cls().params
    
    # 驗證綠界送的檢查碼 check_mac_value
    @classmethod
    def get_check_mac_value(cls, get_request_form):
        
        params = dict(get_request_form)

        if params.get('CheckMacValue'):
            params.pop('CheckMacValue')
        
        order_params = collections.OrderedDict(
            sorted(params.items(), key=lambda k: k[0].lower())
        )

        HahKy = cls().params['HashKey']
        HashIV = cls().params['HashIV']

        encoding_list = []
        encoding_list.append('HashKey=%s&' % HahKy)
        encoding_list.append(''.join([
            '{}={}&'.format(key, value) for key, value in order_params.items()
        ]))

        encoding_list.append('HashIV=%s' % HashIV)

        safe_characters = '-_.!*()'

        encoding_str = ''.join(encoding_list)
        encoding_str = quote_plus(str(encoding_str), safe=safe_characters).lower()

        check_mac_value = ''
        check_mac_value = hashlib.sha256(encoding_str.encode('utf-8')).hexdigest().upper()

        return check_mac_value