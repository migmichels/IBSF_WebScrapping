import json
import webDriver
from nationality import nationalityAthletes
from athlete import athleteResults
from results import getAllResults

browser = webDriver.startBrowser()


# soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/athletes?nationality=BRA&last_season=0&page_number=0')
# result = nationalityAthletes(browser, soup)
# print(json.dumps(result, indent= 4))

# soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/component/events/event/501462')
# result = athleteResults(browser, soup)
# print(json.dumps(result, indent= 4))

soup = webDriver.getSoup(browser, 'https://www.ibsf.org/en/component/events/event/501462')
result = getAllResults(soup)
print(json.dumps(result, indent= 4))