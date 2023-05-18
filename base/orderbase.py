from api import order


class OrderBase:

    def __init__(self):
        self.info = {}

    def first_order_apply(self, user_info):
        """第一笔借款审核中"""
        self.info['user_info'] = user_info
        header = self.info['user_info']['header']
        user_id = self.info['user_info']['user_id']
        merchant_id = order.MerChant.order_merchant['first']
        order.apply(header, merchant_id)
        self.info['first_order_info'] = order.get_merchant(header, merchant_id)
        loan = self.info['first_order_info']['data']['one']['order_info']['loan']
        first_order_id = loan['id']
        first_order_merchant = loan['order_merchant']
        first_order_status = loan['order_status']
        order.submit(header, user_id, first_order_id, first_order_merchant, first_order_status)
        return self.info

    def second_order_apply(self, user_info):
        """第一笔借款审核中，第二笔借款审核中"""
        self.first_order_apply(user_info)
        first_order_id = self.info['first_order_info']['data']['one']['order_info']['loan']['id']
        merchant_id = order.MerChant.order_merchant['second']
        order_status = order.OrderStatus.order_status['submit']
        order.check_order_status(first_order_id, order_status)
        header = self.info['user_info']['header']
        user_id = self.info['user_info']['user_id']
        order.apply(header, merchant_id)
        self.info['second_order_info'] = order.get_merchant(header, merchant_id)
        second_order_info = self.info['second_order_info']
        second_order_id = second_order_info['data']['two']['order_info']['loan']['id']
        second_order_merchant = second_order_info['data']['two']['order_info']['loan']['order_merchant']
        second_order_status = second_order_info['data']['two']['order_info']['loan']['order_status']
        order.submit(header, user_id, second_order_id, second_order_merchant, second_order_status)
        return self.info
