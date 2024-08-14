from datetime import datetime
from .database import select_item_price

def order_param_init(hostname :str,item: str):
    target = select_item_price(item)
    item_name = target.level
    item_price = target.price
    return {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': item_price,
        'TradeDesc': '訂單測試',
        'ItemName': item_name, # free, basic, premium, or VVIP
        'ReturnURL': hostname + '/receive_result',
        'ChoosePayment': 'ALL',
        'ClientBackURL': hostname + '/trad_result',
        # 'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': hostname + '/trad_result',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '阿倫測試中',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }

def extend_params_1():
    return {
    'ExpireDate': 7,
    'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
    'ClientRedirectURL': '',
    }

def extend_params_2():
    return {
    'StoreExpireDate': 15,
    'Desc_1': '',
    'Desc_2': '',
    'Desc_3': '',
    'Desc_4': '',
    'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
    'ClientRedirectURL': '',
    }

def extend_params_3():
    return {
    'BindingCard': 0,
    'MerchantMemberID': '',
    }   

def extend_params_4():
    return {
    'Redeem': 'N',
    'UnionPay': 0,
    }

def inv_params():
    return {
    'RelateNumber': 'Tea0001', # 特店自訂編號
    'CustomerID': 'TEA_0000001', # 客戶編號
    'CustomerIdentifier': '53348111', # 統一編號
    'CustomerName': '客戶名稱',
    'CustomerAddr': '客戶地址',
    'CustomerPhone': '0912345678', # 客戶手機號碼
    'CustomerEmail': 'abc@ecpay.com.tw',
    'ClearanceMark': '2', # 通關方式
    'TaxType': '1', # 課稅類別
    'CarruerType': '', # 載具類別
    'CarruerNum': '', # 載具編號
    'Donation': '1', # 捐贈註記
    'LoveCode': '168001', # 捐贈碼
    'Print': '1',
    'InvoiceItemName': 'free',
    'InvoiceItemCount': '2|3',
    'InvoiceItemWord': '個|包',
    'InvoiceItemPrice': '35|10',
    'InvoiceItemTaxType': '1|1',
    'InvoiceRemark': 'free document',
    'DelayDay': '0', # 延遲天數
    'InvType': '07', # 字軌類別
    }
