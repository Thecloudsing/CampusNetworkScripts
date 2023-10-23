import re
import subprocess
from array import array
from time import sleep
from CustomizationLog import log


class IPUtils(object):

    def __init__(self, **kwargs):
        self.card_ip = kwargs.get("card_ip")
        self.card_mac = kwargs.get("card_mac")
        self.ip_address_index = 0
        self.card_name = kwargs["card_name"]
        self.modify_ip_list = kwargs.get("modify_ip_list")

        if self.card_name is None or self.card_mac is None:
            self.get_ip_address()

    def get_ip_address(self):
        ip3_reg_str = '((2[0-4]\d)|(25[0-5])|(1\d{2})|([1-9]\d)|([1-9]))'
        ip_reg_str = f'(({ip3_reg_str}\.){{3}}{ip3_reg_str})'
        mac_reg_str = '((([\da-fA-F]){2}-){5}([\da-fA-F]){2})'
        reg_str = f'(.|\\n)*无线局域网适配器 {self.card_name}:(.|\\n)*?' \
                  f'物理地址. . . . . . . . . . . . . : {mac_reg_str}(.|\\n)*?' \
                  f'IPv4 地址 . . . . . . . . . . . . : {ip_reg_str}(.|\\n)*'
        ipconfig = subprocess.check_output('ipconfig/all', shell=True)
        reg = re.compile(reg_str)
        match = reg.match(str(ipconfig, 'GBK'))
        try:
            if match is not None:
                self.card_mac = match.group(3).replace('-', ':')
                self.card_ip = match.group(8)
                if self.modify_ip_list is None:
                    self.modify_ip_list = []
                    self.modify_ip_list.append(self.card_ip)
                    last_index = self.card_ip.rindex('.')
                    first = self.card_ip[0:last_index + 1]
                    last = int(self.card_ip[last_index + 1:len(self.card_ip)])
                    for i in range(0, 10):
                        last += 1
                        if last > 253:
                            break
                        self.modify_ip_list.append(first + str(last))
                    log.info(f'自动获取IP列表 ==> {self.modify_ip_list}')
                else:
                    log.info(f'自定义IP列表 ==> {self.modify_ip_list}')
                self.ip_address_index = self.modify_ip_list.index(self.card_ip)
                return self.card_ip + "|" + self.card_mac
        except:
            log.error(f'获取ip地址失败, 请以检查网卡名字是否正确')
            exit()

    def set_ip_address(self):
        current_ip_index = self.ip_address_index

        while True:
            if current_ip_index > len(self.modify_ip_list):
                current_ip_index = 0
            current_ip_index += 1
            modify_ip = self.modify_ip_list[current_ip_index]
            if self.card_ip != modify_ip:
                break

        try:
            command = f'netsh interface ip set address name={self.card_name} static {modify_ip} 255.255.248.0 10.1.143.253'
            output = subprocess.run(["powershell.exe", "-Command", command], shell=True, check=True)
            log.info(f'修改IP 地址 => [ "{self.card_ip}" => "{modify_ip}" ]')
            log.info(f'command ==> [{command}]')
            self.ip_address_index = current_ip_index
            self.card_ip = modify_ip
            sleep(5)
            return modify_ip
        except:
            log.error(f'没有管理员权限, 请以管理员方式运行py')
            exit()
