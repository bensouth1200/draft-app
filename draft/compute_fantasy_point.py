import sys, getopt
import numpy as mp
import pandas as pd

cmd_args = sys.argv

year = cmd_args[1]
print(type(year))
# read in the input data
qbs = pd.read_csv('Game_Logs_Quarterback.csv')
rbs = pd.read_csv('Game_Logs_Runningback.csv')
wrs = pd.read_csv('Game_Logs_Wide_Receiver_and_Tight_End.csv')

def compute_fantasy_points(passing_yards = 0, passing_TDs = 0, INTs = 0, rushing_yards = 0, rushing_TDs = 0, receiving_yards = 0, receiving_TDs = 0, Fumbles = 0):
    return passing_yards * 0.04 + passing_TDs * 4 - INTs * 2 + rushing_yards * 0.1 + rushing_TDs * 6 + receiving_yards * 0.1 + receiving_TDs * 6 - Fumbles * 2
# filter out games in different years and non-regular season games
#print(type(qbs.Year[0]))
#qbs = qbs[qbs.Year == year]
#qbs = qbs[qbs.Season == 'Regular Season']
#rbs = rbs[rbs.Year == year]
#rbs = rbs[rbs.Season == 'Regular Season']
#wrs = wrs[wrs.Year == year]
#wrs = wrs[wrs.Season == 'Regular Season']

# create space for output csv files
stats = []
fantasy_points = []

# parse through qbs dataset
for row in range(len(qbs)):
    if qbs['Year'][row] == int(year) and qbs['Season'][row] == 'Regular Season':
        if qbs['Passing Yards'][row] == '--':
            qbs['Passing Yards'][row] = 0

        if qbs['TD Passes'][row] == '--':
            qbs['TD Passes'][row] = 0

        if qbs['Ints'][row] == '--':
            qbs['Ints'][row] = 0

        if qbs['Rushing Yards'][row] == '--':
            qbs['Rushing Yards'][row] = 0

        if qbs['Rushing TDs'][row] == '--':
            qbs['Rushing TDs'][row] = 0

        if qbs['Fumbles'][row] == '--':
            qbs['Fumbles'][row] = 0

        #print("Passing Yards: " + str(type(qbs['Passing Yards'][row])))
        #print("TD Passes: " + str(type(qbs['TD Passes'][row])))
        #print("Ints: " + str(type(qbs['Ints'][row])))
        #print("Rushing Yards: " + str(type(qbs['Rushing Yards'][row])))
        #print("Rushing TDs: " + str(type(qbs['Rushing TDs'][row])))
        #print("Fumbles: " + str(type(qbs['Fumbles'][row])))
        fantasy_pts = compute_fantasy_points(int(qbs.replace(',','')['Passing Yards'][row]), int(qbs.replace(',','')['TD Passes'][row]), int(qbs.replace(',','')['Ints'][row]), int(qbs.replace(',','')['Rushing Yards'][row]), int(qbs.replace(',','')['Rushing TDs'][row]), 0, 0, int(qbs.replace(',','')['Fumbles'][row]))

        stats.append([qbs['Player Id'][row], qbs['Name'][row], 'QB', year, qbs['Week'][row], qbs['Home or Away'][row], qbs['Opponent'][row], qbs['Passes Completed'][row], qbs['Passes Attempted'][row], qbs['Completion Percentage'][row], qbs['Passing Yards'][row], qbs['TD Passes'][row], qbs['Ints'][row], qbs['Rushing Attempts'][row], qbs['Rushing Yards'][row], qbs['Rushing TDs'][row], qbs['Fumbles'][row], 0, 0, 0])

        fantasy_points.append([qbs['Player Id'][row], qbs['Name'][row], 'QB', year, qbs['Week'][row], fantasy_pts])

# parse through rbs dataset
for row in range(len(rbs)):
    if rbs['Year'][row] == int(year) and rbs['Season'][row] == 'Regular Season':
        if rbs['Rushing Yards'][row] == '--':
            rbs['Rushing Yards'][row] = 0

        if rbs['Rushing TDs'][row] == '--':
            rbs['Rushing TDs'][row] = 0

        if rbs['Fumbles'][row] == '--':
            rbs['Fumbles'][row] = 0

        if rbs['Receiving Yards'][row] == '--':
            rbs['Receiving Yards'][row] = 0

        if rbs['Receiving TDs'][row] == '--':
            rbs['Receiving TDs'][row] = 0

        fantasy_pts = compute_fantasy_points(0, 0, 0, int(rbs.replace(',','')['Rushing Yards'][row]), int(rbs.replace(',','')['Rushing TDs'][row]), int(rbs.replace(',','')['Receiving Yards'][row]), int(rbs.replace(',','')['Receiving TDs'][row]), int(rbs.replace(',','')['Fumbles'][row]))

        stats.append([rbs['Player Id'][row], rbs['Name'][row], 'RB', year, rbs['Week'][row], rbs['Home or Away'][row], rbs['Opponent'][row], 0, 0, 0, 0, 0, 0, rbs['Rushing Attempts'][row], rbs['Rushing Yards'][row], rbs['Rushing TDs'][row], rbs['Fumbles'][row], rbs['Receptions'][row], rbs['Receiving Yards'][row], rbs['Receiving TDs'][row]])

        fantasy_points.append([rbs['Player Id'][row], rbs['Name'][row], 'RB', year, rbs['Week'][row], fantasy_pts])

# parse through wrs/TEs dataset
for row in range(len(wrs)):
    if wrs['Year'][row] == int(year) and wrs['Season'][row] == 'Regular Season':
        if wrs['Rushing Yards'][row] == '--':
            wrs['Rushing Yards'][row] = 0

        if wrs['Rushing TDs'][row] == '--':
            wrs['Rushing TDs'][row] = 0

        if wrs['Fumbles'][row] == '--':
            wrs['Fumbles'][row] = 0

        if wrs['Receiving Yards'][row] == '--':
            wrs['Receiving Yards'][row] = 0

        if wrs['Receiving TDs'][row] == '--':
            wrs['Receiving TDs'][row] = 0

        fantasy_pts = compute_fantasy_points(0, 0, 0, int(wrs.replace(',','')['Rushing Yards'][row]), int(wrs.replace(',','')['Rushing TDs'][row]), int(wrs.replace(',','')['Receiving Yards'][row]), int(wrs.replace(',','')['Receiving TDs'][row]), int(wrs.replace(',','')['Fumbles'][row]))

        stats.append([wrs['Player Id'][row], wrs['Name'][row], wrs['Position'][row], year, wrs['Week'][row], wrs['Home or Away'][row], wrs['Opponent'][row], 0, 0, 0, 0, 0, 0, wrs['Rushing Attempts'][row], wrs['Rushing Yards'][row], wrs['Rushing TDs'][row], wrs['Fumbles'][row], wrs['Receptions'][row], wrs['Receiving Yards'][row], wrs['Receiving TDs'][row]])

        fantasy_points.append([wrs['Player Id'][row], wrs['Name'][row], wrs['Position'][row], year, wrs['Week'][row], fantasy_pts])

print(stats)
# export the data
stats_df = pd.DataFrame(stats, columns=['Player Id', 'Name', 'Position', 'Year', 'Week', 'Home or Away', 'Opponent', 'Passes Completed', 'Passes Attempted', 'Completion Percentage', 'Passing Yards', 'TD Passes', 'Ints', 'Rushing Attempts', 'Rushing Yards', 'Rushing TDs', 'Fumbles', 'Receptions', 'Receiving Yards', 'Receiving TDs'])

fantasy_points_df = pd.DataFrame(fantasy_points, columns=['Player Id', 'Name', 'Position', 'Year', 'Week', 'Fantasy Points'])

stats_df.to_csv('stats.csv')

fantasy_points_df.to_csv('fantasy_points.csv')


