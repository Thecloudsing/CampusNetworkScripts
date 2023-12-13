# 校园网认证脚本

## 执行脚本必须管理员方式运行

## CampusNetwork 配置
### mode
+ `Automatic` => 【默认】自动模式，自动匹配网卡名称获取IP及MAC信息
+ `Customization` => 自定义模式，需要手动填写`card_ip`，`card_ip`参数
### 必填参数

#### 在 Automatic 模式下必要参数
- `card_name` => 连接校园网的网卡名称，作用是自动获取IP及MAC信息

#### 在 Automatic 模式下可选填参数
- `modify_ip_list` ==> IP更换列表，作用是在限流的情况下更换IP，重新发起请求【需要注意的是IP在校园网内网段，避免IP冲突】

#### 在 Customization 模式下必要参数
- `card_name` => 连接校园网的网卡名称，作用是修改IP
- `card_ip` => 连接校园网的网卡IP
- `card_mac` => 连接校园网的网卡MAC地址，如*FF:FF:FF:FF:FF:FF*
- `modify_ip_list` => IP更换列表，作用是在限流的情况下更换IP，重新发起请求【需要注意的是IP在校园网内网段，避免IP冲突】

## 目录结构

- ### `main.py` 程序主入口
- ### `build.py` 程序打包
- ### `requirements.txt` 依赖模块

- ### /core 
  * `CampusNetwork.py` 核心模块
  * `CustomizationLog.py` 自定义日志模块
  * `FileUtils.py` 文件工具类
  * `NetworkUtils.py` 网络工具类

- ### /db 
  * `dis.token.db` 存储上次，获取的认证信息

- ### /log
  * `error.log` 错误日志
  * `run.log` 运行日志

- ### /config
  * `config.properties` 配置文件 ~ 目前没有用
  


### 如何知道可以用该脚本呢？
1. 校园网是石斧
2. 注册校园网账号时网络可用

# star
### 有疑问可以Q 
* 交流群 `1019741841`