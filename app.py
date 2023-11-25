import requests
import json
import threading
import tkinter
import tkinter.messagebox
import webbrowser

key = "V86v838SJb4GJhpaNbElRqLSLHFhyBc0LPBscDetwnXZosPS2pmtehPSNNsY6Hy1"

def getData(url):
    response = requests.get(url, headers={"X-TBA-Auth-Key": key})
    response = json.loads(response.text)
    return response

def getRewards(team):
    global year
    global isFinished
    global currentAwards

    currentAwards = []

    isFinished = False
    data = getData("https://www.thebluealliance.com/api/v3/team/" + team + "/awards/" + year)
    for award in data:
        currentAwards.append(award["name"])

    isFinished = True

def getTeams():
    global isFinished
    global year
    global teams

    isFinished = False
    matches = getData("https://www.thebluealliance.com/api/v3/team/frc4450/matches/" + year)

    teams = []

    for match in matches:
        redAllianceTeams = match["alliances"]["red"]["team_keys"]
        for team in redAllianceTeams:
            if (not team in teams) and team != "frc4450":
                teams.append(team)
        blueAllianceTeams = match["alliances"]["blue"]["team_keys"]
        for team in blueAllianceTeams:
            if (not team in team) and team != "frc4450":
                team.append(team)

    isFinished = True

def waitForFinish():
    global isFinished
    global teams
    global requestType
    global currentAwards
    if isFinished:
        if (requestType == "team"):
            pleaseWaitLabel.grid_forget()
            teamListBox.configure(listvariable=tkinter.StringVar(value=teams))
            mainContainer.grid(row=1, column=0, columnspan=2, sticky="NSEW")
            submitButton.configure(state=tkinter.NORMAL)
        if (requestType == "award"):
            teamAwardLabel.grid_forget()
            teamAwardBox.configure(listvariable=tkinter.StringVar(value=currentAwards))
            teamAwardBox.grid(row=0, column=0, sticky="NSEW")
            teamAwardBox.configure(state=tkinter.NORMAL)
            submitButton.configure(state=tkinter.NORMAL)
    else:
        mainWindow.after(10, waitForFinish)

def submitRequest(*args):
    global year
    global requestType
    try:
        year = int(yearInput.get())
        if year < 0:
            raise ValueError()
    except ValueError:
        tkinter.messagebox.showerror(title="Error", message="Please enter a positive number")
    else:
        requestType = "team"
        year = str(year)
        thread = threading.Thread(target=getTeams)
        thread.daemon = True
        thread.start()
        submitButton.configure(state=tkinter.DISABLED)
        mainContainer.grid_forget()
        pleaseWaitLabel.grid(row=1, column=0, columnspan=2, sticky="N")
        teamAwardBox.grid_forget()
        teamAwardLabel.configure(text="Please select a team")
        teamAwardLabel.grid(row=0, column=0, sticky="N")
        mainWindow.after(10, waitForFinish)

def submitAwardRequest(*args):
    global requestType
    requestType = "award"
    thread = threading.Thread(target=getRewards, args=(str(teams[teamListBox.curselection()[0]]),))
    thread.daemon = True
    thread.start()
    teamAwardBox.grid_forget()
    teamAwardLabel.configure(text="Please wait...")
    teamAwardLabel.grid(row=0, column=0, sticky="N")
    teamAwardBox.configure(state=tkinter.DISABLED)
    submitButton.configure(state=tkinter.DISABLED)
    mainWindow.after(10, waitForFinish)

def openTBA(*args):
    webbrowser.open_new_tab("https://www.thebluealliance.com/")

mainWindow = tkinter.Tk()
mainWindow.geometry("960x540")
mainWindow.title("orf4450 Team Awards Application")
mainWindow.rowconfigure(1, weight=1)
mainWindow.columnconfigure(0, weight=1)
yearInput = tkinter.Entry(mainWindow)
yearInput.grid(row=0, column=0, sticky="NSEW")
submitButton = tkinter.Button(mainWindow, text="Submit", command=submitRequest)
submitButton.grid(row=0, column=1)
pleaseWaitLabel = tkinter.Label(mainWindow, text="Please wait...")
mainContainer = tkinter.PanedWindow(mainWindow, orient=tkinter.HORIZONTAL)
teamListBox = tkinter.Listbox(mainContainer)
mainContainer.add(teamListBox, sticky="NSEW")
awardContainer = tkinter.Frame(mainContainer)
awardContainer.rowconfigure(0, weight=1)
awardContainer.columnconfigure(0, weight=1)
teamAwardBox = tkinter.Listbox(awardContainer)
teamAwardLabel = tkinter.Label(awardContainer, text="Please select a team")
teamAwardLabel.grid(row=0, column=0, sticky="N")
tbaButton = tkinter.Button(mainWindow, text="Powered by The Blue Alliance", relief="flat", command=openTBA)
tbaButton.grid(row=2, column=0, columnspan=2, sticky="N")
mainContainer.add(awardContainer, sticky="NSEW")

teamListBox.bind("<<ListboxSelect>>", submitAwardRequest)
yearInput.bind("<KeyPress-Return>", submitRequest)

mainWindow.mainloop()