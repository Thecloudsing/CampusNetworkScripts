from CampusNetwork import CampusNetwork, Automatic

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
    modify_ip_list = ['10.1.143.239', '10.1.143.240', '10.1.143.241']
    CampusNetwork(mode=Automatic, card_name="WLAN", modify_ip_list=modify_ip_list).run()

