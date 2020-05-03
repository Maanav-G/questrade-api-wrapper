import call

def symb_search_ticker(ticker):
    rest_op = "symbols/search?prefix=" + ticker
    return call.get_(rest_op)['symbols'][0]

def symb_search_id(id):
    rest_op = "symbols/" + id
    return call.get_(rest_op)

def symb_information(ticker):
    ticker_id = str(symb_search_ticker(ticker)['symbolId'])
    info = symb_search_id(ticker_id)


    return info['symbols'][0]

def print_info(ticker):
    x = symb_information(ticker)
    print(x['symbol'])
    print(x['description'])
    print(x['prevDayClosePrice'])
    print(x['currency'])
    print(x['dividend'])








