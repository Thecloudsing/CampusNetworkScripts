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

options_ui = '''
________          __  .__                       _________                _____.__        
\_____  \ _______/  |_|__| ____   ____   ______ \_   ___ \  ____   _____/ ____\__| ____  
 /   |   \\____ \   __\  |/  _ \ /    \ /  ___/ /    \  \/ /  _ \ /    \   __\|  |/ ___\ 
/    |    \  |_> >  | |  (  <_> )   |  \\___ \  \     \___(  <_> )   |  \  |  |  / /_/  >
\_______  /   __/|__| |__|\____/|___|  /____  >  \______  /\____/|___|  /__|  |__\___  / 
        \/|__|                       \/     \/          \/            \/        /_____/
        
'''

if __name__ == '__main__':
    # modify_ip_list = ['xxx.xxx.xxx.xxx', 'xxx.xxx.xxx.xxx', 'xxx.xxx.xxx.xxx']
    # CampusNetwork(mode=Customization, card_name="WLAN", card_ip="'xxx.xxx.xxx.xxx'", card_mac="FF:FF:FF:FF:FF:FF", modify_ip_list=modify_ip_list).run()
    # sys.argv[]

    parser = ArgumentParser(description="CampusNetwork manual to this script")
    parser.add_argument("--name", type=str, default="WLAN")
    parser.add_argument("--mode", type=str, default="auto")
    parser.add_argument("--ip", type=str)
    parser.add_argument("--mac", type=str)
    parser.add_argument("--stop", type=int, default=3)
    parser.add_argument("--modify_ip_list", type=str, default=[])
    args = parser.parse_args()

    ip_list = []
    for i in args.modify_ip_list:
        ip = match_ip(i)
        if ip is not None:
            ip_list.append(ip)

    print(options_ui)

    name = ''
    loop = -1
    print('[*]****       Enter commit        ****')
    if args.name == 'WLAN':
        name = input('[?]Is update default card-name(WLAN): ') or args.name
    if args.stop == 3:
        loop = -1 if input('[?]Whether it never stops (y/[Enter or other default no]): ') == 'y' else int(args.stop)

    # print()
    CampusNetwork(
        mode=mode.get(args.mode),
        card_name=name,
        card_ip=args.ip,
        card_mac=args.mac,
        modify_ip_list=ip_list,
        stop=loop
    ).run()
