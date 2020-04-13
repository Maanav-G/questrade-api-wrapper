import call
import numpy as np
import matplotlib.pyplot as plt

def get_asset_information():
    balances = call.get_('accounts/' + call.id_ + '/balances')
    call_to_make = 'accounts/' + call.id_ + '/positions'
    positions = call.get_(call_to_make)['positions']
    labels = []
    price = []
    for position in positions:
        symbol = position['symbol']
        value = position['currentMarketValue']
        labels.append(symbol)
        price.append(value)
    total = 0
    for val in price:
        total = total + val
    sizes = []
    for val in price:
        x = val/total
        sizes.append(x)
    array = np.array([labels, sizes])
    return array

def plot_asset_allocation(type_):
    array = get_asset_information()
    if(type_ == 'position'):
        labels = array[0]
        sizes = array[1]
        explode = []
        colors = []
        i = 0
        for lab in labels: 
            print(lab)
        for size in sizes:
            if(float(size) < 0.05):
                explode.append(0.2)
            else: 
                explode.append(0.4)
            if (i % 2 == 0):
                colors.append('grey')
            else:
                colors.append('black')
            i += 1
        plt.pie(sizes, labels=labels, colors=colors, explode=explode,
        autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.show()
    if(type_ == 'sector'):
        print("sector")

def assign_new_type(symbol, type_):
    x = []
    array = get_asset_information()
    arr = array[0]
    n = -1
    for sym in arr:
        if (sym == symbol):
            print('already exists')
            n = 0
    if (n == -1):
        x.append(type_)

