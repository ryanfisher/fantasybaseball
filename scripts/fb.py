import csv

def process_csv():
    with open('KeeperList.csv', 'rb') as csvfile:
        keeper_reader = csv.reader(csvfile, delimiter=',')
        rows = []
        for row in keeper_reader:
            rows.append(row)
    teams = {}
    for team in range(10):
        teams[rows[0][team]] = [row[team] for row in rows][1:]
    return teams

process_csv()
