from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import requests
import time
import os

options = webdriver.ChromeOptions()
options.add_extension(os.path.join('extensions','AdBlock.crx'))
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-features=CSSStable,LoadCSSDeclarativeLinking")
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
count = 1



######################################################

def calculate_income_and_profit(driver,URL):
    if count == 1:
        window_h = driver.window_handles[0]
        driver.switch_to.window(window_h)
        time.sleep(1)
        try:
            popup = driver.find_element(By.CSS_SELECTOR, "#wzrk_wrapper > div.wzrk-alert.wiz-show-animate")
            close_button = popup.find_element(By.CSS_SELECTOR, "#wzrk-cancel")
            close_button.click()
        except:
            time.sleep(10)
            popup = driver.find_element(By.CSS_SELECTOR, "#wzrk_wrapper > div.wzrk-alert.wiz-show-animate")
            close_button = popup.find_element(By.CSS_SELECTOR, "#wzrk-cancel")
            close_button.click()
    
    
    time.sleep(5)
    
    try:
        consolidated_button = driver.find_element(By.XPATH,"//a[contains(@href, '#consolidated')]")
        consolidated_button.click()
    except:
        print("Already on consolidated")
        
    time.sleep(2)
    
    try:
        a_tag = driver.find_element(By.XPATH,"//a[contains(@href, '#income_statement')]")
        a_tag.click()
    except:
        time.sleep(10)
        a_tag = driver.find_element(By.XPATH,"//a[contains(@href, '#income_statement')]")
        a_tag.click()
        
    time.sleep(2)
    
    try:
        table = driver.find_element(By.CSS_SELECTOR,'#C-income_statement-3 > table:nth-child(1)').get_attribute('outerHTML')
        soup = BeautifulSoup(table, 'html.parser')
        tr_elements = soup.find_all('tr')
        tr = []
        for td in tr_elements:
            tr_single = td.find_all('td')[:-1]
            td_single = []
            for td in tr_single:
                td_single.append(td.text)
            tr.append(td_single)
            td_single = []

        q_income = tr[1][1]
        q_profit = tr[-1][1]
    except:
        q_income = "--"
        q_profit = "--"
    
    time.sleep(1)
    
    try:
        a_tag = driver.find_element(By.XPATH, "//a[contains(@href, '#C-income-12')]")
        a_tag.click()
    except:
        time.sleep(10)
        a_tag = driver.find_element(By.XPATH, "//a[contains(@href, '#C-income-12')]")
        a_tag.click()
    
    time.sleep(2)
    
    try:
        table = driver.find_element(By.CSS_SELECTOR,'#C-income_statement-12 > table:nth-child(1)').get_attribute('outerHTML')
        soup = BeautifulSoup(table, 'html.parser')
        
        tr_elements = soup.find_all('tr')
        tr = []
        for td in tr_elements:
            tr_single = td.find_all('td')[:-1]
            td_single = []
            for td in tr_single:
                td_single.append(td.text)
            tr.append(td_single)
            td_single = []

        y_income = tr[1][1]
        y_profit = tr[-1][1]
    except:
        y_income = "--"
        y_profit = "--"

    return [q_profit, q_income, y_profit, y_income]

def main(URL):
    global count
    url = requests.get(URL)
    soup = BeautifulSoup(url.text,"html.parser")
    stockname = soup.find('div',id="stockName").find('h1').text
    currprice = soup.find('div',class_= "inprice1 nsecp").get('rel')
    h52price = soup.find('td',class_="nseH52 bseH52").text
    l52price = soup.find('td',class_="nseL52 bseL52").text
    ind_PE = soup.find('td',class_="nsesc_ttm bsesc_ttm").text
    pe = soup.find('span',class_="nsepe bsepe").text
    face_value = soup.find('td',class_="nsefv bsefv").text
    market_cap = soup.find('td',class_="nsemktcap bsemktcap").text
    output = [count,stockname, currprice, l52price, h52price, ind_PE, pe, face_value, market_cap]
    URL = URL + '#financials'
    
    driver.get(URL)
    
    
    output = output + calculate_income_and_profit(driver,URL)
    count = count + 1
    return output

if __name__ == "__main__":
    
    url_list = [
        "https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/thetatapowercompany/TPC",
        "https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/adanipower/AP11",
        "https://www.moneycontrol.com/india/stockpricequote/infrastructure-general/adaniportsspecialeconomiczone/MPS",
        "https://www.moneycontrol.com/india/stockpricequote/metals-non-ferrous/hindustancopper/HC07",
        "https://www.moneycontrol.com/india/stockpricequote/constructioncontracting-civil/ncc/NCC01",
        "https://www.moneycontrol.com/india/stockpricequote/online-services/zomato/Z",
        "https://www.moneycontrol.com/india/stockpricequote/consumer-food/devyaniinternational/DI06",
        "https://www.moneycontrol.com/india/stockpricequote/engineering/engineersindia/EI14",
        "https://www.moneycontrol.com/india/stockpricequote/cement-mini/nclindustries/NCL",
        "https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/nhpc/N07",
        "https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/sjvn/S11",
        "https://www.moneycontrol.com/india/stockpricequote/diversified/tatatechnologies/TTL01",
        "https://www.moneycontrol.com/india/stockpricequote/engineering-industrial-equipments/ideaforgetechnology/IT07",
        "https://www.moneycontrol.com/india/stockpricequote/engineering-construction/bajelprojects/BP06",
        "https://www.moneycontrol.com/india/stockpricequote/vanaspatioils/bclindustries/BC06",
        "https://www.moneycontrol.com/india/stockpricequote/aerospacedefence/bharatelectronics/BE03",
        "https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/indianrenewableenergydevelopmentagency/IREDAL",
        "https://www.moneycontrol.com/india/stockpricequote/engineering-heavy/irconinternational/II07",
        "https://www.moneycontrol.com/india/stockpricequote/finance-others/jiofinancialservices/JFS",
        "https://www.moneycontrol.com/india/stockpricequote/hospitalhealthcare-services/mediassisthealthcareservices/MAH01",
        "https://www.moneycontrol.com/india/stockpricequote/finance-term-lending-institutions/rec/REC02",
        "https://www.moneycontrol.com/india/stockpricequote/food-processing/sarveshwarfoods/SF29",
        "https://www.moneycontrol.com/india/stockpricequote/banks-private-sector/yesbank/YB",
        "https://www.moneycontrol.com/india/stockpricequote/finance-investments/blb/BLB",
    ]
    
    for URL in url_list:
        output = main(URL)
        print(output)
        
    driver.quit()