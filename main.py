from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from prettytable import PrettyTable
from datetime import date
import time

SCROLL_PAUSE_TIME = 1


# load chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://coinmarketcap.com/")


# prepare pretty table
table = PrettyTable()
table.field_names = ['Position', 'Name', 'Price', '24h price change', '7d price change', 'Market cap', 'Volume 24h', 'Circulating suply', 'Logo', '7d price graph']



# get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")


# get monitor height
monitor_height_const = int(driver.get_window_size()["height"])
monitor_height_curr = 0


# load complette page
while True:
    # wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # scroll down for one monitor height
    monitor_height_curr += monitor_height_const
    driver.execute_script(f"window.scrollTo(0, {monitor_height_curr});")

    # calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height < monitor_height_curr:
        break
    last_height = new_height

# make BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
table_body = soup.find('tbody')
rows = table_body.find_all('tr')

# chceck if span class is positive or negative for percentual changes
def is_positive_number(object):
    if object.attrs['class'] == ['sc-15yy2pl-0', 'hzgCfk']:
        return("-" + object.text)
    else:
        return("+" + object.text)

# fill table with data
position=0
for row in rows:
    position+=1
    name_soup = (row.find('div', attrs={"class" : lambda L: L and L.startswith('sc-16r8icm-0')}))
    name = name_soup.p.text
    price_soup = (row.find('div', attrs={"class" : lambda L: L and L.startswith('sc-131di3y-0 cLgOOr')}))
    price = price_soup.span.text
    percentual = (row.findAll('span', attrs={'class' : 'sc-15yy2pl-0'}))
    percentual_24h = is_positive_number(percentual[0])
    percentual_7d = is_positive_number(percentual[1])
    market_cap = (row.find('span', attrs={'class' : 'sc-1ow4cwt-1 ieFnWP'})).text
    volume24h = (row.find('p', attrs={'class' : 'sc-1eb5slv-0 hykWbK font_weight_500'})).text
    circulating_suply = (row.find('p', attrs={'class' : 'sc-1eb5slv-0 kZlTnE'})).text
    images = (row.findAll('img'))
    logo = images[0]['src']
    price_graph = images[1]['src']
    table.add_row([position, name, price, percentual_24h, percentual_7d, market_cap, volume24h, circulating_suply, logo, price_graph])

print(table)

# save csv file
with open(f'first_100_crypto_{date.today()}.txt', 'w') as w:
    w.write(str(table))