import csv

class Player:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.position = kwargs['position']
        self.aliases = kwargs['aliases']

class FantasyTeam:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.owner = kwargs['owner']
        self.players = kwargs['players']

class League:
    def __init__(self, **kwargs):
        self.teams = ['teams']

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
