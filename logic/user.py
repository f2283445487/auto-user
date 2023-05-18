from base import userbase


def account():
    user = userbase.UserBase()
    user_info = user.account()
    return user_info


def save_info_account():
    user = userbase.UserBase()
    user_info = user.save_info_account()
    return user_info
