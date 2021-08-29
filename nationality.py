from athlete import athleteResults
from webDriver import getSoup

def nationalityAthletes(browser, soup, url):
    if len(url.split('&page_number=')) == 1 or len(url.split('?page_number=')) == 1: url = url + '&page_number='
    else : url = url.replace('page_number=' + url.split('page_number=')[1], 'page_number=')

    athletes = []

    paginate_buttonsTag = soup.select('span a.paginate_button')
    lenghtPages = int(paginate_buttonsTag[len(paginate_buttonsTag)-1].contents[0])

    for indexPage in range(0, lenghtPages):
        print('Nacionalidade: página ' + str(indexPage))
        athletesLinks = soup.find('table', id='results_table').find_all('a')
        for athleteLink in athletesLinks:
            athleteLink = 'https://www.ibsf.org' + athleteLink['href'] # O link de retorno é apenas /en/component/events/event/(ID)
            athleteSoup = getSoup(browser, athleteLink)
            if not(athleteSoup) :
                continue
            athlete = athleteResults(browser, athleteSoup)
            athletes.append(athlete)

        indexPage+=1
        if indexPage == lenghtPages+1: break
        soup = getSoup(browser, (url + str(indexPage)))

    return athletes