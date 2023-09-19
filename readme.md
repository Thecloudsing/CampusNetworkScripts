# 校园网认证脚本

## 执行脚本必须管理员方式运行

## CampusNetwork 配置
### mode
+ `Automatic` => 【默认】自动模式，自动匹配网卡名称获取IP及MAC信息
+ `Customization` => 自定义模式，需要手动填写`card_ip`，`card_ip`参数
### 必填参数

#### 在 Automatic 模式下必要参数
- `card_name` => 连接校园网的网卡名称，作用是自动获取IP及MAC信息
- `modify_ip_list` => IP更换列表，作用是在限流的情况下更换IP，重新发起请求【需要注意的是IP在校园网内网段，避免IP冲突】

#### 在 Customization 模式下必要参数
- `card_ip` => 连接校园网的网卡IP
- `card_mac` => 连接校园网的网卡MAC地址，如FF:FF:FF:FF:FF:FF
- `modify_ip_list` => IP更换列表，作用是在限流的情况下更换IP，重新发起请求【需要注意的是IP在校园网内网段，避免IP冲突】

### z_dat.db
* 存储上次，获取的认证信息

### 如何知道可以用该脚本呢？
1. 校园网是石斧
2. 注册校园网账号时网络可用

### 有疑问可以Q
* `1019741841`