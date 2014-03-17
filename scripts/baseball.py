import csv

DEFAULT_TEAMLIST = '../teamdata/2014/KeeperList.csv'
DEFAULT_PROJECTIONS = '../projections/2014/FanGraphsBatters.csv'
DEFAULT_PITCHER_PROJECTIONS = '../projections/2014/FanGraphsPitchers.csv'
DEFAULT_FARMLIST = '../teamdata/2014/FarmList.csv'
DEFAULT_DRAFTEDLIST = '../teamdata/2014/DraftedList.csv'
DEFAULT_RANKINGS = '../projections/2014/FantasyProsRankings.csv'

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

    def process_csv(self, csv_path=None):
        if not csv_path: csv_path = self.csv
        with open(csv_path, 'rb') as csvfile:
            csv_rows = [row for row in csv.reader(csvfile, delimiter='\t')]
        self.add_players(csv_rows)

    def add_players(self, csv_rows):
        for col in range(len(csv_rows[0])):
            team = csv_rows[0][col]
            players = [row[col] for row in csv_rows[1:] if row[col]]
            try:
                self.teams[team].extend(players)
            except KeyError:
                self.teams[team] = players

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

class RankingsDisplay:
    def __init__(self):
        self.players_taken = []
        self.rankings = self.process_fantasy_rankings()
        self.update_taken()

    def update_taken(self):
        league = FantasyLeague()
        league.process_csv(DEFAULT_FARMLIST)
        league.process_csv(DEFAULT_DRAFTEDLIST)
        taken = []
        for team in league.teams: taken.extend(league.teams[team])
        self.players_taken = taken

    def process_fantasy_rankings(self):
        rankings = []
        with open(DEFAULT_RANKINGS, 'rb') as csvfile:
            rankings_reader = csv.reader(csvfile, delimiter='\t')
            rows = []
            for row in rankings_reader:
                rankings.append(row[0])
        return rankings[1:]

    def to_html(self, filename='rankings.html'):
        f = open(filename, 'w')
        f.write('<ol>\n')
        self.update_taken()
        projections = Projections()
        pitcher_projections = Projections(csv=DEFAULT_PITCHER_PROJECTIONS)
        count = 0
        for player in self.rankings:
            f.write('<li')
            if player in self.players_taken:
                count+=1
                f.write(' style="text-decoration: line-through; color: #666;')
            else:
                f.write(' style="font-weight: bold;')
            f.write('"><span style="width: 300px; display: inline-block; text-decoration: inherit;">'+player+'</span>')
            f.write('<span style="width: 100px; display: inline-block;">')
            if projections.exists(player): f.write(projections.for_player(player)['OPS'])
            f.write("</span>")
            f.write('<span style="width: 100px; display inline-block;">')
            if pitcher_projections.exists(player):
                f.write(pitcher_projections.for_player(player)['WHIP'])
            f.write("</span>")
            f.write('</li>\n')
        f.write('</ol>')
        f.close()
        print count

if __name__ == '__main__':
    RankingsDisplay().to_html()
