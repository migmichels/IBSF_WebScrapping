from results import getRace
from webDriver import getSoup

def athleteResults(browser, soup):
    if not(soup) : return None
    url = soup.find('base')['href'] + '?page_number='

    results = []

    paginate_buttonsTag = soup.select('span a.paginate_button')
    lenghtPages = int(paginate_buttonsTag[len(paginate_buttonsTag)-1].contents[0])
    
    for indexPage in range(0, lenghtPages):
        print('Atleta: página ' + str(indexPage))
        resultsLinks = soup.find('table', id='results_table').find_all('a')
        for resultLink in resultsLinks:
            resultLink = 'https://www.ibsf.org' + resultLink['href'] # O link de retorno é apenas /en/component/events/event/(ID)
            resultSoup = getSoup(browser, resultLink)
            result = getRace(resultSoup)
            results.append(result)
        
        indexPage+=1
        if indexPage == lenghtPages: break
        soup = getSoup(browser, (url + str(indexPage)))

    return results