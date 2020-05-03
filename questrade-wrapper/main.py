import call
import refresh
import summary
import numpy as np
import matplotlib.pyplot as plt
import csv
from csv import writer
import sys
from datetime import date
import requests

def calls():
    arguments = ["get_asset_information", "get_type", "assign_new_type 'ticker' 'type'", 'etc.']
    for arg in arguments:
        print(arg)

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
        fileName = './info/assetType.txt'
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

def build_graph(labels, sizes):
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
        build_graph(labels, sizes)
    elif(type_ == 'Sector'):
        labels = get_type()[0]
        sizes = get_type()[1]
        build_graph(labels, sizes)
    else:
        print("ERROR")

def assign_new_type(symbol, sector):
    fileName = './info/assetType.txt'   
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
    with open('./info/overall_history.csv', 'a') as file_:
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

def portfolio():
    assets = get_asset_information()[0]
    for asset in assets:
        print("-----------------")
        summary.print_info(asset)



n = len(sys.argv)
arg_arr = []
for i in range(0, n):
    arg_arr.append(sys.argv[i])
    

if __name__ == '__main__':
    try:
        if len(sys.argv) == 4:
            print(globals()[sys.argv[1]](sys.argv[2], sys.argv[2]))
        elif len(sys.argv) == 3:
            print(globals()[sys.argv[1]](sys.argv[2]))
        elif len(sys.argv) == 2:
            if sys.argv[1] == 'refresh':
                refresh.activate_refresh_key()
            else:
                print(globals()[sys.argv[1]]())
        else:
            print("ERROR - No valid argument given, please choose one of the following:")
            calls()
    except:
        print("ERROR - Invalid argument given, please choose one of the following:")
        calls()