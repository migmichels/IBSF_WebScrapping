from athlete import athleteResults
from webDriver import getSoup

def nationalityAthletes(browser, soup):
    athletesLinks = soup.find('table', class_='table nowrap dataTable no-footer').find_all('a')

    results = []
    
    for athleteLink in athletesLinks:
        athleteLink = 'https://www.ibsf.org' + athleteLink['href'] # O link de retorno é apenas /en/component/events/event/(ID)
        athleteSoup = getSoup(browser, athleteLink)
        athlete = athleteResults(athleteSoup) 
        results.append(athlete)

    return results