import os
import sys
import asyncio
import time
sys.path.append('../../../')

from bfxapi import Client

try:
    os.remove('BTC_indicators.txt')
    os.remove('ETH_indicators.txt')
    os.remove('LTC_indicators.txt')
except:
    pass

bfx = Client(
  logLevel='DEBUG',
)


now = int(round(time.time() * 1000))
then = now - (1000 * 60 * 60 * 24 * 1) # 1 day ago

SYMBOL = ['tBTCUSD' , 'tETHUSD', 'tLTCUSD']

s=0

def file_write(row,symbol):
    if symbol == 'tBTCUSD':
        filename= 'BTC_indicators.txt'

    elif symbol == 'tETHUSD':
        filename= 'ETH_indicators.txt'

    elif symbol == 'tLTCUSD':
        filename= 'LTC_indicators.txt'

    with open(filename, 'a+') as file_object:
        #Move read cursor to the start of the file.
        file_object.seek(0)
        #If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        #Append text at the end of file
        file_object.write(row)

async def log_hist_candles_1day():
    for s in range(len(SYMBOL)):
        candles = await bfx.rest.get_public_candles(SYMBOL[s], 0, then, section='hist', tf='1D', limit='100') #Default candle duration is 1 min
        print (SYMBOL[s])

        i = 0
        total = 0
        series = list()

        for c in candles:
            i+=1

            series.append(c[2])
            total = total+c[2]

            if i == 7:
                ma7=str(total/7)
                print('MA7: ', total/7)
                file_write(ma7, SYMBOL[s])
            elif i == 25:
                ma25=str(total/25)
                print('MA25: ', total/25)
                file_write(ma25, SYMBOL[s])
            if i == 99:
                ma99=str(total/99)
                print('MA99: ', total/99)
                file_write(ma99, SYMBOL[s])

async def run():
    await log_hist_candles_1day()

t = asyncio.ensure_future(run())
asyncio.get_event_loop().run_until_complete(t)
