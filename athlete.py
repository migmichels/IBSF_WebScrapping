from results import getRace
from webDriver import getSoup

def athleteResults(browser, soup):
    resultsLinks = soup.find_all('a', class_='link_results fr')

    results = []
    
    for resultLink in resultsLinks:
        resultLink = 'https://www.ibsf.org' + resultLink['href'] # O link de retorno é apenas /en/component/events/event/(ID)
        resultSoup = getSoup(browser, resultLink)
        result = getRace(resultSoup)
        results.append(result)

    return results