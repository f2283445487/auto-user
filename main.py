from logic import order, user

if __name__ == '__main__':
    while True:
        print(
            "1.未保存信息用户 \n"
            "2.已保存信息用户 \n"
            "3:借一笔  \n"
            "4.借两笔  \n"
            "5.第一笔放款成功  \n"
            "6.两笔放款成功  \n"
            "7.第一笔放款成功，第二笔申请中  \n"
            "8.第一笔已结清，第二笔放款成功  \n"
            "9.一笔订单并且满足展期  \n"
            "10.两笔订单都满足展期  \n"
            "11.一笔订单，逾期八天  \n"
            "12.一笔订单，逾期八天还款  \n"
            "13.一笔订单，生成展期订单  \n")
        a = input('输入。。。。')
        if a == '3':
            print(order.one_order_apply())
        elif a == '4':
            print(order.two_order_apply())
        elif a == '5':
            print(order.one_order_pay_success())
        elif a == '6':
            print(order.two_order_pay_success())
        elif a == '7':
            print(order.one_order_pay_success_two_order_apply())
        elif a == '8':
            print(order.one_order_repay_success_two_order_pay_success())
        elif a == '9':
            print(order.one_order_extension())
        elif a == '10':
            print(order.two_order_extension())
        elif a == '11':
            print(order.one_order_overdue_eight())
        elif a == '12':
            print(order.one_order_overdue_eight_repay())
        elif a == '13':
            print(order.one_order_extension_apply())
        elif a == '1':
            print(user.account())
        elif a == '2':
            print(user.save_info_account())
        else:
            print('error')
