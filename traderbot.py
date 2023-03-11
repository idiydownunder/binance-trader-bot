#!/bin/python3

#=====================================================================
#
#  Copyright (c) 2023 iDIY Down Under
#  Author: Julian Carmichael (aka Digital Jester)
#
#  This work is licensed under a Creative Commons 
#  Attribution-NonCommercial-ShareAlike 4.0 International License
#  http://creativecommons.org/licenses/by-nc-sa/4.0/
#
#=====================================================================

#=============================================
# Import Libaries
#=============================================
import os
import sys
import time
import datetime
import math
import json
from colorama import Fore, Back, Style
from binance.client import Client
from binance.exceptions import BinanceAPIException

#=============================================
# Set some 'constants'
#=============================================
CONFIG_FILE = 'config.json'
PRICE_LIST = 'price_guard.json'
ASCII_LOGO=Fore.YELLOW + "__________.__\n\______   \__| ____ _____    ____   ____  ____\n |    |  _/  |/    \\\\__  \  /    \_/ ___\/ __ \\\n |    |   \  |   |  \/ __ \|   |  \  \__\  ___/\n |______  /__|___|  (____  /___|  /\___  >___  >\n        \/        \/     \/     \/     \/    \/" + Style.RESET_ALL + Fore.GREEN + "\n               _____            _           ___      _\n              |_   _| _ __ _ __| |___ _ _  | _ ) ___| |_\n                | || '_/ _` / _` / -_) '_| | _ \/ _ \  _|\n                |_||_| \__,_\__,_\___|_|   |___/\___/\__|\n\n" + Style.RESET_ALL

#=============================================
# Define timeframe
#=============================================

#timeframe = Client.KLINE_INTERVAL_15MINUTE # Less gains More Trades
#timeframe = Client.KLINE_INTERVAL_30MINUTE
#timeframe = Client.KLINE_INTERVAL_1HOUR
#timeframe = Client.KLINE_INTERVAL_2HOUR
timeframe = Client.KLINE_INTERVAL_4HOUR
#timeframe = Client.KLINE_INTERVAL_6HOUR
#timeframe = Client.KLINE_INTERVAL_8HOUR
#timeframe = Client.KLINE_INTERVAL_12HOUR
#timeframe = Client.KLINE_INTERVAL_1DAY 
#timeframe = Client.KLINE_INTERVAL_3DAY # More gains Less Trades

#=============================================
# Set some default values for just incase
#=============================================
sma_short_period = 7
sma_medium_period = 25
sma_long_period = 99
trade_timer = 60*60
connection_retry_count=0

#=============================================
# Define some functions
#=============================================
def get_timestamp_string():
    stamp=datetime.datetime.now()
    string=f"[{stamp.strftime('%x')} {stamp.strftime('%X')}] "
    return string

def get_system_mark_string():
    string=Fore.BLACK + Back.LIGHTBLUE_EX + "[SYS]" + Style.RESET_ALL + " "
    return string

def get_error_mark_string():
    string=Fore.BLACK + Back.RED + "[ERR]" + Style.RESET_ALL + " "
    return string

def get_sma(symbol, timeframe, period):
    # Calculate simple moving average for a given symbol and timeframe
    klines = client.get_historical_klines(symbol, timeframe, "100 days ago")
    closes = [float(kline[4]) for kline in klines]
    sma = sum(closes[-period:]) / period
    return sma

def log_to_file(file,log_data):
    # Log data to a file
    f = open(file, "a")
    f.write(log_data)
    f.close()

def make_trade(coin_pair,buy_sell,order_type,order_qty):
    # Create an order
    trade = client.create_order(
        symbol=coin_pair,
        side=buy_sell,
        type=order_type,
        quoteOrderQty=float(order_qty),
    )
    return trade

# Clear the screen/terminal
os.system('cls' if os.name == 'nt' else 'clear')
# Display something nice
print(ASCII_LOGO)

# Error Checking
if os.path.isfile(CONFIG_FILE):
    # Load Config.json
    with open(CONFIG_FILE) as f:
        settings = json.load(f)
        config_load_time=time.time()
else:
    # Handle Error
    sys.exit(f"ERROR: {CONFIG_FILE} Not Found! Terminating Program.")
    
# Error Checking
if os.path.isfile(PRICE_LIST):
    # Load PRICE_LIST
    with open(PRICE_LIST) as f:
        price_guard = json.load(f)
else:
    # Handle Error
    price_guard={}

# Set moving average periods
if (settings['sma_medium_period']>settings['sma_short_period']) & (settings['sma_long_period']>settings['sma_medium_period']):
    sma_short_period = settings['sma_short_period']
    sma_medium_period = settings['sma_medium_period']
    sma_long_period = settings['sma_long_period']

# Set trading timer
if settings['trade_timer_minutes']>=1:
    trade_timer = settings['trade_timer_minutes']*60
timer=-trade_timer

# Initialize Binance Client
print(get_timestamp_string() + get_system_mark_string() + "Initialize Binance Client.")
client = Client(settings['api_key'], settings['api_secert_key'])

while True:
    try:
        #=============================================
        # Check config.json Change
        #=============================================
        if os.path.getmtime(CONFIG_FILE)>config_load_time:
            print(get_timestamp_string() + get_system_mark_string() + f"{CONFIG_FILE} has changed! Applying new changes...")

            # Close Binance client
            print(get_timestamp_string() + get_system_mark_string() + f"Stopping Binance client.")
            client.close_connection()

            with open(CONFIG_FILE) as f:
                settings = json.load(f)
                config_load_time=time.time()
            
            # Set moving average periods
            if (settings['sma_medium_period']>settings['sma_short_period']) & (settings['sma_long_period']>settings['sma_medium_period']):
                sma_short_period = settings['sma_short_period']
                sma_medium_period = settings['sma_medium_period']
                sma_long_period = settings['sma_long_period']
            else:
                sma_short_period = 7
                sma_medium_period = 25
                sma_long_period = 99

            # Set trading timer
            if settings['trade_timer_minutes']>=1:
                trade_timer = settings['trade_timer_minutes']*60
            else:
                trade_timer = 60*60

            print(get_timestamp_string() + get_system_mark_string() + f"All {CONFIG_FILE} changes have been applied!")

            # Initialize Binance Client
            print(get_timestamp_string() + get_system_mark_string() + "Initialize Binance Client.")
            client = Client(settings['api_key'], settings['api_secert_key'])

        #=============================================
        # Check Network Connection
        #=============================================
        if format(client.ping()) == "{}":
            if connection_retry_count>0:
                print(get_timestamp_string() + get_system_mark_string() + "Network Connection Good.")
            connection_retry_count=0

        if time.time()-timer>=trade_timer: # Check The Timer
            timer=time.time() # Set The Timer
            #=============================================
            # Start Checking Markets
            #=============================================
            print(get_timestamp_string() + get_system_mark_string() + "Checking crypto markets.")
            # Reset Price Guard update Flag
            price_guard_update=False
            for tp in settings['trading_pairs']:
                #=============================================
                # Get Market Data Needed For Trading
                #=============================================
                # Define trading pair
                symbol = f"{tp['coin']}{tp['fiat']}"
                # Get current price, moving averages, wallet balances and coin info
                ticker = client.get_symbol_ticker(symbol=symbol)
                price = float(ticker['price'])
                sma_short = round(get_sma(symbol, timeframe, sma_short_period),4)
                sma_medium = round(get_sma(symbol, timeframe, sma_medium_period),4)
                sma_long = round(get_sma(symbol, timeframe, sma_long_period),4)
                fiat_balance = client.get_asset_balance(tp['fiat'])
                coin_balance = client.get_asset_balance(tp['coin'])
                coin_info = client.get_symbol_info(symbol)

                # Make Price adjustments
                if tp['trade_buy_price_adjustment']!=0:
                    buy_price = round(sma_long - tp['trade_buy_price_adjustment'],4)
                else:
                    buy_price = sma_short-0.0001
                if tp['trade_sell_price_adjustment']!=0:
                    sell_price = round(sma_long + tp['trade_sell_price_adjustment'],4)
                else:
                    sell_price=sma_short+0.0001
                # Make adjustment for Price Guard if enabled.    
                if tp['trade_price_guard']:
                    g_price=price_guard.get(symbol, None)
                    if g_price is not None:
                        if sell_price<round(g_price + tp['trade_sell_price_adjustment'],4):
                            sell_price = round(g_price + tp['trade_sell_price_adjustment'],4)

                #=============================================
                # Print Market Data, If Needed
                #=============================================
                if settings['show_markets']:
                    # Add to output strings
                    output="Trading: "
                    if tp['trade_enable']:
                        if tp['trade_buy_enable'] & tp['trade_sell_enable']:
                            output+=Fore.GREEN + "BUY & SELL" + Style.RESET_ALL
                        if tp['trade_buy_enable'] & tp['trade_sell_enable']==False:
                            output+=Fore.GREEN + "BUY ONLY" + Style.RESET_ALL
                        if tp['trade_buy_enable']==False & tp['trade_sell_enable']:
                            output+=Fore.GREEN + "SELL ONLY" + Style.RESET_ALL
                        if tp['trade_buy_enable']==False & tp['trade_sell_enable']==False:
                            output+=Fore.RED + "BUY & SELL DISABLED" + Style.RESET_ALL
                    else:
                        output+=Fore.RED + "DISABLED" + Style.RESET_ALL
                    
                    print(get_timestamp_string() + Fore.WHITE + Back.BLUE + "[MKT]" + Style.RESET_ALL + f" {tp['coin']}/{tp['fiat']} Price: {price} {output}\n" + " " * 26 + f"MA({sma_short_period}):{sma_short} MA({sma_medium_period}):{sma_medium} MA({sma_long_period}):{sma_long}\n" + " " * 26 + f"Sell: {sell_price}  Buy: {buy_price}")

                # Start trading
                if tp['trade_enable']:
                    #=============================================
                    # Try To Buy
                    #=============================================
                    if tp['trade_buy_enable']:
                        do_buy=False
                        # Buy when price is below short-term SMA and short-term SMA is below long-term SMA
                        if (price < sma_short) & (sma_short < sma_medium) & (sma_medium < sma_long) & (price <= buy_price):
                            do_buy=True
                        if (price < sma_short) & (sma_short < sma_long) & (sma_medium > sma_long) & (price <= buy_price):
                            do_buy=True
                        if do_buy==True:
                            # Check if we have any position to buy
                            if float(fiat_balance['free'])-tp['fiat_hold_amount'] >= float(coin_info['filters'][2]['minNotional']):  # minimum order amount on Binance is 10 AUD
                                if tp['trade_buy_adjustment']>1:
                                    qty=math.floor(float(coin_info['filters'][2]['minNotional']) * tp['trade_buy_adjustment'])  # Add a % to min trade amount for buy. 
                                elif (tp['trade_buy_adjustment']<1) & (tp['trade_buy_adjustment']>0):
                                    qty=math.floor(float(coin_info['filters'][2]['minNotional']) / tp['trade_buy_adjustment'])  # Add a % to min trade amount for buy.
                                elif tp['trade_buy_adjustment']==1:
                                    qty=float(fiat_balance['free'])-tp['fiat_hold_amount'] # Use all avalibal balance
                                elif tp['trade_buy_adjustment']==0:
                                    qty=float(coin_info['filters'][2]['minNotional']) # Use min trade amount
                                else:
                                    qty=float(coin_info['filters'][2]['minNotional']) # Use min trade amount just incase of bad logic above

                                if qty>float(fiat_balance['free'])-tp['fiat_hold_amount']:
                                    qty=float(coin_info['filters'][2]['minNotional']) # Use min trade amount
                                
                                # Make the trade
                                order = make_trade(symbol,Client.SIDE_BUY,Client.ORDER_TYPE_MARKET,qty)

                                if settings['show_trades']:
                                    # Creat output string
                                    output = get_timestamp_string() + Fore.WHITE + Back.GREEN + "[BUY]" + Style.RESET_ALL + f" {order['executedQty']} {tp['coin']} at {price} {tp['fiat']}"
                                    # Add to output strings
                                    print(output)
                                # Log output to file
                                log_to_file(settings['sales_log_file'],get_timestamp_string() + f"[BUY] {order['executedQty']} {tp['coin']} at {price} {tp['fiat']}\n")

                                # If Price Guard enabled update price if needed
                                if tp['trade_price_guard']:
                                    g_price=price_guard.get(symbol, None)

                                    if g_price is None:
                                        #print('add price')
                                        price_guard[symbol]=price
                                        price_guard_update=True
                                    else:
                                        if price>price_guard[symbol]:
                                            price_guard[symbol]=price
                                            price_guard_update=True
                            else:
                                if settings['show_trades']:
                                    # Creat output string
                                    output = get_timestamp_string() + Fore.WHITE + Back.MAGENTA + "[MIS]" + Style.RESET_ALL + f" Insufficient {tp['fiat']} For {tp['coin']} Buy!"
                                    # Add to output strings
                                    print(output)
                    
                    #=============================================
                    # Try To Sell
                    #=============================================
                    if tp['trade_sell_enable']:
                        do_sell=False
                        # Sell when price is above long-term SMA and short-term SMA is above long-term SMA
                        if (price > sma_short) & (sma_short > sma_medium) & (sma_medium > sma_long) & (price >= sell_price):
                            do_sell=True
                        if (price > sma_short) & (sma_short > sma_long) & (sma_medium < sma_long) & (price >= sell_price):
                            do_sell=True
                        if do_sell:
                            # Check if we have any position to sell
                            if float(coin_balance['free'])-tp['coin_hold_amount'] >= price*float(coin_info['filters'][2]['minNotional']):

                                if tp['trade_sell_adjustment']>1:
                                    qty=math.floor(price*float(coin_info['filters'][2]['minNotional']) / tp['trade_sell_adjustment'])  # Add a % to min trade amount for buy. 
                                elif (tp['trade_sell_adjustment']<1) & (tp['trade_sell_adjustment']>0):
                                    qty=math.floor(price*float(coin_info['filters'][2]['minNotional']) * tp['trade_sell_adjustment'])  # Add a % to min trade amount for buy.
                                elif tp['trade_sell_adjustment']==1:
                                    qty=float(coin_balance['free'])-tp['coin_hold_amount'] # Use all avalibal balance
                                elif tp['trade_sell_adjustment']==0:
                                    qty=price*float(coin_info['filters'][2]['minNotional']) # Use min trade amount
                                else:
                                    qty=price*float(coin_info['filters'][2]['minNotional']) # Use min trade amount just incase of bad logic above

                                if qty>price*(float(coin_balance['free'])-tp['coin_hold_amount']):
                                    qty=price*float(coin_info['filters'][2]['minNotional']) # Use min trade amount just incase of bad logic above (shouldn't happen!)

                                if qty<price*float(coin_info['filters'][2]['minNotional']):
                                    qty=price*float(coin_info['filters'][2]['minNotional']) # Use min trade amount
                                    
                                # Make the trade
                                order = make_trade(symbol,Client.SIDE_SELL,Client.ORDER_TYPE_MARKET,qty)

                                if settings['show_trades']:
                                    # Creat output string
                                    output = get_timestamp_string() + Fore.WHITE + Back.GREEN + "[SOL]" + Style.RESET_ALL + f" {order['executedQty']} {tp['coin']} at {price} {tp['fiat']}"
                                    print(output)
                                # Log output to file
                                log_to_file(settings['sales_log_file'],get_timestamp_string() + f"[SOLD] {order['executedQty']} {tp['coin']} at {price} {tp['fiat']}\n")

                                if tp['trade_price_guard']:
                                    g_price=price_guard.get(symbol, None)
                                    if g_price is not None:
                                        price_guard.pop(symbol)
                                        price_guard_update=True
                            else:
                                if settings['show_trades']:
                                    # Creat output string
                                    output = get_timestamp_string() + Fore.WHITE + Back.MAGENTA + "[MIS]" + Style.RESET_ALL + f" Insufficient {tp['coin']} For {tp['fiat']} Sale!"
                                    # Add to output strings
                                    print(output)

            #=============================================
            # Update Price Guard, If Needed
            #=============================================
            if price_guard_update:
                with open(PRICE_LIST, 'w') as f:
                    json.dump(price_guard, f)     

            #=============================================
            # Print Wallet Balances, If Needed
            #=============================================
            if settings['show_balances']:
                # Setup output strings
                holdings=""
                for tp in settings['trading_pairs']:
                    fiat_balance = client.get_asset_balance(tp['fiat'])
                    coin_balance = client.get_asset_balance(tp['coin'])
                    # Add to output strings
                    if holdings.find(tp['fiat'])==-1:
                        if float(fiat_balance['free']) > 0:
                            holdings+=get_timestamp_string() + Fore.BLACK + Back.YELLOW + f"[BAL]" + Style.RESET_ALL + f" {tp['fiat']} {fiat_balance['free']}\n"
                    if holdings.find(tp['coin'])==-1:
                        if float(coin_balance['free']) > 0:
                            holdings+=get_timestamp_string() + Fore.BLACK + Back.YELLOW + f"[BAL]" + Style.RESET_ALL + f" {tp['coin']} {coin_balance['free']}\n"

                # Print the output
                print(holdings.rstrip("\n"))

    #=============================================
    # Exception/Error Handling
    #=============================================
    except BinanceAPIException as e:
        # Creat output string
        output = f"Binance API error: {e}"
        # Print the output
        print(get_timestamp_string() + get_error_mark_string() + output)
        # Log output to file
        log_to_file(settings['error_log_file'],get_timestamp_string() + output + "\n\n")

    except KeyboardInterrupt:
        print("\n" + get_timestamp_string() + get_system_mark_string() + "Exiting Bot.")
        sys.exit(0)

    except Exception as e:
        #[Errno 11001]
        if "[Errno 11001]" in format(e) or "HTTPSConnectionPool" in format(e):
            if connection_retry_count==0:
                print(get_timestamp_string() + get_error_mark_string() + "Network Connection Error.")
                connection_retry_count+=1
            else:
                print(get_timestamp_string() + get_error_mark_string() + f"Retrying Network Connection. Attempt: {connection_retry_count}")
                connection_retry_count+=1
            time.sleep(30)
        else:
            output=f"Unknown Error: {e}"
            # Print the output
            print(get_timestamp_string() + get_error_mark_string() + output)
            # Log output to file
            log_to_file(settings['error_log_file'],get_timestamp_string() + output + "\n\n")