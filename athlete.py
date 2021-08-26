from results import getRace
from webDriver import getSoup

def athleteResults(browser, soup):
    if not(soup) : return None
    url = soup.find('base')['href'] + '?page_number='

    results = []

    lenghtPages = len(soup.select('span a.paginate_button'))
    
    for indexPage in range(0, lenghtPages):
        resultsLinks = soup.find('table', id='results_table').find_all('a')
        for resultLink in resultsLinks:
            resultLink = 'https://www.ibsf.org' + resultLink['href'] # O link de retorno é apenas /en/component/events/event/(ID)
            resultSoup = getSoup(browser, resultLink)
            result = getRace(resultSoup)
            results.append(result)
        
        indexPage+=1
        if indexPage == lenghtPages+1: break
        soup = getSoup(browser, (url + str(indexPage)))

    return results