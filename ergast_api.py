#API documentation http://ergast.com/mrd/
import requests
import json
import os

class Ergast():

    def __init__(self, season='current'):
        self.season = season
        
        path = '{}'.format(os.path.abspath('C:'))

        if not os.path.isdir('data'):
            os.mkdir('{}/data'.format(path))

        if not os.path.isdir('data/{}'.format(self.season)):
            os.mkdir('{}/data/{}'.format(path,self.season))

        if not os.path.isfile('data/{}/{}_season'.format(self.season,self.season)):
            url = 'http://ergast.com/api/f1/{}.json'.format(self.season)
            data = requests.get(url)
            data = data.json()

            with open('data/{}/{}_season'.format(self.season,self.season),'w') as outfile:
                json.dump(data, outfile)        

    def raceName(self, raceNumber):
        with open('data/{}/{}_season'.format(self.season,self.season),'r') as json_file:
            data = json.load(json_file)

        data = data['MRData']['RaceTable']['Races'][raceNumber]
        return data['raceName']

    def raceDate(self, raceNumber):
        with open('data/{}/{}_season'.format(self.season,self.season),'r') as json_file:
            data = json.load(json_file)

        data = data['MRData']['RaceTable']['Races'][raceNumber]
        return data['date']

    def allRaces(self):
        with open('data/{}/{}_season'.format(self.season,self.season),'r') as json_file:
            data = json.load(json_file)

        total_races = data['MRData']['total']
        allRaces = []
        for i in range(int(total_races)):
            allRaces.append([self.raceName(i),self.raceDate(i)])
        return allRaces, total_races
    
    def driverStandings(self,):
        if not os.path.isfile('data/{}/{}_driverStandings'.format(self.season,self.season)) or self.season == 'current' or self.season == '2019':
            url = 'http://ergast.com/api/f1/{}/driverStandings.json'.format(self.season)
            data = requests.get(url)
            data = data.json()

            with open('data/{}/{}_driverStandings'.format(self.season,self.season),'w') as outfile:
                json.dump(data, outfile)

        with open('data/{}/{}_driverStandings'.format(self.season,self.season),'r') as json_file:
            data = json.load(json_file)

        total_limit = data['MRData']['limit']
        total_limit = int(total_limit)
        total_drivers = data['MRData']['total']
        total_drivers = int(total_drivers)
        if total_limit < total_drivers: total_drivers = total_limit
        data = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        driverStandings = []
        for i in range(int(total_drivers)):
            driverStandings.append([data[i]['position'],
                                    str(data[i]['Driver']['givenName'])+' '+
                                    str(data[i]['Driver']['familyName']),
                                    data[i]['Constructors'][0]['name'],
                                    data[i]['points'],
                                    data[i]['wins'],
                                    data[i]['Driver']['familyName'][:3]])
        return driverStandings, int(total_drivers)

    def constructorStandings(self):
        if not os.path.isfile('data/{}/{}_constructorStandings'.format(self.season,self.season)) or self.season == 'current' or self.season == '2019':
            url = 'http://ergast.com/api/f1/{}/constructorStandings.json'.format(self.season)
            data = requests.get(url)
            data = data.json()

            with open('data/{}/{}_constructorStandings'.format(self.season,self.season),'w') as outfile:
                json.dump(data, outfile)

        with open('data/{}/{}_constructorStandings'.format(self.season,self.season),'r') as json_file:
            data = json.load(json_file)

        total_limit = data['MRData']['limit']
        total_limit = int(total_limit)
        total_constructors = data['MRData']['total']
        total_constructors = int(total_constructors)
        if total_limit < total_constructors: total_constructors = total_limit
        data = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
        constructorStandings = []
        for i in range(total_constructors):
            constructorStandings.append([data[i]['position'],
                                        data[i]['Constructor']['name'],
                                        data[i]['points'],
                                        data[i]['wins']])
        return constructorStandings, total_constructors

    def nextRace(self):
        last_race_url = 'http://ergast.com/api/f1/current/next.json'
        data = requests.get(last_race_url)
        data = data.json()
        data = data['MRData']['RaceTable']['Races'][0]
        race_name = data['raceName']
        race_date = data['date']
        return [race_name, race_date]


def currentSeason():
    url = 'http://ergast.com/api/f1/current.json'
    data = requests.get(url)
    data = data.json()
    currentSeason = data['MRData']['RaceTable']['season']
    return int(currentSeason)
