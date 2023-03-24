# Binance Trader Bot

**Trade crypto like pro 24/7 whether you're working, resting or playing.**

<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/BTB_Screen_Shot_01.png?raw=true">

### Introduction
 This project came about as I wanted my crypto holdings to work harder for me than simply staking it. I looked around a little (not very much at all, if I'm honest) and couldn't really find one that I liked. I really didn't like the way I'd have to set and watch prices for trading pairs or the way others only did one trading pair at a time, monthly subscriptions, etc, etc. I just wanted a bot that was simple to use and capable of multiple trading pairs.

 As stated I wanted something that was simple and easy to use. With that in mind I went into developing this bot with two old sayings in mind, the first one being *'keep it simple, stupid'*, as I'm definitely no crypto trading god. The second being about making money *'buy low, Sell high'* and that's exactly how this thing works. The bot follows three SMA (Simple Moving Averages) points as well as the current price, to determine which way the market is moving, to figure out if it's a good time to buy or sell. Simply put it *'buys in the dips and sells at the tips'*.

### Trading Strategy
The trading strategy is very simple; buy low, sell high. This is achieved by calculating three different moving averages over three different time periods, just like in any trading graph you've ever seen. To determine which way the market is moving, either up or down. So if the medium average price is greater than the long average price and the short average price is greater than the medium average price and the current price is greater than the short average price, the bot will sell. The same is true for buying just replace the 'greater then' with 'less than' and the bot will buy.

**WARNING:** If any of these conditions are met the bot will trade regardless of the current price being the lowest or highest price possible. It simply makes the buy or sell choice based on trends in the market at that time.

### Prerequisites
1. Hardware, some kind of computer to run the python script. It definitely doesn't have to be a high end machine, in fact something like a Raspberry Pi is perfect for this, due to its low power consumption and physical size. It's also what was used during the testing of the bot.
2. An installation of Linux (or possibly Mac OS, not tested as yet), something Debian based, like Ubuntu or Raspberry Pi OS. It's possible the bot may work with other versions of Linux, but it hasn't been tested at the time of writing this. Sorry to Windows users as there seems to be a bug in the python-binance library used in the bot that causes errors.
3. An internet connection, obviously as there is no way to communicate with the Binance exchange without it
4. An account with the [Binance](https://www.binance.com/) exchange, with some funds available. Your account will also provide the necessary API keys to get the bot working with your account on the exchange. 

### Installation
After you have your chosen system up and running, you can run the following commands to install the bot.

1. Update System

 ```BASH
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y
```
2. Install Dependencies

```BASH
sudo apt install python3 python3-pip git screen -y
```
3. Clone Repository

```BASH
git clone https://github.com/idiydownunder/binance-trader-bot.git
```

4. Change Directory

```BASH
cd binance-trader-bot
```
5. Install pip Dependencies

```BASH
python3 -m pip install -r requirements.txt
```

6. After you have run the above commands you should be all set to run the bot, just remember you will need to edit the config.json file with the trading pairs you wish to use first. See configuration section below.

7. Run The Bot

```BASH
python3 traderbot.py
```
8. The first time you run the bot you will be asked for your API key and secret key, See Getting API Keys section below.

### Configuration (config.json)
The config.json is where you will need to add your data relating to which markets you wish to trade on, as well as defining certain things about the trading behavior on those markets. The bot will also monitor this file for changes and will apply the changes dynamically at run time, so you don't need to close and restart the bot for setting changes to take place.

To get started you will need to load the config.json file into your favorite text editor, nano, vi, whatever you like.

```BASH
nano config.json
``` 

**NOTE:** After editing config.json it needs to be a valid JSON file, If you are unfamiliar with editing JSON files I would highly recommend using an online JSON validation tool like [JSON Lint](https://jsonlint.com/) to check your changes are valid.

This is what a basic default config.json file looks like;
```JSON
{
    "tld":"com",
    "sma_short_period":7,
    "sma_medium_period":25,
    "sma_long_period":99,
    "trade_timer_minutes":60,
    "show_balances":false,
    "show_markets":false,
    "show_trades":true,
    "sales_log_file":"SalesLog.txt",
    "error_log_file":"ErrLog.txt",
    "trading_pairs":[
        {
            "coin":"BTC",
            "fiat":"USDT",
            "coin_hold_amount":0,
            "fiat_hold_amount":0,
            "trade_enable":true,
            "trade_price_guard":false,
            "trade_buy_enable":true,
            "trade_sell_enable":true,
            "trade_buy_adjustment":0,
            "trade_sell_adjustment":0,
            "trade_buy_price_adjustment":0,
            "trade_sell_price_adjustment":0
        },
        {
            "coin":"ETH",
            "fiat":"USDT",
            "coin_hold_amount":0,
            "fiat_hold_amount":0,
            "trade_enable":true,
            "trade_price_guard":false,
            "trade_buy_enable":true,
            "trade_sell_enable":true,
            "trade_buy_adjustment":0,
            "trade_sell_adjustment":0,
            "trade_buy_price_adjustment":0,
            "trade_sell_price_adjustment":0
        },
        {
            "coin":"BNB",
            "fiat":"USDT",
            "coin_hold_amount":0,
            "fiat_hold_amount":0,
            "trade_enable":true,
            "trade_price_guard":false,
            "trade_buy_enable":true,
            "trade_sell_enable":true,
            "trade_buy_adjustment":0,
            "trade_sell_adjustment":0,
            "trade_buy_price_adjustment":0,
            "trade_sell_price_adjustment":0
        }
    ]
}
```

**tld** If you are interacting with a regional version of Binance which has a different Top Level Domain then you will need to pass this when using the bot for it to work properly, for example if the website you login to is 'binance.com' you would set this to 'com' or if you use 'binance.us' you would set this to 'us'.

**sma_short_period, sma_medium_period & sma_long_period** These values represent the number of days used when calculating the moving average price's. I do not recommend changing these values unless you are a more advanced trader looking to adjust the trading strategy to better suit your trading strategy.

**trade_timer_minutes** This value sets, in minutes, how often the bot will check the markets looking for trades. Remember to be conservative when setting this value, for example if you set it to 1 minute the bot will attempt to make buy or sell trades every minute if the market conditions are right resulting in holdings being rapidly drained one way or the other. The other consideration when setting this value is the time period used in the timeframe variable within the bot python script, see Configuration (traderbot.py) for more information

**show_balances, show_markets & show_trades** These are boolean flags set to either true or false depending on if you want the data displayed in the terminal at run time.<br>"show_balances":true = Will display the 'free' (not locked) amount of holdings in that wallet, zero balances are not shown.<br>"show_markets":true = Will display the current market price as well as your trading status for that market.<br>"show_trades":true = Will display a buy, sell or miss message about an order. All successful buy and sell orders are logged to a file regardless if this value is true or false. 

**sales_log_file & error_log_file** These values are used to set the log file names and or paths the bot uses for reporting.

**trading_pairs** This is where we set up which trading pairs or markets we want the bot to trade on. E.g BTC/USDT or ETH/USDT. You can add as many as you want to trade on, but you will need at least one! Add or remove trading pairs in blocks like this;
```JSON
{
    "coin":"BTC",
    "fiat":"USDT",
    "coin_hold_amount":0,
    "fiat_hold_amount":0,
    "trade_enable":true,
    "trade_price_guard":false,
    "trade_buy_enable":true,
    "trade_sell_enable":true,
    "trade_buy_adjustment":0,
    "trade_sell_adjustment":0,
    "trade_buy_price_adjustment":0,
    "trade_sell_price_adjustment":0
}
```
**coin** Sets which cyrpto currency we wish to buy and sell.

**fiat** Sets what currency we are using to buy and sell the cyrpto currency with. This could also be another cyrpto currency.

**coin_hold_amount & fiat_hold_amount** Sets how much of a currency you wish to hold. These values are subtracted from your wallets free holding balance before determining if a buy or sell action is possible. Note if set to 0 the bot will use all available assets when making trades. Also note that this hold amount is only for this trading pair and not other Trading pairs.

**trade_enable** This value will enable or disable all trading in this market. It acts like a master switch and will override trade_buy_enable and trade_sell_enable without changing their values.

**trade_price_guard** By having this value set to true, the bot will monitor the buy pricing to find the highest buy price. Then when it comes time to sell again, the highest buy price will be added to the trade_sell_price_adjustment value, then if the current price is equal to or greater than this calculated value, the sale is made. Note this is a one time deal and after a successful sale the highest buy price is reset ready for the next buy period. Also use this with some caution as if a market continues to dip it may be a long time before the price goes high enough to trigger another sale. 

**trade_buy_enable & trade_sell_enable** Setting these will either enable or disable buying or selling. As long as "trade_enable": true these settings are in effect. Useful if you wish to liquidate or accrue certain currencies.

**trade_buy_adjustment & trade_sell_adjustment** Setting these values will determine the amount at which you buy and sell at. These work like a multiplier as Binance has a minimum trade amount. Because they work like a multiplier two numbers are reserved as they would mess with the calculations.<br>0 = Minimum Buy/Sell Amount<br>1 = All Available Balance<br>values > 1 = Minimum Buy/Sell Amount X Adjustment Value<br>values < 1 & values > 0 = All Available Balance X Adjustment Value (works like a percent of)<br>If the calculated adjusted value can not be used the minimum amount will be used instead.

**trade_buy_price_adjustment & trade_sell_price_adjustment** These values get +/- to the Long Moving Average to help reduce noise and small gains. For example if the MA was .5430 and the Current Price is .5432 it would not be a very profitable trade. By adding a small adjustment we can better see how far away the current price is from the moving average. The trick here is to have it set high enough to reduce noise when the price is close to the average as well as making good gains, but not so high that we never make any trades. If set to 0 the price will only need to be higher than the Short Moving Average to trigger a trade.

### Configuration (traderbot.py)
While configuring the traderbot.py is not mandatory and there is only one option, I would only recommend this for advanced traders, but I'll cover it here anyway.

Open the traderbot.py file in your favorite text editor.

```BASH
nano traderbot.py
``` 

Then scroll down until you find the section that looks like this;

```PYTHON
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
```

This section sets the KLINE Time Frame, to change this simply comment out the line *timeframe = Client.KLINE_INTERVAL_4HOUR* with a *#* at the start of the line and delete the *#* mark from the line for the Time Frame you wish to use.

**WARNING:** This option will have the biggest impact on the bots behavior. If you wish to change this option I highly recommend you do so before running the bot for the first time. Changing after trading for a while could very well see go from buying phase to a selling phase, just by changing this one option. I can not recommend strongly enough that if you do wish to change this option, to make that decision before trading with the bot and once set, forget about it, seriously.

 **IMPORTANT INFORMATION** This option defines the 'candle' time period that you would see on a trading chart. As a result this will have a major impact on calculating the moving average prices, ultimately affecting the bots decision making process.<br>As a general rule setting this option to lower values like 15min or 30min would result in more trades being made with only small gains being made. Alternatively setting it higher values like 1day or 3day would result in less trades being made, but with bigger gains.<br>Other things to consider; more trades for smaller gains would incur more transaction fees. The trade_timer_minutes value in the config.json file as there would be no need to try and make trades every minute if your KLINE was set to 3days, generally you would only need to check once per KLINE period, to maybe 2 or 3 times per KLINE period depend on your capital and risk levels.

### Getting API Keys

1. Head over to [Binance](https://www.binance.com/) and login or sign up.

2. Click on the profile icon.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_01.png?raw=true" width="600">

3. Select 'API Management' from the drop down menu.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_02.png?raw=true" width="600">

4. Select 'Create API'.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_03.png?raw=true" width="600">

5. Ensure 'System generated' is selected and click 'Next'.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_04.png?raw=true" width="600">

6. Enter a label (name) for the API Key, this can be anything.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_05.png?raw=true" width="600">

7. You should now be faced with an anti robot verification check, complete that and move on.<br>

8. You will need to complete a 'Security verification', Click both 'Get Code' buttons, enter them in the appropriate spaces and click 'Submit'.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_06.png?raw=true" width="600">

9. We now need to edit the API Key to enable it to be able to trade, click 'Edit restrictions'.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_07.png?raw=true" width="600">

10. Select 'Restrict access to trusted IP's only'.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_08.png?raw=true" width="600">

11. Enter your IP address and click 'Confirm'. If you don't know your IP address simply ask [Google](https://www.google.com.au/search?q=whats+my+ip) or use a service like [WhatIsMyIP](https://www.whatismyip.com/) to find it.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_09.png?raw=true" width="600">

12. Now you can select 'Enable Spot & Margin Trading', then click 'Save'.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_10.png?raw=true" width="600">

13. You will need to complete another 'Security verification', Click 'Get Code' buttons, enter it in spaces and click 'Submit'.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_11.png?raw=true" width="600">

14. Now you can copy and paste your API Key and Secret Key into the config.json file.<br>
<img src="https://github.com/idiydownunder/binance-trader-bot/blob/main/Resources/Get_API_Step_12.png?raw=true" width="600">

**NOTE:** You must get the Secret Key at this point as it WILL NOT be shown again. If you fail to get it now you will need to delete the API Key and start over.

*Before You Bother: The API Key shown here was deleted after compiling this section, it will not work!. The IP address shown here is not mine! I made it up for demo purposes!*

### Persistence (Terminal)

This is great and all, but the bot stops as soon as I close my terminal and I don't want to have it open 24/7, I hear you say. Relax, if you have been following along we actually installed a program called screen during the Installation section. Just in case you didn't you can install it now with the following command.

```BASH
sudo apt install screen -y
```
The screen program creates terminal instances we can attach and detach to while keeping whatever program that's running in it active. To start a new terminal instance with screen we use the following command syntax;<br>*screen -S &#60;instance name&#62;*<br>we can use the following command syntax to reconnect to an instance with;<br>*screen -r &#60;instance name&#62;*<br>And we can see a list of running instances with the syntax;<br>*screen -ls*<br>when we are connected to a running instance we can detach from it by pressing *ctrl* + *a* then press *ctrl* + *d*

Let's start a screen instance for our bot with the following command;

```BASH
screen -S binance-trader
```

Now navigate to the bot directory and run the bot just like before;

```BASH
python3 traderbot.py
```

Let's detach by pressing *ctrl* + *a* then pressing *ctrl* + *d*

Now check to see that we did detach properly;

```BASH
screen -ls
```
Let's check on our bot by reconnecting;

```BASH
screen -r binance-trader
```

### Persistence (System Startup)

To have this bot run every time the system is started or rebooted, I recommend making a cron job. To do this simply enter the following command in your terminal;

```BASH
crontab -e
```

If this is your first time creating a cron job you will be asked to select a text editor, pick whichever you feel comfortable with. If you're new just go with nano as directions from here will be with nano. Once the crontab opens in the chosen editor simply copy the following code and paste it in as the last line;

```BASH
@reboot screen -dmS binance-trader python3 /home/pi/binance-trader-bot/traderbot.py
```
Just remember to change the */home/pi/binance-trader-bot/traderbot.py* to the location of the bot on your system. Now press *ctrl* + *x* to exit, confirm the changes by pressing *y* and write the output by pressing *'Enter'*. Now the bot should start automatically every time the computer is restarted.

### Donate

While developing things like this are a passion and hobby for me. I ask that if you have found this educational, helpful, insiteful or maybe you've even made a few dollars out of this bot, maybe you could consider making a donation to the project. To help fund future development costs, mainly my time and coffee.

Cash donations can be made through my [PayPal.Me](https://www.paypal.com/paypalme/carmichaeljuian) link.

Crypto donations can be made to the following wallets;<br>
Bitcoin (BTC): 1Kt78m7LPZkkfxyMx8rVcdJxBftZw937Sc<br>
Monero (XMR): 4BAco3fES2cXfymfx7NVd62Z6EfgXNvaZg3tba8jWjvHR52cHDbmkiT5iEm3Kxq4XhbCeFEacCJzkBYtHpXwwGbJ2d7FWwr<br>

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.