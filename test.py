import webDriver, time, json
from pprint import pprint
from nationality import nationalityAthletes
from athlete import athleteResults
from results import getRace, getSpecificTeam


browser = webDriver.startBrowser()

t0 = time.time()


soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/athletes?nationality=BRA&last_season=0')
with open('result.json', 'w') as file:
    file.write(json.dumps(nationalityAthletes(browser, soup, 'https://www.ibsf.org/en/athletes?nationality=BRA&last_season=0'), indent=4))

# soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/athletes/athlete/263511/Barbosa%20Neves')
# result = athleteResults(browser, soup)

# soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/component/events/event/166010')
# result = getRace(soup)
# result = getRace(soup, '/en/athletes/athlete/100048/Bindilatti')

t1 = time.time()

# pprint(result)
print('Tempo de resposta: ' + str(t1-t0) + 'segundos')