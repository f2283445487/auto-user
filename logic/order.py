from base import orderbase, statusbase, userbase


def one_order_apply():
    """借一笔"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    user_info = user.save_info_account()
    order_info = order.first_order_apply(user_info)
    return order_info


def two_order_apply():
    """借两笔"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    user_info = user.save_info_account()
    order_info = order.second_order_apply(user_info)
    return order_info


def one_order_pay_success():
    """第一笔放款成功"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    status = statusbase.StatusBase()
    user_info = user.save_info_account()
    order_info = order.first_order_apply(user_info)
    status_info = status.order_pay(order_info, which_order='one')
    return status_info


def two_order_pay_success():
    """两笔放款成功"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    status = statusbase.StatusBase()
    user_info = user.save_info_account()
    order_info = order.second_order_apply(user_info)
    status.order_pay(order_info, which_order='one')
    status_info = status.order_pay(order_info, which_order='two')
    return status_info


def one_order_pay_success_two_order_apply():
    """第一笔放款成功，第二笔申请中"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    status = statusbase.StatusBase()
    user_info = user.save_info_account()
    order_info = order.second_order_apply(user_info)
    status_info = status.order_pay(order_info, which_order='one')
    return status_info


def one_order_repay_success_two_order_pay_success():
    """第一笔已结清，第二笔放款成功"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    status = statusbase.StatusBase()
    user_info = user.save_info_account()
    order_info = order.second_order_apply(user_info)
    pay_info = status.order_pay(order_info, which_order='one')
    repay_info = status.order_repay(pay_info, which_order='one')
    status_info = status.order_pay(repay_info, which_order='two')
    return status_info


def one_order_extension():
    """一笔订单并且满足展期"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    status = statusbase.StatusBase()
    user_info = user.save_info_account()
    order_info = order.first_order_apply(user_info)
    status.order_pay(order_info, which_order='one')
    status_info = status.order_extension(order_info, which_order='one', overdue_day=0, expire_day=1)
    return status_info


def two_order_extension():
    """两笔订单都满足展期"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    status = statusbase.StatusBase()
    user_info = user.save_info_account()
    order_info = order.second_order_apply(user_info)
    status.order_pay(order_info, which_order='one')
    status.order_pay(order_info, which_order='two')
    status.order_extension(order_info, which_order='one', overdue_day=0, expire_day=1)
    status_info = status.order_extension(order_info, which_order='two', overdue_day=0, expire_day=1)
    return status_info


def one_order_overdue_eight():
    """一笔订单，逾期八天"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    status = statusbase.StatusBase()
    user_info = user.save_info_account()
    order_info = order.first_order_apply(user_info)
    status.order_pay(order_info, which_order='one')
    status_info = status.order_extension(order_info, which_order='one', overdue_day=8, expire_day=9)
    return status_info


def one_order_overdue_eight_repay():
    """一笔订单，逾期八天还款"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    status = statusbase.StatusBase()
    user_info = user.save_info_account()
    order_info = order.first_order_apply(user_info)
    status.order_pay(order_info, which_order='one')
    status.order_extension(order_info, which_order='one', overdue_day=8, expire_day=9)
    status_info = status.order_repay(order_info, which_order='one')
    return status_info


def one_order_extension_apply():
    """一笔订单，生成展期订单"""
    user = userbase.UserBase()
    order = orderbase.OrderBase()
    status = statusbase.StatusBase()
    user_info = user.save_info_account()
    order_info = order.first_order_apply(user_info)
    status.order_pay(order_info, which_order='one')
    status.order_extension(order_info, which_order='one', overdue_day=0, expire_day=1)
    status_info = status.extension_apply(order_info, which_order='one')
    return status_info
