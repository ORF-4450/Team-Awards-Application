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
        teamString += "\n\t" + award["name"]
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
                thread.daemon = True
                thread.start()
                toBeRequestedTeams.append(team)
        blueAllianceTeams = match["alliances"]["blue"]["team_keys"]
        for team in blueAllianceTeams:
            if (not team in toBeRequestedTeams) and team != "frc4450":
                thread = threading.Thread(target=getRewards, args=(team,))
                threads.append(thread)
                thread.daemon = True
                thread.start()
                toBeRequestedTeams.append(team)

    for thread in threads:
        thread.join()

    isFinished = True

def waitForFinish():
    global isFinished
    global teams
    if isFinished:
        pleaseWaitLabel.grid_remove()
        teamListBox.configure(listvariable=tkinter.StringVar(value=teams))
        mainContainer.grid(row=0, column=0, sticky=tkinter.NSEW)
    else:
        mainWindow.after(10, waitForFinish)

mainWindow = tkinter.Tk()
mainWindow.geometry("960x540")
mainWindow.rowconfigure(0, weight=1)
mainWindow.columnconfigure(0, weight=1)
pleaseWaitLabel = tkinter.Label(mainWindow, text="Please wait...")
pleaseWaitLabel.grid(row=0, column=0, sticky=tkinter.N)
mainContainer = tkinter.PanedWindow(mainWindow, orient=tkinter.HORIZONTAL)
teamListBox = tkinter.Listbox(mainContainer)
mainContainer.add(teamListBox, sticky=tkinter.NSEW)
teamAwardBox = tkinter.Listbox(mainContainer)
mainContainer.add(teamAwardBox, sticky=tkinter.NSEW)

year = tkinter.simpledialog.askinteger(title="Year", prompt="What year do you want to know the awards of the teams orf4450 has competed with?", minvalue=0)

if (year != None):
    year = str(year)
    isFinished = False
    teams = []
    thread = threading.Thread(target=getTeamData)
    thread.daemon = True
    thread.start()
    mainWindow.after(10, waitForFinish)
else:
    mainWindow.destroy()

mainWindow.mainloop()