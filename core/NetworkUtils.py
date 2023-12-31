from re import compile
import subprocess
from time import sleep
from core.CustomizationLog import log, out_err


class IPUtils(object):
    primary_dns = '8.8.8.8'
    spare_dns = '223.5.5.5'
    mask = '255.255.248.0'
    gateway = '10.1.143.253'
    gwmetric = '1'

    def __init__(self, **kwargs):
        self.card_ip = kwargs.get("card_ip")
        self.card_mac = kwargs.get("card_mac")
        self.ip_address_index = 0
        self.card_name = kwargs["card_name"]
        self.modify_ip_list = kwargs.get("modify_ip_list")

        if self.card_name is None or self.card_mac is None:
            self.get_ip_address()
        else:
            print('tttttttttttttt')

    def get_ip_address(self):
        try:
            command = f'netsh interface ip set address name="{self.card_name}" dhcp'
            subprocess.run(['powershell.exe', '-Command', command], shell=True)
        except Exception as e:
            out_err()
            log.info(f'dhcp interface error, name ==> [{self.card_name}]')

        ip3_reg_str = '((2[0-4]\d)|(25[0-5])|(1\d{2})|([1-9]\d)|([1-9]))'
        ip_reg_str = f'(({ip3_reg_str}\.){{3}}{ip3_reg_str})'
        mac_reg_str = '((([\da-fA-F]){2}-){5}([\da-fA-F]){2})'
        reg_str = f'(.|\\n)*无线局域网适配器 {self.card_name}:(.|\\n)*?' \
                  f'物理地址. . . . . . . . . . . . . : {mac_reg_str}(.|\\n)*?' \
                  f'IPv4 地址 . . . . . . . . . . . . : {ip_reg_str}(.|\\n)*'
        ipconfig = subprocess.check_output('ipconfig/all', shell=True, encoding="GBK")
        reg = compile(reg_str)
        match = reg.match(ipconfig)
        try:
            if match is not None:
                self.card_mac = match.group(3).replace('-', ':')
                self.card_ip = match.group(8)
                if self.modify_ip_list is None or self.modify_ip_list == []:
                    self.modify_ip_list = []
                    self.modify_ip_list.append(self.card_ip)
                    last_index = self.card_ip.rindex('.')
                    first = self.card_ip[0:last_index + 1]
                    last = int(self.card_ip[last_index + 1:len(self.card_ip)])
                    for i in range(0, 10):
                        last += 1
                        if last > 253:
                            last = 100
                        self.modify_ip_list.append(first + str(last))
                    log.info(f'自动获取IP列表 ==> {self.modify_ip_list}')
                else:
                    log.info(f'自定义IP列表 ==> {self.modify_ip_list}')
                self.ip_address_index = self.modify_ip_list.index(self.card_ip)
                return self.card_ip + "|" + self.card_mac
        except Exception as e:
            out_err()
            log.error(f'获取ip地址失败, 请以检查网卡名字是否正确')
            exit()

    def set_ip_address(self):
        current_ip_index = self.ip_address_index

        while True:
            if current_ip_index >= len(self.modify_ip_list) - 1:
                current_ip_index = 0
            current_ip_index += 1
            modify_ip = self.modify_ip_list[current_ip_index]
            if self.card_ip != modify_ip:
                break

        try:
            name = f'name="{self.card_name}"'
            set_ip_command = f'netsh interface ip set address {name} static {modify_ip} ' \
                             f'{self.mask} {self.gateway} {self.gwmetric}'
            set_dns_command = f'netsh interface ip set dns {name} static {self.primary_dns} primary'
            add_dns_command = f'netsh interface ip add dns {name} {self.spare_dns} 2'
            log.info(f'修改IP 地址 => [ "{self.card_ip}" => "{modify_ip}" ]')
            log.info(f'command ==> [{set_ip_command}]')
            subprocess.run(['powershell.exe', '-Command', set_ip_command], shell=True)
            subprocess.run(['powershell.exe', '-Command', set_dns_command], shell=True)
            subprocess.run(['powershell.exe', '-Command', add_dns_command], shell=True)
            self.ip_address_index = current_ip_index
            self.card_ip = modify_ip
            sleep(5)
            return modify_ip
        except Exception as e:
            out_err()
            log.error(f'修改IP失败，出错... (可能不是以管理员方式运行)')
            exit()


def match_ip(ip):
    ip_item = '((25[0-5])|(2[0-4]\d)|(1\d{2})|([1-9]\d)|\d)'
    reg = compile(f'^(({ip_item}\.){{3}}{ip_item})$')
    try:
        match = reg.match(ip.strip())
        return match.group(1)
    except:
        pass
