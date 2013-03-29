import csv

def process_fantasy_rankings():
    rankings = []
    with open('fantasy_rankings.csv', 'rb') as csvfile:
        rankings_reader = csv.reader(csvfile, delimiter='\t')
        rows = []
        for row in rankings_reader:
            rankings.append(row[0])
    return rankings[1:]

def process_team_list(filename='KeeperList.csv'):
    with open(filename, 'rb') as csvfile:
        keeper_reader = csv.reader(csvfile, delimiter='\t')
        rows = []
        for row in keeper_reader:
            rows.append(row)
    teams = {}
    for team in range(10):
        teams[rows[0][team]] = [row[team] for row in rows][1:]
    return teams

def projections_dict(filename='FanGraphsProjections.csv'):
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
    l = process_team_list('KeeperList.csv')
    for key in l:
        keepers.extend(l[key])
    return keepers

def team_list():
    players_taken = []
    keepers = process_team_list('KeeperList.csv')
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
    ops_list = stat_list_for(team, 'OPS')
    avg_list = stat_list_for(team, 'AVG')
    hit_list = stat_list_for(team, 'H')
    run_list = stat_list_for(team, 'R')
    rbi_list = stat_list_for(team, 'RBI')
    hr_list = stat_list_for(team, 'HR')
    ab_list = stat_list_for(team, 'AB')
    averages = {
        'runs': average(run_list),
        'hits': average(hit_list),
        'rbi': average(rbi_list),
        'hr': average(hr_list),
    }
    return averages

if __name__ == '__main__':
    rankings_to_html()
