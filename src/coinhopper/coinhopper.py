#!python3

import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
import aiohttp
import requests
import json
from coinhopper import api


logging.basicConfig(level=logging.INFO)

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_BASEURL = 'https://api.binance.com'
COINS = os.getenv("COINS")

headers = {
    'X-MBX-APIKEY': BINANCE_API_KEY
}

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)

async def run():
    await bot.send_message(TELEGRAM_CHAT_ID, 'coinhopper started')
    coin = None

    while True:
        if not coin:
            fiat_balance = api.get_fiat_balance()
            coin = api.get_biggest_diff(COINS.split(','))
            amount_bought = api.buy(coin, fiat_balance)
            if amount_bought == 0:
                coin = None
                await bot.send_message(
                    TELEGRAM_CHAT_ID,
                    'error: failed to buy'
                )
            else:
                await bot.send_message(
                    TELEGRAM_CHAT_ID,
                    f"bought {amount_bought} {coin} for ${int(fiat_balance)}"
                )
        else:
            price, avg_price = api.get_coin_cur_and_avg_price(coin)
            if price > avg_price:
                await bot.send_message(
                    TELEGRAM_CHAT_ID,
                    'will try to sell'
                )
                api.sell(coin, amount_bought)
                await bot.send_message(
                    TELEGRAM_CHAT_ID,
                    'successfully sold'
                )
                coin = None
                await bot.send_message(
                    TELEGRAM_CHAT_ID,
                    f"sold {amount_bought} {coin}"
                )
        await asyncio.sleep(900)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
