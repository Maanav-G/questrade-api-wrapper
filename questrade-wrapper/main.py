import call
import numpy as np
import matplotlib.pyplot as plt
import csv
from csv import writer
import sys
from datetime import date
import requests

def get_asset_information():
    call_to_make = 'accounts/' + call.id_ + '/positions'
    positions = call.get_(call_to_make)['positions']
    labels = []
    marketVal = []
    for position in positions:
        symbol = position['symbol']
        value = position['currentMarketValue']
        labels.append(symbol)
        marketVal.append(value)
    total = 0
    for val in marketVal:
        total = total + val
    sizes = []
    for val in marketVal:
        x = val/total
        sizes.append(x)
    array = np.array([labels, sizes, marketVal])
    return array

def get_type():
    arr = get_asset_information()
    symbols = arr[0]
    prices = arr[2]

    Consumer = 0
    Tech = 0
    ETF = 0
    RealEstate = 0
    Util = 0
    Other = 0
    Unidentified = 0

    i = 0
    while i < len(symbols):
        symbol = symbols[i]
        price = prices[i]
        fileName = 'assetType.txt'
        accessMode = 'r'
        sector = ''
        with open(fileName, accessMode) as myCSVfile:
            dataFromFile = csv.reader(myCSVfile, delimiter="=")
            for row in dataFromFile:
                if(symbol == row[0]):
                    sector = row[1]
            myCSVfile.close()   

        if(sector == 'Consumer'):
            Consumer = Consumer + float(price) 
        elif(sector == 'Tech'):
            Tech = Tech + float(price) 
        elif(sector == 'ETF'):
            ETF = ETF + float(price) 
        elif(sector == 'RealEstate'):
            RealEstate = RealEstate + float(price) 
        elif(sector == 'Util'):
            Util = Util + float(price) 
        elif(sector == 'Other'):
            Other = Other + float(price) 
        else:
            Unidentified = Unidentified + float(price)
                    
        i+=1

    arrLabels = ['Consumer', 'Tech', 'ETF', 'RealEstate', 'Util', 'Other', 'Unidentified']
    arrPercentage = [Consumer, Tech, ETF, RealEstate, Util, Other, Unidentified]
    array = np.array([arrLabels, arrPercentage])
    return array

def plot_(labels, sizes):
    colors = []
    i = 0
    while i < len(labels):
        if (i % 2 == 0):
            colors.append('grey')
        else:
            colors.append('white')
        i += 1
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.show()

def plot(type_):
    if(type_ == 'Position'):
        labels = get_asset_information()[0]
        sizes = get_asset_information()[1]
        plot_(labels, sizes)
    elif(type_ == 'Sector'):
        labels = get_type()[0]
        sizes = get_type()[1]
        plot_(labels, sizes)
    else:
        print("ERROR")

def assign_new_type(symbol, sector):
    fileName = 'assetType.txt'   
    to_add = symbol + '=' + sector
    with open(fileName, 'a') as myCSVfile:
        myCSVfile.write(to_add)     

def prices_CAD():
    symbols = get_asset_information()[0]
    marketVal = get_asset_information()[2]
    USDCAD = get_exchange_rate('USD')
    i = 0
    converted_marketVal = []
    while i < len(symbols):
        symbol = symbols[i]
        val = marketVal[i]
        symbol_info = call.get_('symbols/search?prefix='+symbol)['symbols'][0]
        if(symbol_info['currency'] == 'USD'):
            converted_val = val * USDCAD
        elif(symbol_info['currency'] == 'CAD'):
            converted_val = val
        else:
            converted_val = val
        converted_marketVal.append(converted_val)
    


    array_to_return = np.array([symbols, converted_marketVal])
    return array_to_return
    
def overall_portfolio():
    totalEquity = float(call.get_('accounts/' + call.id_ + '/balances')['combinedBalances'][0]['totalEquity'])
    marketValue = float(call.get_('accounts/' + call.id_ + '/balances')['combinedBalances'][0]['marketValue'])
    cash = float(call.get_('accounts/' + call.id_ + '/balances')['combinedBalances'][0]['cash'])
    return totalEquity, marketValue, cash

def add_todays_totals():
    marketValue = overall_portfolio()[1]
    cash = overall_portfolio()[2]
    today = date.today()
    to_add = [today, marketValue, cash]
    with open('overall_history.csv', 'a') as file_:
        writer = csv.writer(file_)
        writer.writerow(to_add)

def get_exchange_rate(base):
    uri = 'https://api.exchangeratesapi.io/latest'
    r = requests.get(uri)
    response = r.json()
    EUR_base = float(response['rates'][base])
    EUR_CAD = float(response['rates']['CAD'])
    USD_CAD = EUR_CAD/EUR_base
    return USD_CAD

try:
    if sys.argv[1] == 'refresh':
        call.refresh_()
except:
    pass


x = get_exchange_rate('USD')
print (x)

# add_todays_totals()

# x = ['2020-04-06', '2020-04-07', '2020-04-08', '2020-04-09', '2020-04-10', '2020-04-13']
# # x = [0, 1, 2, 3, 4, 5]
# y1 = [13585.65, 14995.65, 15085.65, 17585.65, 17100.65, 18985.65]
# y2 = [3108.27, 3108.27, 3108.27, 3108.27, 3108.27, 3108.27]
# y_comb = np.array([y1, y2])
# y_stack = np.cumsum(y_comb, axis=0)

# print(y_comb)
# print(y_stack)
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.fill_between(x, 0, y_stack[0,:], facecolor="#CC6666", alpha=.7)
# ax1.fill_between(x, y_stack[1,:], y_stack[0,:], facecolor="#1DACD6", alpha=.7)
# plt.show()























# def plot_asset_allocation(type_):
#     array = get_asset_information()
#     if(type_ == 'position'):
#         labels = array[0]
#         sizes = array[1]
#         explode = []
#         colors = []
#         i = 0

#         for size in sizes:
#             if(float(size) < 0.05):
#                 explode.append(0.2)
#             else: 
#                 explode.append(0.4)
#             if (i % 2 == 0):
#                 colors.append('grey')
#             else:
#                 colors.append('black')
#             i += 1
#         plt.pie(sizes, labels=labels, colors=colors, explode=explode,
#         autopct='%1.1f%%', startangle=140)
#         plt.axis('equal')
#         plt.show()
#     if(type_ == 'sector'):
#         print("sector")