def getRaceAttributes():
    global place, datetime, category, teams, runs, quantityRunsPerTeam, limitRun, tbody

    # Lugar
    place = soup.find('div', class_='place').contents[0]
    # Data e Hora
    datetime = soup.find('span', class_='date')['data-datetime']
    # Categoria
    category = soup.find('div', class_='category').contents[1].contents[0]
    # Informações de cada equipe está neste tr, como nome dos atletas e país
    teams = soup.select('.visible-xs .fl.athletes')
    # Cada corrida esta num tr de classe run, separado do tr de classe crew, ou seja, não está agrupado com o 'teams' sendo assim segue-se uma lógica diferente explicada a seguir
    runs = soup.find_all('tr', class_='run')

    tbody = soup.find('tbody').contents

    limitRun = 0

def getSpecificTeam(athleteURL):
    global teams,limitRun

    team = soup.find_all('a', href=athleteURL)[1].parent

    limitRun = runs.index(team.findNext('tr', class_='run'))
    
    teams = processTeamAttributes(team)

    # runsTeam, total = getRuns(limitRun)

def getAthletes(team):
    # O nome de cada atleta fica dentro de um <a>
    # Este find_all() pega todos os links que existe dentro de cada 'fl athletes', e pondo cada um num array da equipe
    athletes = team.find_all('a')

    # Para cada item de athletes, vai ser pego apenas o seu nome, e feito tratamento de texto
    for athlete in athletes:
        # O index do atleta, para alterar o valor do atleta no array "athletes"
        indexAthletes = athletes.index(athlete)

        # Tratamento de texto, pois haviam algumas quebras de linha
        # print(athlete[indexAthletes]) # Compare descomentando esse print() e o próximo
        if athlete.contents[0] == '\n' :
            athleteContent = athlete.contents[2]
        else:
            athleteContent = athlete.contents[0]

        athletes[indexAthletes] = athleteContent.replace('\n', '').strip()
        # print(athlete[indexAthletes])

    return athletes

def getRuns():
    global limitRun

    firstRun = limitRun

    try: indexTbody = tbody.index(runs[limitRun])
    except: return None, None

    i = 0

    while True:
        i+=1
        if limitRun + i == len(runs) or str(tbody[indexTbody+i].findNext('tr').get('class')[0]) != 'run' : break

    limitRun+=i

    # runsTeam : Array com corridas por equipe
    # Quando começar a iteração de uma nova equipe, a variável é resetada
    runsTeam = []

    total = 0
    # Nesse loop são pegas as informações de cada corrida, e feito o tratamento das informações
    for indexRun in range(firstRun, limitRun) : # Enquanto o index for menor que a quantidade de corrida...
        # run : array com cada tempo da corrida
        run = runs[indexRun].find_all('td')
        # O primeiro index indica o número da corrida, então é deletado. Ex: RUN 1, RUN 2 etc.
        del run[0]

        for runValue in run:
            indexValue = run.index(runValue)
            # Algumas informações vinha com tags, ou em formato de tag (<>)
            # O BeautifulSoup trata Tag como um tipo diferente de atributo
            # Outras informações vinha com mais de um conteúdo
            # Então dentro deste if, é feita a junção de todos os conteúdos em um só

            if len(runValue.contents) > 1:
                contentIndex = 0
                while contentIndex < len(runValue.contents):
                    runValue.contents[contentIndex] = str(runValue.contents[contentIndex])
                    contentIndex+= 1

                runValue = ''.join(runValue.contents)

            # Caso venha alguma informação que tenha apenas um conteúdo e que não seja do tipo string
            # É convertido então em string, para tratamento posterior
            elif type(runValue) != str:
                runValue = str(runValue.contents[0])
            else: runValue = runValue.contents[0]

            # Como há diversos padrões nos conteúdos
            # São feitas tentativas para tratamento, pois algumas podem dar erro
            try:
                # Primeiramente é retirado os espaços do início e do final com a função strip()
                try :
                    runValue = runValue.strip()

                    # Caso houver tags (<>) em formato de strings
                    # Essa será removida
                    while '<' in runValue :
                        tag = runValue.split('<')[1].split('>')[0]
                        runValue = runValue.replace(tag, ''); runValue = runValue.replace('<>', ''); runValue = runValue.replace('  ', ' ')
                except: pass

                # caso ouverem números em reais sem mais nenhum conteúdo, o conteúdo é convertido em float
                try: runValue = float(runValue)
                except: pass

                # Havia alguns desses caracteres vindo junto com as informações
                runValue = runValue.replace('\n', '')
                runValue = runValue.replace('\xa0\xa0', ' ')
                
                # Para os campos sem informação, representado por '-', esse é convertido para None (vazio)
                if runValue == '-': runValue = None; pass

            except: pass

            if type(runValue) == str:
                if '(' in runValue or ')' in runValue :
                    time = runValue.split(' ')[0] # O tempo é separado dos parênteses por um espaço. assim o primeiro conteúdo é o tempo

                    if ':' in time : # Caso o número seja maior que 1 min, o valor é quebrado pra mn:sc:ms
                        time = time.split(':')
                        minute = float(time[0])
                        second = float(time[1])
                        second = second + minute*60
                        time = second
                    time = float(time)
                    total += time

            run[indexValue] = runValue

        runsTeam.append(run)

    # print(runsTeam)

    return runsTeam, total

def processTeamAttributes(team):
    # O nome do país está em img, no campo de descrição alt
    country = team.find('img', class_='country-flag')['alt']

    athletes = getAthletes(team)

    # O número de corridas por equipe é igual á quantidade de corridas, dividida pela quantidade de equipes
    runsTeam, total = getRuns()

    return {
        'country' : country,
        'athletes' : athletes,
        'runs' : runsTeam,
        'total' : total
        }

def getTeamsAttributes(teams):
    global quantityRunsPerTeam
    # Cada corrida é separada em 'tr' de classe 'run' diferente
    # indexRun : index do tr de classe run, limitRun : Quantidade de corridas por equipe

    # Para cada div da equipe (ou para cada equipe) vai ser feita uma função...
    for team in teams:
        teamInfos = processTeamAttributes(team)

        index = teams.index(team)
        teams[index] = teamInfos

    return teams

def getRace(soupParameter, athleteUrl = False):
    if not(soupParameter) :
        return None

    global soup
    soup = soupParameter

    race = str(soup.find('base')['href']).split('event/')[1]
    print('Processando os dados da corrida ' + race)
    getRaceAttributes()
    
    if athleteUrl: getSpecificTeam(athleteUrl)
    else: getTeamsAttributes(teams)

    return(
        {
            'place' : place,
            'datetime' : datetime,
            'category' : category,
            'teams' : teams
        }
    )