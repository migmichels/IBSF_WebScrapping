from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from results import getAllResults
from time import sleep as sl
import json

def athleteResults(url):
    options = Options()
    options.headless = True; options.add_argument("--log-level=3")

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(url)
    sl(2)
    webSite = browser.page_source

    soup = BeautifulSoup(webSite, 'html.parser')

    resultsLinks = soup.find_all('a', class_='link_results fr')

    # file = open('result.txt', 'a')
    
    for resultLink in resultsLinks:
        resultLink = resultLink['href']
        result = getAllResults('https://www.ibsf.org' + resultLink) # O link de retorno é apenas /en/component/events/event/(ID)
        resultsLinks.index(resultLink) = result
    #     file.write(json.dumps(result, indent=4))

    # file.close()

    return resultsLinks

athleteResults('https://www.ibsf.org/en/athletes/athlete/100048')