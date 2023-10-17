import requests

key = "V86v838SJb4GJhpaNbElRqLSLHFhyBc0LPBscDetwnXZosPS2pmtehPSNNsY6Hy1"

print(requests.get("https://www.thebluealliance.com/api/v3/status", headers={"X-TBA-Auth-Key": key}).text)