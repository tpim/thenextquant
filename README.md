
## TheNextQuant

异步事件驱动的量化交易/做市系统。

![](docs/images/framework.png)

![](docs/images/struct.png)


### 框架依赖

- 运行环境
	- python 3.5.3 或以上版本

- 依赖python三方包
	- aiohttp>=3.2.1
	- aioamqp>=0.13.0
	- motor>=2.0.0 (可选)

- RabbitMQ服务器
    - 事件发布、订阅

- MongoDB数据库(可选)
    - 数据存储


### 安装
使用 `pip` 可以简单方便安装:
```text
pip install thenextquant
```


### Demo使用示例

- 推荐创建如下结构的文件及文件夹:
```text
ProjectName
    |----- docs
    |       |----- README.md
    |----- scripts
    |       |----- run.sh
    |----- config.json
    |----- src
    |       |----- main.py
    |       |----- strategy
    |               |----- strategy1.py
    |               |----- strategy2.py
    |               |----- ...
    |----- .gitignore
    |----- README.md
```

- 快速体验示例
    [Demo](example/demo)


- 运行
```text
python src/main.py config.json
```


### 使用文档

本框架使用的是Python原生异步库(asyncio)实现异步事件驱动，所以在使用之前，需要先了解 [Python Asyncio](https://docs.python.org/3/library/asyncio.html)。

- [服务配置](docs/configure/README.md)
- [行情](docs/market.md)
- [交易](docs/trade.md)
- [资产](docs/asset.md)
- 当前支持交易所
    - [Binance 现货](example/binance)
    - [OKEx 现货](example/okex)
    - [Huobi 现货](example/huobi)

- 其它
    - [安装RabbitMQ](docs/others/rabbitmq_deploy.md)
    - [日志打印](docs/others/logger.md)
    - [定时任务](docs/others/tasks.md)

- 学习课程
    - [数字资产做市策略与实战](https://study.163.com/course/introduction/1209595888.htm?share=2&shareId=480000002173520)


### FAQ
- [FAQ](docs/faq.md)


### 有任何问题，欢迎联系

- 微信二维码
<p>
  <img src ="http://open-space.ifclover.com/wx_qrcode.jpeg" align="middle" width="250" height="250"/>
</p>
