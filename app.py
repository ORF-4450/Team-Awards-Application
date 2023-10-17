# Task: find all the teams 4450 will be upagainst by finding each event 4450 is competing in and looking at those teams

import requests
import pandas
import json

key = "V86v838SJb4GJhpaNbElRqLSLHFhyBc0LPBscDetwnXZosPS2pmtehPSNNsY6Hy1"

def getData(url):
    response = requests.get(url, headers={"X-TBA-Auth-Key": key})
    response = json.loads(response.text)
    return pandas.DataFrame.from_records(response)

print(getData("https://www.thebluealliance.com/api/v3/events/2023").query(""))