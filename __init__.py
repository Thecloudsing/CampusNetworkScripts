from argparse import ArgumentParser
from CampusNetwork import CampusNetwork, mode
from NetworkUtils import match_ip

# headers = {
#     'Connection': 'keep-alive',
#     'Accept': 'application/json, text/plain, */*',
#     'Content-Type': 'application/json;charset=UTF-8',
#     'Origin': xywhost,
#     'Referer': xywhost + '/self/index.html',
#     'Accept-Encoding': 'gzip,deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9'
# }


if __name__ == '__main__':
    # modify_ip_list = ['xxx.xxx.xxx.xxx', 'xxx.xxx.xxx.xxx', 'xxx.xxx.xxx.xxx']
    # CampusNetwork(mode=Customization, card_name="WLAN", card_ip="'xxx.xxx.xxx.xxx'", card_mac="FF:FF:FF:FF:FF:FF", modify_ip_list=modify_ip_list).run()
    # sys.argv[]

    parser = ArgumentParser(description="CampusNetwork manual to this script")
    parser.add_argument("--name", type=str, default="WLAN")
    parser.add_argument("--mode", type=str, default="auto")
    parser.add_argument("--ip", type=str)
    parser.add_argument("--mac", type=str)
    parser.add_argument("--modify_ip_list", type=str, default=[])
    args = parser.parse_args()

    ip_list = []
    for i in args.modify_ip_list:
        ip = match_ip(i)
        if ip is not None:
            ip_list.append(ip)

    CampusNetwork(
        mode=mode.get(args.mode),
        card_name=args.name,
        card_ip=args.ip,
        card_mac=args.mac,
        modify_ip_list=ip_list
    ).run()
