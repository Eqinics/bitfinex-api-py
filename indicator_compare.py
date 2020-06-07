import os
import sys
import asyncio
import time
sys.path.append('../../../')

from bfxapi import Client

bfx = Client(
  logLevel='DEBUG',
)

now = int(round(time.time() * 1000))
then = now - (1000 * 60 * 60 * 24 * 1) # 1 day ago

SYMBOL = ['tBTCUSD' , 'tETHUSD', 'tLTCUSD'] #3 coins are supported

s=0

def file_read(row,symbol):
    if symbol == 'tBTCUSD':
        filename= 'BTC_indicators.txt'

    elif symbol == 'tETHUSD':
        filename= 'ETH_indicators.txt'

    elif symbol == 'tLTCUSD':
        filename= 'LTC_indicators.txt'

    with open(filename, 'r') as file_object:
        data=file_object.readlines()

async def log_last_candles_1min():
    for s in range(len(SYMBOL)):
        candlesrt = await bfx.rest.get_public_candles(SYMBOL[s], 0, then, section='last', tf='1m') #Default candle duration is 1 min
        print (SYMBOL[s], candlesrt[2])

async def run():
    await log_last_candles_1min()

t = asyncio.ensure_future(run())
asyncio.get_event_loop().run_until_complete(t)
