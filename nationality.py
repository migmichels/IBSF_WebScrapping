from athlete import athleteResults
from webDriver import getSoup

def nationalityAthletes(browser, soup, url):
    if len(url.split('&number_page=')) == 1 or len(url.split('?number_page=')) == 1: url = url + '&number_page='
    else : url = url.replace('number_page=' + url.split('number_page=')[1], 'number_page=')

    athletes = []

    lenghtPages = len(soup.select('span a.paginate_button'))
    
    for indexPage in range(0, lenghtPages):
        athletesLinks = soup.find('table', id='results_table').find_all('a')
        for athleteLink in athletesLinks:
            athleteLink = 'https://www.ibsf.org' + athleteLink['href'] # O link de retorno é apenas /en/component/events/event/(ID)
            athleteSoup = getSoup(browser, athleteLink)
            athlete = athleteResults(browser, athleteSoup)
            athletes.append(athlete)

        indexPage+=1
        if indexPage == lenghtPages+1: break
        soup = getSoup(browser, (url + str(indexPage)))

    return len(athletes)