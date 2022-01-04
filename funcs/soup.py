import requests
from bs4 import BeautifulSoup
import time

def getStockPrice(stocks, stocksPrice, running):
    base_url = 'https://www.marketwatch.com/investing/stock/'
    while True:
        try:
            if not running():
                break
            for i,stock in enumerate(stocks):
                if not running():
                    break
                url = base_url + stock
                html = requests.get(url)
                soup = BeautifulSoup(html.content, "html.parser")
                main_div = soup.find('bg-quote', attrs = {'class':'value'})
                sign = soup.find('sup', attrs = {'class':'character'}).text
                try:
                    stocksPrice[i] = (sign if sign else '') + main_div.text
                except:
                    stocksPrice[i] = "Error"
                #welp, this is the fast version, so whatever
        except IndexError:
            pass
        except:
            break

#--------------------------------------------Discontinued--------------------------------------------#

def getStockPriceLegacy(stocks, stocksPrice):
    while True:
        base_url = 'https://finance.yahoo.com/quote/'
        for i,stock in enumerate(stocks):
            url = base_url + stock
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")
            main_div = soup.find('fin-streamer', attrs = {'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'})
            try:
                stocksPrice[i] = main_div.text
            except:
                stocksPrice[i] = "Error in getting stock price"
            print(stocksPrice)
            time.sleep(1)
        time.sleep(2)

def getStockPriceIndividual(stock):
    base_url = 'https://finance.yahoo.com/quote/'
    url = base_url + stock
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    main_div = soup.find('fin-streamer', attrs = {'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'})
    try:
        return main_div.text
    except:
        return "Error in getting stock price"