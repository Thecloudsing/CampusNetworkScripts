from json import loads
from time import time, sleep
from requests import post

from CustomizationLog import log
from NetworkUtils import IPUtils

version = "0.0.4"
Automatic = "Automatic"
Customization = "Customization"


def get_date_str():
    date_str = str((time() * 1000))
    end = 13
    start = end - 8
    date_str = date_str[start:end]
    return date_str


class CampusNetwork(object):

    def __init__(self, mode="Automatic", **kwargs):
        open('z_dat.db', 'a+').close()
        modes = ["Automatic", "Customization"]
        card_name = kwargs["card_name"]
        if mode not in modes:
            log.error("mode出错,已结束运行...")
            exit()

        # self.username: str = kwargs["username"]
        # self.password: str = kwargs["password"]
        self.t_server_typeid = "axe"
        self.wlan_ac_ip = "1.1.1.1"
        self.wlan_ac_name = "axe135"
        self.auto_userid = "radius_share"
        self.auto_passwd = "radius_share"
        self.dis_token = ""
        self.request_head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/113.0.0.0 '
                          'Safari/537.36 Edg/113.0.1774.57'
        }
        self.card = IPUtils(
            card_name=card_name,
            card_ip=kwargs.get("card_ip"),
            card_mac=kwargs.get("card_mac"),
            modify_ip_list=kwargs.get("modify_ip_list"))
        if mode == "Customization":
            self.wlan_user_ip = kwargs["card_ip"]
            self.wlan_user_mac = kwargs["card_mac"]
        else:
            self.wlan_user_ip = self.card.card_ip
            self.wlan_user_mac = self.card.card_mac
        self.read()

    def logo_version(self):
        logo = '''
                              _  _                                   _  _                    
          __ __      o O O   | || |     o O O  __ __ __     o O O   | || |   _  _     _ _    
          \ \ /     o         \_, |    o       \ V  V /    o         \_, |  | +| |   | ' \   
          /_\_\    TS__[O]   _|__/    TS__[O]   \_/\_/    TS__[O]   _|__/    \_,_|   |_||_|  
        _|"""""|  {======| _| """"|  {======| _|"""""|   {======| _| """"| _|"""""| _|"""""| 
        "`-0-0-' ./o--000' "`-0-0-' ./o--000' "`-0-0-'  ./o--000' "`-0-0-' "`-0-0-' "`-0-0-'
        ''' f'                                              {self.wlan_user_mac}     version - ({version})'
        print(logo)
        log.info('石斧校园网临时认证脚本')

    def read(self):
        try:
            with open('z_dat.db', 'rt') as file:
                data_json = file.read(-1)
                file.close()
                data = loads(data_json)
                self.dis_token = data["distoken"]
        except:
            pass

    def write(self, data):
        with open('z_dat.db', 'tw+') as file:
            file.write(str(data).replace("'", '"'))
            file.close()

    def modify_ip(self):
        self.wlan_user_ip = self.card.set_ip_address()

    def provisional_certification(self):
        data = {
            "wlanacip": self.wlan_ac_ip,
            "wlanacname": self.wlan_ac_name,
            "mac": self.wlan_user_mac,
            "wlanuserip": self.wlan_user_ip,
            "userId": self.auto_userid + get_date_str(),
            "passwd": self.auto_passwd
        }
        portalAuthUrl = f"http://1.1.1.1:8888/quickAuthShare.do?" \
                        f"wlanacip={self.wlan_ac_ip}&" \
                        f"wlanacname={self.wlan_ac_name}&" \
                        f"mac={self.wlan_user_mac}&" \
                        f"wlanuserip={self.wlan_user_ip}&" \
                        f"userId={self.auto_userid}{get_date_str()}&" \
                        f"passwd={self.auto_passwd}"
        ret_text = ""
        for i in range(1, 5):
            try:
                ret = post(headers=self.request_head, data={}, url=portalAuthUrl, timeout=5)
                ret_text = ret.text
                self.write(ret_text)
                break
            except:
                if i == 4:
                    log.error(f'网络异常, 结束运行...')
                    exit()
                log.error(f'发送临时认证信息失败, 第{i}次, 重试')
                self.modify_ip()

        result = loads(ret_text)
        message = result["message"]
        log.info(f'认证信息 => [{data}]')

        if message == "认证成功":
            log.info(f'{message} => [{ret_text}]')
            self.dis_token = result['distoken']
        elif message == "此IP已在线请勿重复认证":
            log.warning(f'{message} => [{ret_text}]')
            self.temporary_certification_goes_offline()
            self.provisional_certification()
        else:
            log.error(f'{message} => [{ret_text}]')
            log.error(f'{message} 限流了, 下线换IP')
            self.temporary_certification_goes_offline()
            self.modify_ip()
            self.provisional_certification()

    def temporary_certification_goes_offline(self):
        if self.dis_token == "":
            return
        discoonurl = f"http://1.1.1.1:8888/httpservice/appoffline.do?" \
                     f"wlanacip={self.wlan_ac_ip}&" \
                     f"wlanacname={self.wlan_ac_name}&" \
                     f"userId={self.auto_userid}{get_date_str()}&" \
                     f"passwd={self.auto_passwd}&" \
                     f"mac={self.wlan_user_mac}&" \
                     f"wlanuserip={self.wlan_user_ip}&" \
                     f"distoken={self.dis_token}"
        ret = post(headers=self.request_head, data={}, url=discoonurl, timeout=5)
        ret_text = ret.text
        result = loads(ret_text)
        log.info(f'{result["message"]} => [{ret_text}]')

    def run(self):
        self.logo_version()
        while True:
            self.provisional_certification()
            sleep(60 * 3 + 13)

