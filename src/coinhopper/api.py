import os
import requests
import json
import asyncio
import hashlib
import hmac
from urllib.parse import urljoin, urlencode

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_BASEURL = 'https://api.binance.com'

headers = {
    'X-MBX-APIKEY': BINANCE_API_KEY
}

def get_fiat_balance():
    URL = '/sapi/v1/capital/config/getall'
    params = {
        'timestamp': get_server_time()
    }
    query_string = urlencode(params)
    params['signature'] = hmac.new(
        BINANCE_API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    try:
        response = requests.get(urljoin(BINANCE_BASEURL, URL),
                                headers=headers,
                                params=params)
    except Exception:
        raise Exception("get_fiat_balance(): request failed")
    if response.status_code == 200:
        for i in response.json():
            if i['coin'] == 'USDT':
                return i['free']
    else:
        raise Exception(f"Code {response.status_code} from Binance, {response.json()}")

def get_biggest_diff(coins):
    data = {}
    for coin in coins:
        price, avg_price = get_coin_cur_and_avg_price(coin)
        data[coin] = avg_price / cur_price

    filtered_data = {}
    for coin in data:
        if data[coin] > 1:
            filtered_data[coin] = data[coin]

    max = 0
    result = None
    for coin in filtered_data:
        if max == 0 or max < filtered_data[coin]:
            max = filtered_data[coin]
            result = coin

    return result

def get_coin_price(coin):
    params = {
        'symbol': coin + 'USDT',
        'interval': '1m',
        'limit': 1
    }
    response = requests.get(BINANCE_BASEURL + '/api/v3/klines',
                            headers=headers,
                            params=params)
    if response.status_code == 200:
        return response.json()[0][4]
    else:
        raise Exception(f"Code {response.status_code} from Binance, {response.json()}")

def get_coin_cur_and_avg_price(coin):
    params = {
        'symbol': coin + 'USDT',
        'interval': '1d',
        'limit': 1
    }
    response = requests.get(BINANCE_BASEURL + '/api/v3/klines',
                            headers=headers,
                            params=params)
    if response.status_code == 200:
        avg_price = (float(response.json()[0][2]) +
                     float(response.json()[0][3])) / 2
        cur_price = get_coin_price(coin)
        return float(cur_price), float(avg_price)
    else:
        raise Exception(f"Code {response.status_code} from Binance, {response.json()}")

def buy(coin, fiat_balance):
    URL = '/api/v3/order'
    timestamp = get_server_time()
    params = {
        'symbol': coin + 'USDT',
        'side': 'BUY',
        'type': 'MARKET',
        'quoteOrderQty': fiat_balance,
        'timestamp': timestamp
    }

    query_string = urlencode(params)
    params['signature'] = hmac.new(
        BINANCE_API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    try:
        response = requests.post(urljoin(BINANCE_BASEURL, URL),
                                 headers=headers,
                                 params=params)
    except Exception:
        raise Exception("buy(): request failed")
    if response.status_code == 200:
        if response.json()['status'] == 'FILLED':
            return float(response.json()['executedQty'])
        else:
            return 0
    else:
        raise Exception(f"Code {response.status_code} from Binance, {response.json()}")

def sell(coin, amount_bought):
    URL = '/api/v3/order'
    timestamp = get_server_time()
    params = {
        'symbol': coin + 'USDT',
        'side': 'SELL',
        'type': 'MARKET',
        'quantity': amount_bought,
        'timestamp': timestamp
    }

    query_string = urlencode(params)
    params['signature'] = hmac.new(
        BINANCE_API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    try:
        response = requests.post(urljoin(BINANCE_BASEURL, URL),
                                 headers=headers,
                                 params=params)
    except Exception:
        raise Exception("sell(): request failed")
    if response.status_code == 200:
        return True
    else:
        raise Exception(f"Code {response.status_code} from Binance, {response.json()}")

def get_server_time():
    URL = '/api/v3/time'
    try:
        response = requests.get(urljoin(BINANCE_BASEURL, URL),
                                headers=headers)
    except Exception:
        raise Exception("get_server_time(): request failed")
    if response.status_code == 200:
        return response.json()['serverTime']
    else:
        raise Exception(f"Code {response.status_code} from Binance, {response.json()}")
