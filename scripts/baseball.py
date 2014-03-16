import csv

class Player:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.position = kwargs.get('positions', [])
        self.aliases = kwargs.get('aliases', [])

class FantasyTeam:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.owner = kwargs.get('owner', '')
        self.players = kwargs.get('players', [])

DEFAULT_TEAMLIST = '../teamdata/2014/KeeperList.csv'

class FantasyLeague:
    def __init__(self, **kwargs):
        self.teams = kwargs.get('teams', {})
        self.csv = kwargs.get('csv', DEFAULT_TEAMLIST)
        if self.teams == {}: self.process_teams()

    def process_teams(self):
        with open(self.csv, 'rb') as csvfile:
            keeper_reader = csv.reader(csvfile, delimiter='\t')
            rows = []
            for row in keeper_reader:
                rows.append(row)
        for team in range(10):
            self.teams[rows[0][team]] = [row[team] for row in rows][1:]

DEFAULT_PROJECTIONS = '../projections/2014/FanGraphsBatters.csv'

class Projections:
    def __init__(self, **kwargs):
        self.csv = kwargs.get('csv', DEFAULT_PROJECTIONS)
        self.projections = {}
        self.process_projections()

    def process_projections(self):
        with open(self.csv, 'rb') as csvfile:
            projections_reader = csv.reader(csvfile, delimiter=',')
            stat_name = projections_reader.next()
            for row in projections_reader:
                stats = {}
                for n in range(len(row)):
                    stats[stat_name[n]] = row[n]
                self.projections[row[0]] = stats

    def for_player(self, player):
        return self.projections[player]
