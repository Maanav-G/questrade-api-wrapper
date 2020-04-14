# Questrade API Wrapper

This is a custom Python wrapper for the [Questrade API](https://www.questrade.com/api/documentation/getting-started) that I built this to analyze and retrive key information from my personal Questrade Trading Account.

## Functions

Currently it supports the following functions:

`get_(rest_opr)` - Calls any applicable [Rest Operation](https://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-activities) and returns it in a JSON format

`refresh_()` - Calls the current 'Refresh Token' to refresh the Access Token, API Server and new Refresh Token which are saved in a config file (used when Access Token expires)

`get_asset_information()` - Retrieves basic information for each asset in portfolio (Symbol, Market Value, Price and Quantity)

`get_type()` - Pulls and assigns 'Sector' (Tech, Consumer, Util, etc.) type to each owned asset in portfolio from saved list

`assign_new_type()` - Assigns a specific 'Sector' (Tech, Consumer, Util, etc.) to a symbol and adds to a saved list

`prices_CAD()` - Converts Market Value of each owned asset from respective currency to CAD

`overall_portfolio()` - Retrieves overall information of the portfolio (Equity, Market Value and Cash) and stores in datasets

`add_todays_totals()` - Retrieves information from 'overall_portfolio()' and adds to a day-by-day portfolio history CSV file


## Upcoming
- Build out more common functions - Ex. get ticker information, get history of ticker, etc.
- Design and implement an aesthetically pleasing UI 
- Add plotting functions for pie graphs, line graphs, stacked graphs, etc.
- Host an interactive version on a web app connected to a mock/practice account

