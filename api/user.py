import requests
from database import db
import random


def get_account():
    """生成账号"""
    phone = random.randint(80000000000, 88800000000)
    sql = "select id from singa_origin.users where mobile_phone = '{}'".format(phone)
    data = db.select(sql)
    if not data:
        user_phone = phone
        return user_phone
    else:
        get_account()


def send_code(account_num):
    """发送验证码"""
    body = {
        "mobile_phone": account_num,
        "type": "mobile"
    }
    url = 'http://api-test.singa.id/new/login/sendCode'
    requests.post(url, json=body)


def login_phone(account_num):
    """输入手机号"""
    url = 'http://api-test.singa.id/new/login/first-step-by-phone'
    body = {
        "mobile_phone": account_num
    }
    requests.post(url, json=body)


def set_pw(account_num, code):
    body = {
        "mobile_phone": account_num,
        "code": code,
        "password": "abc123456"
    }
    url = "http://api-test.singa.id/new/login/setting-password"
    res = requests.post(url, json=body)
    return res.json()


def get_phone_code(account_num):
    """读取数据库验证码"""
    sql = 'select * from singa_origin.sg_login_verfications where verfied_by = "{}"'.format(account_num)
    try:
        data = db.select(sql)
        return data[-1]["code"]
    except Exception as e:
        return e


def upload_file(header):
    """上传文件"""
    # file = {'file': open(r'C:\Users\86172\Desktop\demo\files\ktp.jpg', 'rb')}
    file_data = {'file_ktp_ocr': open('C:\\Users\\86172\\Desktop\\singa-user\\files\\ktp.jpg', 'rb')}
    url = "http://api-test.singa.id/new/index/uploadFile"
    res = requests.post(url, files=file_data, headers=header)
    return res.json()['data']['url']


def get_ktp(file_path, header):
    """解析ktp"""
    body = {
        "img_url": file_path,
        "isWrite": '1'
    }
    url = "http://api-test.singa.id/new/index/getUserInfoByKtp"
    requests.post(url, json=body, headers=header)


def get_info_id(userid):
    sql = "select id from singa_origin.sg_user_personal_infos where user_id = {}".format(userid)
    try:
        data = db.select(sql)
        return data[0]['id']
    except Exception as e:
        return e


def get_ktp_num():
    ktp_number = random.randint(3275030000000000, 3275039999999999)
    sql = "select id from singa_origin.sg_user_personal_infos where ktp_number = '{}'".format(ktp_number)
    data = db.select(sql)
    if not data:
        return ktp_number
    else:
        get_ktp_num()


def save_personal_info(person_id, header):
    ktp_num = get_ktp_num()
    user_basic_info_body = {
        "data": "[{\"id\":" + str(
            person_id) + ",\"ktp_image_url\": \"3213/4324324\",\"name\":\"singaAuto\",\"birthday\":\"1980-04-20 00:00:00\",\"family_size\":11,\"email\":\"2283445487@yahoo.com\",\"gender\":1,\"ktp_number\":\"" + str(
            ktp_num) + "\",\"ref_education_id\":1,\"ref_housing_id\":1,\"ref_marital_id\":2,\"residential_addr_detail\":\"KEPULAUAN RIAU KABUPATEN BINTAN TELUK SEBONG SEBONG LAGOI Jl.Langsat\",\"ref_residential_addr_province_id\":1,\"ref_residential_addr_city_id\":110,\"ref_residential_addr_region_id\":1,\"ref_residential_addr_village_id\":16271,\"whatsapp\":\"081270789748\"}]",
        "type": "user_basic_info"
    }
    user_work_info_body = {
        "data": "[{\"company_name\":1,\"work_phone\":17262638891,\"ref_company_addr_province_id\":1,\"ref_company_addr_city_id\":1,\"ref_company_addr_region_id\":1,\"ref_company_addr_village_id\":1,\"company_addr_detail\":\"hddhhd\",\"income\":6000000000,\"work_years\":0,\"ref_job_id\":8}]",
        "type": "user_work_info"
    }
    user_contacts_info_body = {
        "data": "[{\"name\":\"1000332\",\"phone_number\":\"1000332\",\"ref_relationship_id\":\"1\"},{\"name\":\"本机\",\"phone_number\":\"85781331761\",\"ref_relationship_id\":\"2\"},{\"name\":\"tyj\",\"phone_number\":\"888955888833\",\"ref_relationship_id\":\"3\"}]",
        "type": "user_contacts_info"
    }
    user_bank_card_info_body = {
        "data": "[{\"account_number\":\"987654123\",\"pre_account_number\":\"987654123\",\"ref_bank_id\":2}]",
        "type": "user_bank_card_info"
    }
    url = "http://api-test.singa.id/new/users/savePersonalData"
    try:
        requests.post(url, json=user_basic_info_body, headers=header)
        requests.post(url, json=user_work_info_body, headers=header)
        requests.post(url, json=user_contacts_info_body, headers=header)
        requests.post(url, json=user_bank_card_info_body, headers=header)
    except Exception as e:
        return e
