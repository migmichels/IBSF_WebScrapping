import json
import webDriver
from nationality import nationalityAthletes
from athlete import athleteResults
from results import getRace, getSpecificTeam

browser = webDriver.startBrowser()


# soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/athletes?nationality=BRA&last_season=0&page_number=0')
# result = nationalityAthletes(browser, soup)

# soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/athletes/athlete/264264/Silveira')
# result = athleteResults(browser, soup)

soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/component/events/event/501462')
# result = getRace(soup)
result = getRace(soup, '/en/athletes/athlete/262910/Griebel')


print(json.dumps(result, indent= 4))