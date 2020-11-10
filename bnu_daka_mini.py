import os
import requests, json, re
import time, datetime
from apscheduler.schedulers.blocking import BlockingScheduler


class DaKa(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.info = None

        self.login_url = "https://onewechat.bnu.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fonewechat.bnu.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex"
        self.base_url = "https://onewechat.bnu.edu.cn/ncov/wap/default/index"
        self.save_url = "https://onewechat.bnu.edu.cn/ncov/wap/default/save"
        self.login_check_url = "https://onewechat.bnu.edu.cn/uc/wap/login/check"
        self.sess = requests.Session()


    def login(self):
        """Login to BNU platform"""
        res = self.sess.get(self.login_url)
        
        if res.status_code != 200:
            raise Exception('{} login failed, status code {}'.format(self.username,res.status_code))

        data = {'username': self.username,
                'password': self.password,}
        
        res = self.sess.post(url=self.login_check_url, data=data)
        ret = json.loads(res.content.decode())

        if ret['e'] != 0:
            raise Exception("{} login failed, reason {}".format(self.username,ret['m']))
        return ret
    
    def post(self):
        """Post the hitcard info"""
        res = self.sess.post(self.save_url, data=self.info)
        if res.status_code != 200:
            raise Exception("{} post info failed, status code {}".format(self.username, res.status_code))
        return json.loads(res.text)

    @ staticmethod
    def get_date():
        today = datetime.date.today()
        return "%4d%02d%02d" % (today.year, today.month, today.day)
        
    def get_info(self, html=None):
        """Get hitcard info, which is the old info with updated new time."""
        if not html:
            res = self.sess.get(self.base_url)
            if res.status_code != 200:
                raise Exception("{} get info faild, statu code {}".format(self.username, res.status_code))
            html = res.content.decode()
        old_info = json.loads(re.findall(r'oldInfo: (.*)', html)[0][:-1])
        name = re.findall(r'realname: "([^\"]+)",', html)[0]
        number = re.findall(r"number: '([^\']+)',", html)[0]

        new_info = old_info.copy()
        new_info['name'] = name
        new_info['number'] = number
        new_info["date"] = self.get_date()
        new_info["created"] = round(time.time())

        self.info = new_info
        self.save_info()

        return new_info

    @ staticmethod
    def _rsa_encrypt(self, password_str, e_str, m_str):
        password_bytes = bytes(password_str, 'ascii') 
        password_int = int.from_bytes(password_bytes, 'big')
        e_int = int(e_str, 16) 
        m_int = int(m_str, 16)
        result_int = pow(password_int, e_int, m_int)
        return hex(result_int)[2:].rjust(128, '0')

    def save_info(self):
        with open("cache_info_bk.json", "w", encoding="utf-8") as file:
            json.dump(self.info, file)


    def daka(self):
        ret = []
        res = self.login()
        ret.append(res)
        res = self.get_info()
        ret.append(res)
        res = self.post()
        ret.append(res)
        ret.append(res)
        return ret


def main(username, password):

    dk = DaKa(username, password)
    try:
        dk.daka()
    except Exception as e:
        print(e)
    finally:
        return 0


def run():
    if not os.path.exists('/home/bnu/bnufast/config.txt'):
        print('Please create file config.txt to {}.'.format(os.getcwd()))
        return

    with open('/home/bnu/bnufast/config.txt', 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            username, password = line.strip('\n').split('\t')
            main(username, password)


if __name__ == "__main__":
    run()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Done!")
