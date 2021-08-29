from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import time, sleep as sl

def startBrowser():
    options = Options()
    options.headless = True; options.add_argument("--log-level=3")
    options.page_load_strategy = 'eager'
    
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    return browser

def getSoup(browser, url):
    browser.get(url)
    print('\nCarregando a página: ' + url)
    t0 = time()
    t1 = 0
    
    while len(browser.find_elements_by_class_name("odd")) < 1 and len(browser.find_elements_by_class_name("run")) < 1 or t1-t0 >= 3:
        sl(0.5)
        t1 = time()
    
    if t1-t0 >= 3: return False

    webSite = browser.page_source

    soup = BeautifulSoup(webSite, 'html.parser')

    return soup