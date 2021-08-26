from results import getRace
from webDriver import getSoup

def athleteResults(browser, soup):
    url = soup.find('base')['href'] + '?page_number='

    results = []

    lenghtPages = len(soup.find_all('a', class_='paginate_button'))
    
    for indexPage in range(0, lenghtPages):
        resultsLinks = soup.find('table', id='results_table').find_all('a', class_='link_results fr')
        for resultLink in resultsLinks:
            resultLink = 'https://www.ibsf.org' + resultLink['href'] # O link de retorno é apenas /en/component/events/event/(ID)
            resultSoup = getSoup(browser, resultLink)
            result = getRace(resultSoup)
            results.append(result)
        
        indexPage+=1
        if indexPage == lenghtPages+1: continue
        soup = getSoup(browser, (url + str(indexPage)))

    return results