

def getSlResult(slLines,fPriceBuyF,fPriceSellF):
    # 1- Анализируемый список slLines
    # 2- Цена покупки fPriceBuyF
    # 3- Цена продажи fPriceSellF


    # флаг текущего состояния
    #       готовность покупать - False
    #       готовность продавать - True
    bFlOperation = False
    # прибыль
    fProfit = 0.00
    # количество сделок
    fDeal = 0.0
    # оборот
    # fTurnover = 0.0

    for slLine in slLines:
        if not bFlOperation :
            if ( float(slLine[3]) <= fPriceBuyF ) and (float(slLine[2]) >= fPriceBuyF):
                # покупка
                bFlOperation = True
                fDeal += 0.5
        else:
            if ( float(slLine[3]) <= fPriceSellF ) and (float(slLine[2]) >= fPriceSellF) and (fPriceSellF>fPriceBuyF):
                # продажа
                bFlOperation = False
                fDeal += 0.5
                fProfit +=  1000 / fPriceBuyF * fPriceSellF  - 1000
    # переводим в проценты
    fProfit = fProfit/1000 * 100
    
    return [fProfit,fPriceBuyF,fPriceSellF,fDeal]


def printResults (spResultsF,iVersionF,fPriceMinF,fPriceMaxF,iCountPrintF,iCountTradeF):
    # Сортируем по максиму прибыли
    spResultsF.sort(key=lambda ii: ii[0])
    # Выводим результирующие данные
    print(f'{iVersionF} вариантов. Разброс цены: {fPriceMinF:.8f} - {fPriceMaxF:.8f}')

    print (f'\nАбсолютный рейтинг из {iCountPrintF} позиций по прибыли:')
    i=iVersionF
    iTmpCountPrint = iCountPrintF
    while (i>0) and (iTmpCountPrint>0):
        i-=1
        iTmpCountPrint-=1
        print(f"{iVersionF-i} - {(spResultsF[i][0]):.2f}% {(spResultsF[i][3]):.1f} сделок покупка:{(spResultsF[i][1]):4.8f}  продажа:{(spResultsF[i][2]):4.8f}")
    
    print (f'\nРейтинг из {iCountPrintF} позиций минимум {iCountTradeF} сделок по прибыли:')
    i=iVersionF
    iTmpCountPrint = iCountPrintF
    while (i>0) and (iTmpCountPrint>0):
        i-=1
        if spResultsF[i][3] >= iCountTradeF :
            iTmpCountPrint-=1
            print(f"{iVersionF-i} - {(spResultsF[i][0]):.2f}% {(spResultsF[i][3]):.1f} сделок покупка:{(spResultsF[i][1]):4.8f}  продажа:{(spResultsF[i][2]):4.8f}")


    print (f'\nРейтинг из {iCountPrintF} позиций среди закрытых сделок по прибыли:')
    i=iVersionF
    iTmpCountPrint = iCountPrintF
    while (i>0) and (iTmpCountPrint>0):
        i-=1
        if int(spResultsF[i][3]) == (spResultsF[i][3]) :
            iTmpCountPrint-=1
            print(f"{iVersionF-i} - {(spResultsF[i][0]):.2f}% {(spResultsF[i][3]):.1f} сделок покупка:{(spResultsF[i][1]):4.8f}  продажа:{(spResultsF[i][2]):4.8f}")

    # сортируем по максимальному количеству сделок
    spResultsF.sort(key=lambda ii: ii[3])
    print (f'\nАбсолютный рейтинг из {iCountPrintF} позиций по кол-ву сделок:')
    i=iVersionF
    iTmpCountPrint = iCountPrintF
    while (i>0) and (iTmpCountPrint>0):
        i-=1
        iTmpCountPrint-=1
        print(f"{iVersionF-i} - {(spResultsF[i][0]):.2f}% {(spResultsF[i][3]):.1f} сделок покупка:{(spResultsF[i][1]):4.8f}  продажа:{(spResultsF[i][2]):4.8f}")

    print (f'\nРейтинг из {iCountPrintF} позиций среди закрытых сделок по кол-ву сделок:')
    i=iVersionF
    iTmpCountPrint = iCountPrintF
    while (i>0) and (iTmpCountPrint>0):
        i-=1
        if int(spResultsF[i][3]) == (spResultsF[i][3]) :
            iTmpCountPrint-=1
            print(f"{iVersionF-i} - {(spResultsF[i][0]):.2f}% {(spResultsF[i][3]):.1f} сделок покупка:{(spResultsF[i][1]):4.8f}  продажа:{(spResultsF[i][2]):4.8f}")
    
    print ('\n')
    return


def estimationPair(slKLinesF,sPairF,iLimitF,sIntervalF,iCountPrintF,iCountTradeF):
    # список свечей slKLinesF
    # валютная пара: sPair = 'LTCBTC'
    # количество интервалов для анализа: iLimit = 360
    # интервал: sInterval = '2h'
    # количество результатов для выдачи: iCountPrint = 5
    # минимальное количество сделок: iCountTrade = 4

    print(f'Интервал: {sIntervalF}. Значений: {iLimitF}.')
    # минимальная цена за весь период для покупки
    fPriceMin = 99999999999999999.0
    # максимальная цена за весь период для продажи
    fPriceMax = 0.0
    # уровни покупок
    spBuy  = []
    # уровни продаж
    spSell = []
    # счетчик
    i=0

    for slKLine in slKLinesF:
        i+=1
        # print(i,datetime.datetime.fromtimestamp(int(slKLine[0]) / 1e3),'buy:',slKLine[3],'sell',slKLine[2],'volume',slKLine[7],'Сделок',slKLine[8])
        spBuy.append(float(slKLine[3]))
        spSell.append(float(slKLine[2]))


        if float(slKLine[3]) < fPriceMin:
            fPriceMin = float(slKLine[3])

        if float(slKLine[2]) > fPriceMax:
            fPriceMax = float(slKLine[2])

    # результирующий список
    # 1 - прибыль
    # 2 - покупка
    # 3 - продажа
    # 4 - количество сделок
    spResults = []
    # номер варианта
    iVersion = 0
    j = i
    while i>0:
        i-=1
        iTmp = j
        while j>0:
            j-=1
            spTmp = getSlResult(slKLinesF,float(spBuy[i]),float(spSell[j]))
            if spTmp[0]!=0.0:
                spResults.append(spTmp)
                iVersion += 1
        j = iTmp

    printResults (spResults,iVersion,fPriceMin,fPriceMax,iCountPrintF,iCountTradeF)
    return