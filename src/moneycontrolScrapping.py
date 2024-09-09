from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import requests
import time

stop_thread = False
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-features=CSSStable,LoadCSSDeclarativeLinking")
options.add_experimental_option(
    "prefs", {
        "profile.managed_default_content_settings.images": 2,
    }
)
# options.add_argument("--disable-gpu")
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)


def handle_popup(driver):
    try:
        popup = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#wzrk_wrapper > div.wzrk-alert.wiz-show-animate")))
        close_button = popup.find_element(By.CSS_SELECTOR, "#wzrk-cancel")
        close_button.click()
        print("closed the popup")
        global stop_thread
        stop_thread = True
        calculate_income_and_profit(driver)
    except:
        print("no popup appeared")

def popup_handler(driver):
    global stop_thread
    while not stop_thread:
        handle_popup(driver)
        time.sleep(0.5)

def calculate_income_and_profit(driver,URL):
    wait = WebDriverWait(driver, 5)
    
    time.sleep(1)
    
    try:
        consolidated_button = driver.find_element(By.XPATH,"//a[@href='#consolidated']")
        consolidated_button.click()
    except:
        print("Already on consolidated")
        
    time.sleep(2)
    
    a_tag = driver.find_element(By.XPATH,"//a[contains(@href, '#income_statement') or contains(@href, '#stand_income_statement')]")
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
    stop_thread = False
    popup_thread = threading.Thread(target=popup_handler, args=(driver,))
    popup_thread.start()
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
    output = [stockname, currprice, l52price, h52price, ind_PE, pe, face_value, market_cap]
    URL = URL + '#financials'
    driver.get(URL)
    output = output + calculate_income_and_profit(driver,URL)
    stop_thread = True
    popup_thread.join()
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
    
    # global stop_thread
    
    count = 0
    for URL in url_list:
        output = main(URL)
        print(output)
        count = count + 1
    
    driver.quit()