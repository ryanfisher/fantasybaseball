import csv

DEFAULT_TEAMLIST = '../teamdata/2014/KeeperList.csv'
DEFAULT_PROJECTIONS = '../projections/2014/FanGraphsBatters.csv'

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

class FantasyLeague:
    def __init__(self, **kwargs):
        self.teams = kwargs.get('teams', {})
        self.csv = kwargs.get('csv', DEFAULT_TEAMLIST)
        if self.teams == {}: self.process_csv()

    def process_csv(self):
        with open(self.csv, 'rb') as csvfile:
            rows = [row for row in csv.reader(csvfile, delimiter='\t')]
        for team in range(10):
            self.teams[rows[0][team]] = [row[team] for row in rows][1:]

    def stat_list_for(self, team, stat):
        p = Projections()
        player_projections = [player for player in self.teams[team] if p.exists(player)]
        return [p.for_player(player)[stat] for player in player_projections]

    def average(self, l):
        return sum([float(i) for i in l]) / float(len(l))

    def averages_for(self, team):
        avg_values = {}
        stats = ['SB','R','H','RBI','HR','AVG','OPS']
        for stat in stats:
            avg_values[stat] = self.average(self.stat_list_for(team, stat))
        return avg_values

    def averages(self):
        return {team: self.averages_for(team) for team in self.teams}

class LeagueRankings:
    def sorted_stat(self, averages, stat):
        return sorted([(averages[key][stat], key) for key in averages])

    def update_team_ranks(self, team_values, sorted_list):
        for n in range(len(sorted_list)):
            manager = sorted_list[n][1]
            team_values[manager] += n
        return team_values

    def compute_ranks(self, league):
        avgs = league.averages()
        teams_dict = {manager: 0 for manager in avgs}
        for stat in ['HR','AVG','R','RBI','OPS','SB']:
            teams_dict = self.update_team_ranks(teams_dict, self.sorted_stat(avgs, stat))
        return sorted([(teams_dict[manager], manager) for manager in teams_dict])


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

    def exists(self, player):
        return player in self.projections

    def for_player(self, player):
        return self.projections[player]
