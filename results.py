from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep as sl
import json


def getWebSite(url):
    # Requisita o site com a URL do resultado
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(url)
    sl(2)
    webSite = browser.page_source

    return BeautifulSoup(webSite, 'html.parser')

def getRunAttributes(soup):
    # Lugar
    place = soup.find('div', class_='place').contents[0]
    # Data e Hora
    datetime = soup.find('span', class_='date')['data-datetime']
    # Categoria
    category = soup.find('div', class_='category').contents[1].contents[0]
    # Informações de cada equipe está neste tr, como nome dos atletas e país
    teams = soup.find_all('tr', class_='crew')
    # Cada corrida esta num tr de classe run, separado do tr de classe crew, ou seja, não está agrupado com o 'teams' sendo assim segue-se uma lógica diferente explicada a seguir
    runs = soup.find_all('tr', class_='run')

    return place, datetime, category, teams, runs

def getTeamAttributes(teams, runs):
    def getAthletes(team):
        # O nome de cada atleta fica dentro de um <a>
        # Este find_all() pega todos os links que existe dentro de cada 'fl athletes', e pondo cada um num array da equipe
        athletes = team.find('div', class_='fl athletes').find_all('a')

        # Para cada item de athletes, vai ser pego apenas o seu nome, e feito tratamento de texto
        for athlete in athletes:
            # O index do atleta, para alterar o valor do atleta no array "athletes"
            indexAthletes = athletes.index(athlete)

            # Tratamento de texto, pois haviam algumas quebras de linha
            # print(athlete[indexAthletes]) # Compare descomentando esse print() e o próximo
            athletes[indexAthletes] = athlete.contents[0].replace('\n', '')
            # print(athlete[indexAthletes])

        return athletes

    def getRunsTeam(indexRun, limitRun):
        def wordProcessing(run) :
            pass

        # O número de corridas por equipe é igual á quantidade de corridas, dividida pela quantidade de equipes
        limitRun += int(len(runs)/len(teams))

        # runsTeam : Array com corridas por equipe
        # Quando começar a iteração de uma nova equipe, a variável é resetada
        runsTeam = []
        
        total = 0
        # Nesse loop são pegas as informações de cada corrida, e feito o tratamento das informações
        while indexRun < limitRun : # Enquanto o index for menor que a quantidade de corrida...
            # run : array com cada tempo da corrida
            run = runs[indexRun].find_all('td')
            # O primeiro index indica o número da corrida, então é deletado. Ex: RUN 1, RUN 2 etc.
            del run[0]

            # Aqui é feito o de cada resultado da corrida
            i = 0
            while i < len(run):
                # Algumas informações vinha com tags, ou em formato de tag (<>)
                # O BeautifulSoup trata Tag como um tipo diferente de atributo
                # Outras informações vinha com mais de um conteúdo
                # Então dentro deste if, é feita a junção de todos os conteúdos em um só
                if len(run[i].contents) > 1:
                    contentIndex = 0
                    while contentIndex < len(run[i].contents):
                        run[i].contents[contentIndex] = str(run[i].contents[contentIndex])
                        contentIndex+= 1

                    run[i] = ''.join(run[i].contents)

                # Caso venha alguma informação que tenha apenas um conteúdo e que não seja do tipo string
                # É convertido então em string, para tratamento posterior
                elif type(run[i]) != str:
                    run[i] = str(run[i].contents[0])
                else: run[i] = run[i].contents[0]

                # Como há diversos padrões nos conteúdos
                # São feitas tentativas para tratamento, pois algumas podem dar erro
                try:
                    # Primeiramente é retirado os espaços do início e do final com a função strip()
                    try :
                        run[i] = run[i].strip()
    
                        # Caso houver tags (<>) em formato de strings
                        # Essa será removida
                        while '<' in run[i] :
                            tag = run[i].split('<')[1].split('>')[0]
                            run[i] = run[i].replace(tag, ''); run[i] = run[i].replace('<>', ''); run[i] = run[i].replace('  ', ' ')
                    except: pass

                    # caso ouverem números em reais sem mais nenhum conteúdo, o conteúdo é convertido em float
                    try: run[i] = float(run[i])
                    except: pass

                    # Havia alguns desses caracteres vindo junto com as informações
                    run[i] = run[i].replace('\n', '')
                    run[i] = run[i].replace('\xa0\xa0', ' ')
                    
                    # Para os campos sem informação, representado por '-', esse é convertido para None (vazio)
                    if run[i] == '-': run[i] = None; pass
                    
                except: pass

                if type(run[i]) == str:
                    if '(' in run[i] or ')' in run[i] :
                        time = run[i].split(' ')[0]

                        if ':' in time :
                            time = time.split(':')
                            minute = float(time[0])
                            second = float(time[1])
                            second = second + minute*60
                            time = second
                        time = float(time)
                        total += time
                # print((run[i]))

                i+=1

            runsTeam.append(run)
            indexRun+=1

        # print(runsTeam)

        return indexRun, limitRun, runsTeam, total
    
    
    # Cada corrida é separada em 'tr' de classe 'run' diferente
    # indexRun : index do tr de classe run, limitRun : Quantidade de corridas por equipe
    indexRun, limitRun = 0, 0

    # Para cada div da equipe (ou para cada equipe) vai ser feita uma função...
    for team in teams:
        # O nome do país está em img, no campo de descrição alt
        country = team.find('img', class_='country-flag')['alt']

        athletes = getAthletes(team)

        indexRun, limitRun, runsTeam, total = getRunsTeam(indexRun, limitRun)

        teamInfos = {
            'country' : country,
            'athletes' : athletes,
            'runs' : runsTeam,
            'total' : total
            }

        # print(teamInfos)

        index = teams.index(team)
        teams[index] = teamInfos

    return teams

def getAllResults(url): 
    soup = getWebSite(url)
    place, datetime, category, teams, runs = getRunAttributes(soup)
    
    teams = getTeamAttributes(teams, runs)

    # print(teams)
    # print(len(teams)) # Quantidade de times

    # print(place)
    # print(datetime)
    # print(category)

    return(
        {
            'place' : place,
            'datetime' : datetime,
            'category' : category,
            'teams' : teams,
        }
    )

# getAllResults('https://www.ibsf.org/en/component/events/event/500812')
# print(getAllResults('https://www.ibsf.org/en/component/events/event/500812'))

with open('result.txt', 'w') as file: file.write(json.dumps(getAllResults('https://www.ibsf.org/en/component/events/event/500352'), indent=4))
# print(json.dumps(getAllResults('https://www.ibsf.org/en/component/events/event/500812'), indent=4))