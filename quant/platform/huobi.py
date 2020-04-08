# -*- coding:utf-8 -*-

"""
huobi 交易模块
https://huobiapi.github.io/docs/spot/v1/cn

Author: HuangTao
Date:   2018/08/30
"""

import base64
import datetime
import hashlib
import hmac
import urllib
from urllib import parse
from urllib.parse import urljoin

from quant.utils.web import AsyncHttpRequests

__all__ = ("HuobiRestAPI", )


class HuobiRestAPI:
    """ huobi REST API 封装
    """

    def __init__(self, host, access_key, secret_key):
        """ 初始化
        @param host 请求host
        @param access_key API KEY
        @param secret_key SECRET KEY
        """
        self._host = host
        self._access_key = access_key
        self._secret_key = secret_key
        self._account_id = None

    async def get_server_time(self):
        """ 获取服务器时间
        @return data int 服务器时间戳(毫秒)
        """
        success, error = await self.request("GET", "/v1/common/timestamp")
        return success, error

    async def get_user_accounts(self):
        """ 获取账户信息
        """
        success, error = await self.request("GET", "/v1/account/accounts")
        return success, error

    async def _get_account_id(self):
        """ 获取账户id
        """
        if self._account_id:
            return self._account_id
        success, error = await self.get_user_accounts()
        if error:
            return None
        for item in success:
            if item["type"] == "spot":
                self._account_id = item["id"]
                return self._account_id
        return None

    async def get_account_balance(self):
        """ 获取账户信息
        """
        account_id = await self._get_account_id()
        uri = "/v1/account/accounts/{account_id}/balance".format(account_id=account_id)
        success, error = await self.request("GET", uri)
        return success, error

    async def get_balance_all(self):
        """ 母账户查询其下所有子账户的各币种汇总余额
        """
        success, error = await self.request("GET", "/v1/subuser/aggregate-balance")
        return success, error

    async def create_order(self, symbol, price, quantity, order_type):
        """ 创建订单
        @param symbol 交易对
        @param quantity 交易量
        @param price 交易价格
        @param order_type 订单类型 buy-market, sell-market, buy-limit, sell-limit
        @return order_no 订单id
        """
        account_id = await self._get_account_id()
        info = {
            "account-id": account_id,
            "price": price,
            "amount": quantity,
            "source": "api",
            "symbol": symbol,
            "type": order_type
        }
        if order_type == "buy-market" or order_type == "sell-market":
            info.pop("price")
        success, error = await self.request("POST", "/v1/order/orders/place", body=info)
        return success, error

    async def revoke_order(self, order_no):
        """ 撤销委托单
        @param order_no 订单id
        @return True/False
        """
        uri = "/v1/order/orders/{order_no}/submitcancel".format(order_no=order_no)
        success, error = await self.request("POST", uri)
        return success, error

    async def revoke_orders(self, order_nos):
        """ 批量撤销委托单
        @param order_nos 订单列表
        * NOTE: 单次不超过50个订单id
        """
        body = {
            "order-ids": order_nos
        }
        result = await self.request("POST", "/v1/order/orders/batchcancel", body=body)
        return result

    async def get_open_orders(self, symbol):
        """ 获取当前还未完全成交的订单信息
        @param symbol 交易对
        * NOTE: 查询上限最多500个订单
        """
        account_id = await self._get_account_id()
        params = {
            "account-id": account_id,
            "symbol": symbol,
            "size": 500
        }
        result = await self.request("GET", "/v1/order/openOrders", params=params)
        return result

    async def get_order_status(self, order_no):
        """ 获取订单的状态
        @param order_no 订单id
        """
        uri = "/v1/order/orders/{order_no}".format(order_no=order_no)
        success, error = await self.request("GET", uri)
        return success, error

    async def request(self, method, uri, params=None, body=None):
        """ 发起请求
        @param method 请求方法 GET POST
        @param uri 请求uri
        @param params dict 请求query参数
        @param body dict 请求body数据
        """
        url = urljoin(self._host, uri)
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        params = params if params else {}
        params.update({"AccessKeyId": self._access_key,
                       "SignatureMethod": "HmacSHA256",
                       "SignatureVersion": "2",
                       "Timestamp": timestamp})

        host_name = urllib.parse.urlparse(self._host).hostname.lower()
        params["Signature"] = self.generate_signature(method, params, host_name, uri)

        if method == "GET":
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/39.0.2171.71 Safari/537.36"
            }
        else:
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json"
            }
        _, success, error = await AsyncHttpRequests.fetch(method, url, params=params, data=body, headers=headers,
                                                          timeout=10)
        if error:
            return success, error
        if success.get("status") != "ok":
            return None, success
        return success.get("data"), None

    def generate_signature(self, method, params, host_url, request_path):
        """ 创建签名
        """
        query = "&".join(["{}={}".format(k, parse.quote(str(params[k]))) for k in sorted(params.keys())])
        payload = [method, host_url, request_path, query]
        payload = "\n".join(payload)
        payload = payload.encode(encoding="utf8")
        secret_key = self._secret_key.encode(encoding="utf8")
        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature
