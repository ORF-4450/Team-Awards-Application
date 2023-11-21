# Task: find all the teams 4450 will be upagainst by finding each match frc4450 had competed in and look up those matches to find the teams in those matches and the rewards

import requests
import json

key = "V86v838SJb4GJhpaNbElRqLSLHFhyBc0LPBscDetwnXZosPS2pmtehPSNNsY6Hy1"

def getData(url):
    response = requests.get(url, headers={"X-TBA-Auth-Key": key})
    response = json.loads(response.text)
    return response

def getRewards(team):
    global year
    data = getData("https://www.thebluealliance.com/api/v3/team/" + team + "/awards/" + year)
    awards = []
    for award in data:
        awards.append(award["name"])
    return awards

year = input("What year do you want to know the teams orf4450 has competed in: ")
print("Please wait...")

matches = getData("https://www.thebluealliance.com/api/v3/team/frc4450/matches/" + year)

teams = []

print("")

for match in matches:
    redAllianceTeams = match["alliances"]["red"]["team_keys"]
    for team in redAllianceTeams:
        if (not team in teams) and team != "frc4450":
            teamString = team
            for award in getRewards(team):
                teamString += "\n\t" + award
            teams.append(teamString)
    blueAllianceTeams = match["alliances"]["blue"]["team_keys"]
    for team in blueAllianceTeams:
        if (not team in teams) and team != "frc4450":
            teamString = team
            for award in getRewards(team):
                teamString += "\n\t" + award
            teams.append(teamString)

for team in teams:
    print(team)