from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep as sl

def startBrowser():
    options = Options()
    options.headless = True; options.add_argument("--log-level=3")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    return browser

def getSoup(browser, url):
    browser.get(url)
    print('Carregando a página: ' + url)
    while len(browser.find_elements_by_class_name("odd")) < 1 and len(browser.find_elements_by_class_name("run")) < 1 :
        sl(0.3)
        pass
    
    webSite = browser.page_source

    soup = BeautifulSoup(webSite, 'html.parser')

    return soup