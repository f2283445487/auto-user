import requests
from database import db
import time
import datetime


class OrderStatus:
    order_status = {
        'submit': 11,
        'wait_pay': 13
    }


class MerChant:
    order_merchant = {
        'first': 1,
        'second': 2
    }


def apply(header, merchant):
    if merchant == 1:
        body = {
            "products": [
                {
                    "refPurposeId": 1,
                    "amount": 1100000,
                    "duration": 60,
                    "loanId": 58,
                    "couponId": 0,
                    "merchantId": 1
                }
            ],
            "versionName": "2.0.23"
        }
    else:
        body = {
            "products": [
                {
                    "refPurposeId": 1,
                    "amount": 1100000,
                    "duration": 60,
                    "loanId": 62,
                    "couponId": 0,
                    "merchantId": 2
                }
            ],
            "versionName": "2.0.23"
        }
    url = 'http://api-test.singa.id/V2/order/apply-merchant'
    res = requests.post(url, json=body, headers=header)
    return res


def get_merchant(header, merchant):
    body = {
        "merchant": merchant
    }
    url = 'http://api-test.singa.id/V3/mldlrp-merchant'
    res = requests.get(url, json=body, headers=header)
    return res.json()


def submit(header, userid, orderid, order_merchant, order_status):
    body = {
        "user_id": userid,
        "order_info": [
            {
                "order_id": orderid,
                "order_merchant": order_merchant,
                "order_status": order_status
            }
        ]
    }
    url = 'http://api-test.singa.id/V2/order/submit-merchant'
    res = requests.post(url, json=body, headers=header)
    return res


def pay(**kwargs):
    body = {"arrPayData": "[{\"orderId\": " + str(kwargs['orderid']) + ", \"transferAmount\": " + str(kwargs[
                                                                                                          'transferAmount']) + ", \"interestAmount\": 352000, "
                                                                                                                               "\"managementfeeAmount\": 0, \"managementType\": 2, \"account\": {\"accountName\": "
                                                                                                                               "\"" + str(
        kwargs['accountName']) + "\", \"accountNumber\": \"" + kwargs[
                              'accountNumber'] + "\", \"email\": \"\", \"phoneNumber\": "
                                                 "\"" + kwargs[
                              'phoneNumber'] + "\", \"bankId\": \"80017\", \"bankName\": \"MANDIRI\", \"type\": "
                                               "\"borrower\"}}]"}
    url = 'http://api-test.singa.id/singaPay/api/test/pay'
    res = requests.post(url, json=body)
    return res.json()


def check_order_status(orderid, status):
    sql = "select order_status from singa_order.sgo_orders where id = {}".format(orderid)
    try:
        data = db.select(sql)
        # print(data[0]['order_status'])
        if data[0]['order_status'] == status:
            return data[0]['order_status']
        else:
            time.sleep(20)
            check_order_status(orderid, status)
    except Exception as e:
        return e


def order_pay(info, which_order):
    order = info['first_order_info']['data'][which_order]
    pay_info = {'orderid': order['order_info']['loan']['id'],
                'transferAmount': order['order_info']['loan']['transfer_amount'],
                'accountName': order['user']['first_name'],
                'accountNumber': order['profile']['bank_account_number'],
                'phoneNumber': order['user']['mobile_phone']}
    order_id = pay_info['orderid']
    order_status = OrderStatus.order_status['wait_pay']
    check_order_status(order_id, order_status)
    pay(**pay_info)


def get_repay_detail(header, order_id):
    body = {
        'order_id': order_id
    }
    url = 'http://api-test.singa.id/new/repayment/getRepaymentDetailMerchant'
    res = requests.post(url, headers=header, json=body)
    return res.json()


def get_repay_va(header, orderid, children_order):
    body = {
        "loanID": orderid,
        "bankCode": '1',
        'stagingIdList': children_order
    }
    url = 'http://api-test.singa.id/V3/pdva'
    res = requests.post(url, headers=header, json=body)
    return res.json()


def repay(trans_id, amount, payment_code):
    body = {
        "TRANSIDMERCHANT": trans_id,
        "AMOUNT": amount,
        "paymentcode": payment_code
    }
    url = 'http://api-test.singa.id/singaPay/api/test/pay/doku/notify'
    requests.post(url, json=body)





def extension_apply(header, orderid):
    body = {
        "order_id": orderid,
        "bank_code": 1
    }
    url = 'http://api-test.singa.id/new/order/generateExtensionOrder'
    res = requests.post(url, json=body, headers=header)
    return res.json()


def be_overdue_order(orderid, overdue_day, expire_day):
    overdue_day = (datetime.datetime.now() - datetime.timedelta(days=overdue_day)).strftime('%Y-%m-%d %H:%M:%S')
    expire_day = (datetime.datetime.now() - datetime.timedelta(days=expire_day)).strftime('%Y-%m-%d %H:%M:%S')
    children_order_sql = "select id from singa_order.sgo_orders where parent_order_id = {}".format(orderid)
    data = db.select(children_order_sql)
    children_id = data[0]['id']
    sql = "update `singa_order`.`sgo_orders` set overdue_at =  '{}' , expire_at = '{}' where id = {}".format(
        overdue_day,
        expire_day,
        children_id)
    db.update(sql)


def order_status_rejected(userid, orderid):
    sql = "select order_status from singa_order.sgo_orders where id = {}".format(orderid)
    data = db.select(sql)
    if data[0]['order_status'] == 13:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sg_user_reject_sql = "insert into singa_origin.sg_user_rejected (user_id,order_id,reject_status,status,reject_time) values({},{},2,2,'{}')".format(
            userid, orderid, now)
        db.update(sg_user_reject_sql)
        order_check_sql = "update singa_rc.order_check set passed = 2 where order_id = {}".format(orderid)
        db.update(order_check_sql)
        order_status_sql = "update singa_order.sgo_orders set order_status = 94 where id or parent_order_id = {}".format(
            orderid)
        db.update(order_status_sql)
        order_log = "select id from singa_order.sgo_order_statuses where order_id = {} order by id desc limit 1".format(
            orderid)
        data = db.select(order_log)
        order = data[0]['id']
        order_status_log_sql = "update singa_order.sgo_order_statuses set order_status = 94 where id = {}".format(
            order)
        db.update(order_status_log_sql)
    else:
        time.sleep(5)
        order_status_rejected(userid, orderid)
