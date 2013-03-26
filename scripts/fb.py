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
    count = 0
    for player in rankings:
        f.write('<li')
        if player in keepers:
            count+=1
            f.write(' style="text-decoration: line-through; color: #666;')
        else:
            f.write(' style="font-weight: bold;')
        f.write('"><span style="width: 300px; display: inline-block; text-decoration: inherit;">'+player+'</span>')
        f.write('</li>\n')
    f.write('</ol>')
    f.close()
    print count

if __name__ == '__main__':
    rankings_to_html()
