from api import user


class UserBase:

    def __init__(self):
        self.user_info = {"user_phone": user.get_account()}

    def __login(self):
        user_phone = self.user_info['user_phone']
        user.send_code(user_phone)
        user.login_phone(user_phone)
        code = user.get_phone_code(user_phone)
        res = user.set_pw(user_phone, code)
        self.user_info['user_id'] = res['data']['user_id']
        token = 'Bearer ' + res['data']['token']
        self.user_info['header'] = {
            "Authorization": token
        }

    def account(self):
        """生成账号，未保存信息"""
        self.__login()
        return self.user_info

    def save_info_account(self):
        """生成账号，已保存用户信息"""
        self.__login()
        header = self.user_info['header']
        user_id = self.user_info['user_id']
        ktp_path = user.upload_file(header)
        user.get_ktp(ktp_path, header)
        person_id = user.get_info_id(user_id)
        user.save_personal_info(person_id, header)
        return self.user_info
