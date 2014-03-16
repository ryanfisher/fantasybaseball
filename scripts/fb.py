import csv

TEAM_LIST = 'teamdata/2014/KeeperList.csv'
PROJECTIONS = 'projections/2014/FanGraphsBatters.csv'

def process_fantasy_rankings():
    rankings = []
    with open('fantasy_rankings.csv', 'rb') as csvfile:
        rankings_reader = csv.reader(csvfile, delimiter='\t')
        rows = []
        for row in rankings_reader:
            rankings.append(row[0])
    return rankings[1:]

def process_team_list(filename=TEAM_LIST):
    with open(filename, 'rb') as csvfile:
        keeper_reader = csv.reader(csvfile, delimiter='\t')
        rows = []
        for row in keeper_reader:
            rows.append(row)
    teams = {}
    for team in range(10):
        teams[rows[0][team]] = [row[team] for row in rows][1:]
    return teams

def projections_dict(filename=PROJECTIONS):
    with open(filename, 'rb') as csvfile:
        projections_reader = csv.reader(csvfile, delimiter=',')
        projections = {}
        stat_name = projections_reader.next()
        for row in projections_reader:
            stats = {}
            for n in range(len(row)):
                stats[stat_name[n]] = row[n]
            projections[row[0]] = stats
    return projections

def keeper_list():
    keepers = []
    l = process_team_list(TEAM_LIST)
    for key in l:
        keepers.extend(l[key])
    return keepers

def team_list():
    players_taken = []
    keepers = process_team_list(TEAM_LIST)
    for key in keepers: players_taken.extend(keepers[key])
    farm_players = process_team_list('FarmList.csv')
    for key in farm_players: players_taken.extend(farm_players[key])
    drafted = process_team_list('DraftedList.csv')
    for key in drafted: players_taken.extend(drafted[key])
    return players_taken

def rankings_to_html(filename='rankings.html'):
    rankings = process_fantasy_rankings()
    f = open(filename, 'w')
    f.write('<ol>\n')
    keepers = team_list()
    projections = projections_dict()
    pitcher_projections = projections_dict('FanGraphsPitcherProjections.csv')
    count = 0
    for player in rankings:
        f.write('<li')
        if player in keepers:
            count+=1
            f.write(' style="text-decoration: line-through; color: #666;')
        else:
            f.write(' style="font-weight: bold;')
        f.write('"><span style="width: 300px; display: inline-block; text-decoration: inherit;">'+player+'</span>')
        f.write('<span style="width: 100px; display: inline-block;">')
        if player in projections: f.write(projections[player][17])
        f.write("</span>")
        f.write('<span style="width: 100px; display inline-block;">')
        if player in pitcher_projections:
            f.write(pitcher_projections[player][12])
        f.write("</span>")
        f.write('</li>\n')
    f.write('</ol>')
    f.close()
    print count

def stat_list_for(team, stat):
    p = projections_dict()
    keepers = process_team_list()
    return [p[player][stat] for player in keepers[team] if player in p]

def average(l):
    return sum([float(i) for i in l]) / float(len(l))

def averages():
    keepers = process_team_list()
    averages_dict = {}
    for key in keepers:
        averages_dict[key] = averages_for(key)
    return averages_dict

def averages_for(team):
    avg_values = {}
    for stat in ['SB','R','H','RBI','HR','AVG','OPS']:
        avg_values[stat] = average(stat_list_for(team, stat))
    return avg_values

def sorted_stat(averages, stat):
    return sorted([(averages[key][stat], key) for key in averages])

def update_team_ranks(team_values, sorted_list):
    for n in range(len(sorted_list)):
        manager = sorted_list[n][1]
        team_values[manager] += n
    return team_values

def compute_ranks():
    avgs = averages()
    teams_dict = {}
    for manager in avgs:
        teams_dict[manager] = 0
    for stat in ['HR','AVG','R','RBI','OPS','SB']:
        teams_dict = update_team_ranks(teams_dict, sorted_stat(avgs, stat))
    return sorted([(teams_dict[manager], manager) for manager in teams_dict])

if __name__ == '__main__':
    print compute_ranks()
