import json, webDriver, time
from nationality import nationalityAthletes
from athlete import athleteResults
from results import getRace, getSpecificTeam


browser = webDriver.startBrowser()

t0 = time.time()

url = 'https://www.ibsf.org/en/athletes?nationality=BRA&last_season=0'
soup = webDriver.getSoup(browser, url)
result = nationalityAthletes(browser, soup, url)

# soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/athletes/athlete/10474/Aranha')
# result = athleteResults(browser, soup)

# soup = webDriver.getSoup(browser, url)
# result = getRace(soup)
# result = getRace(soup, '/en/athletes/athlete/262910/Griebel')

t1 = time.time()

print(json.dumps(result, indent= 4))
print('Tempo de resposta: ' + str(t1-t0) + 'segundos')