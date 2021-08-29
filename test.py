import webDriver, time
from pprint import pprint
from nationality import nationalityAthletes
from athlete import athleteResults
from results import getRace, getSpecificTeam


browser = webDriver.startBrowser()

t0 = time.time()


# soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/athletes?nationality=BRA&last_season=0')
# with open('result.txt', 'w') as file:
#     file.write(nationalityAthletes(browser, soup, 'https://www.ibsf.org/en/athletes?nationality=BRA&last_season=0'))

# soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/athletes/athlete/129755/Abdul%20Ghani%20Gregorio')
# result = athleteResults(browser, soup)

soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/component/events/event/500352')
# result = getRace(soup)
result = getRace(soup, '/en/athletes/athlete/100048/Bindilatti')

t1 = time.time()

pprint(result)
print('Tempo de resposta: ' + str(t1-t0) + 'segundos')