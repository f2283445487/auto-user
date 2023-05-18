from api import order


class StatusBase:
    def __init__(self):
        self.info = {}

    def order_pay(self, info, which_order):
        if which_order == 'one':
            merchant_id = order.MerChant.order_merchant['first']
            one_order = 'first_order_info'
        elif which_order == 'two':
            merchant_id = order.MerChant.order_merchant['second']
            one_order = 'second_order_info'
        else:
            return 'which error'
        one_order_info = info[one_order]
        header = info['user_info']['header']
        pay_info = {'orderid': one_order_info['data'][which_order]['order_info']['loan']['id'],
                    'transferAmount': one_order_info['data'][which_order]['order_info']['loan']['transfer_amount'],
                    'accountName': one_order_info['data'][which_order]['user']['first_name'],
                    'accountNumber': one_order_info['data'][which_order]['profile']['bank_account_number'],
                    'phoneNumber': one_order_info['data'][which_order]['user']['mobile_phone']}
        order_id = pay_info['orderid']
        order_status = order.OrderStatus.order_status['wait_pay']
        order.check_order_status(order_id, order_status)
        order.pay(**pay_info)
        self.info = info
        self.info[one_order] = order.get_merchant(header, merchant_id)
        return self.info

    def order_repay(self, info, which_order):
        if which_order == 'one':
            merchant_id = order.MerChant.order_merchant['first']
            one_order = 'first_order_info'
        elif which_order == 'two':
            merchant_id = order.MerChant.order_merchant['second']
            one_order = 'second_order_info'
        else:
            return 'which error'
        order_id = info[one_order]['data'][which_order]['order_info']['loan']['id']
        header = info['user_info']['header']
        order_repay_detail = order.get_repay_detail(header, order_id)
        children_order = []
        for children_id in range(len(order_repay_detail['data']['children'])):
            children_order.append(order_repay_detail['data']['children'][children_id]['order_id'])
        va = order.get_repay_va(header, order_id, children_order)
        trans_id = va['transactionNo']
        amount = va['amount']
        payment_code = va['vaNumber']
        order.repay(trans_id, amount, payment_code)
        self.info = info
        self.info[one_order] = '第{}笔订单已还款,主订单id为{}'.format(merchant_id, order_id)
        return self.info

    def order_extension(self, info, which_order, overdue_day, expire_day):
        if which_order == 'one':
            merchant_id = order.MerChant.order_merchant['first']
            one_order = 'first_order_info'
        elif which_order == 'two':
            merchant_id = order.MerChant.order_merchant['second']
            one_order = 'second_order_info'
        else:
            return 'which error'
        order_id = info[one_order]['data'][which_order]['order_info']['loan']['id']
        order.be_overdue_order(order_id, overdue_day, expire_day)
        header = info['user_info']['header']
        self.info = info
        self.info[one_order] = order.get_merchant(header, merchant_id)
        return self.info

    def extension_apply(self, info, which_order):
        if which_order == 'one':
            merchant_id = order.MerChant.order_merchant['first']
            one_order = 'first_order_info'
        elif which_order == 'two':
            merchant_id = order.MerChant.order_merchant['second']
            one_order = 'second_order_info'
        else:
            return 'which error'
        header = info['user_info']['header']
        order_id = info[one_order]['data'][which_order]['order_info']['loan']['id']
        extension_info = order.extension_apply(header, order_id)
        trans_id = extension_info['data']['arrVA']['transactionNo']
        amount = extension_info['data']['arrVA']['amount']
        payment_code = extension_info['data']['arrVA']['vaNumber']
        order.repay(trans_id, amount, payment_code)
        self.info = info
        return self.info
