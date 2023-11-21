# Task: find all the teams 4450 will be upagainst by finding each match frc4450 had competed in and look up those matches to find the teams in those matches and the rewards

import requests
import json
import threading
import tkinter
import tkinter.simpledialog

key = "V86v838SJb4GJhpaNbElRqLSLHFhyBc0LPBscDetwnXZosPS2pmtehPSNNsY6Hy1"

def getData(url):
    response = requests.get(url, headers={"X-TBA-Auth-Key": key})
    response = json.loads(response.text)
    return response

def getRewards(team):
    global year
    teamString = team
    data = getData("https://www.thebluealliance.com/api/v3/team/" + team + "/awards/" + year)
    for award in data:
        teamString += "\n\t" + award["name"];
    teams.append(teamString)

def getTeamData():
    global isFinished
    matches = getData("https://www.thebluealliance.com/api/v3/team/frc4450/matches/" + year)

    toBeRequestedTeams = []
    threads = []

    for match in matches:
        redAllianceTeams = match["alliances"]["red"]["team_keys"]
        for team in redAllianceTeams:
            if (not team in toBeRequestedTeams) and team != "frc4450":
                thread = threading.Thread(target=getRewards, args=(team,))
                threads.append(thread)
                thread.start()
                toBeRequestedTeams.append(team)
        blueAllianceTeams = match["alliances"]["blue"]["team_keys"]
        for team in blueAllianceTeams:
            if (not team in toBeRequestedTeams) and team != "frc4450":
                thread = threading.Thread(target=getRewards, args=(team,))
                threads.append(thread)
                thread.start()
                toBeRequestedTeams.append(team)

    for thread in threads:
        thread.join()

    isFinished = True

def waitForFinish():
    global isFinished
    if isFinished:
        mainWindow.after_cancel(waitForFinishInterval)
        print("")
        for team in teams:
            print(team)

mainWindow = tkinter.Tk()
pleaseWaitLabel = tkinter.Label(mainWindow, text="Please wait...")
pleaseWaitLabel.pack()

year = tkinter.simpledialog.askinteger(title="Year", prompt="What year do you want to know the awards of the teams orf4450 has competed with?", minvalue=0)

if (year != None):
    year = str(year)
    isFinished = False
    teams = []
    thread = threading.Thread(target=getTeamData)
    thread.start()
    waitForFinishInterval = mainWindow.after(10, waitForFinish)
else:
    mainWindow.destroy()

mainWindow.mainloop()