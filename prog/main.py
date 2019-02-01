# общие библиотеки
import datetime
import sys

# библиотеки сообщества
from binance_api import Binance

# мои библиотеки
import bFunc




# исходные данные ----------------

# интересующая валюта
sBase = 'BNB'

# # валютная пара 
# sPair = 'XLMUSDC'

# количество интервалов для анализа
iLimit = 360
# интервал 
sInterval = '2h'
# количество результатов для выдачи
iCountPrint = 5
# минимальное количество сделок
iCountTrade = 4


print(f'Запускаем анализ всех пар по валюте {sBase}. Выводы в estimation.txt \n')


# будем писать в файл

sys.stdout = open('estimation.txt','wt',encoding='utf-8')


# подключаемся к бирже
bot = Binance(
    API_KEY='D7...Ejj',
    API_SECRET='gwQ...u3A'
)



#  интересующие пары 
lPairs = []


# данные по торгуемым парам

lExchangeInfo = bot.exchangeInfo()
iCountPair = 0
lTicker = []
for lEI in lExchangeInfo['symbols']:
    # print(lEI)
    # print(lEI['status'])
    if (lEI['status'] == 'TRADING') and ((lEI['baseAsset']==sBase) or (lEI['quoteAsset']==sBase)) :
        lTicker24h = bot.ticker24hr(symbol=lEI['symbol'])
        if lEI['baseAsset']==sBase:
            lPairs.append([lEI['symbol'], lEI['baseAsset'], lEI['quoteAsset'], float(lTicker24h['volume']) ])    
        else:
            lPairs.append([lEI['symbol'], lEI['baseAsset'], lEI['quoteAsset'], float(lTicker24h['quoteVolume']) ])    
lPairs.sort(key=lambda ii: ii[3],reverse=True)

for lPair in lPairs:
    iCountPair +=1
    print(f'№ {iCountPair:03d} Пара: {lPair[0]:10s} Оборот за 24h: {lPair[3]: 15.2f}{sBase}')    
    #  данные с биржи по свечам
    slKLines = bot.klines(
        symbol=lPair[0],
        interval=sInterval,
        limit=iLimit)
    # вычисляем !!!
    bFunc.estimationPair(slKLines,lPair[0],iLimit,sInterval,iCountPrint,iCountTrade)
