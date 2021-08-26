from athlete import athleteResults
from webDriver import getSoup

def nationalityAthletes(browser, soup):
    url = soup.find('base')['href'] + '?page_number='

    results = []

    lenghtPages = len(soup.find_all('a', class_='paginate_button'))

    for indexPage in range(0, lenghtPages):
        athletesLinks = soup.find('table', class_='table nowrap dataTable no-footer').find_all('a')
        for athleteLink in athletesLinks:
            athleteLink = 'https://www.ibsf.org' + athleteLink['href'] # O link de retorno é apenas /en/component/events/event/(ID)
            athleteSoup = getSoup(browser, athleteLink)
            athlete = athleteResults(browser, athleteSoup)
            results.append(athlete)

        indexPage+=1
        if indexPage == lenghtPages+1: break
        soup = getSoup(browser, (url + str(indexPage)))

    return results