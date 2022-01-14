import requests

MIN_MILLSECS = 600000
response = requests.get("https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=1722175e22e122a9e19c9ec20211")
unsortedEvents = response.json()['events']
events = sorted(unsortedEvents, key=lambda x: (x['visitorId'],x['timestamp']))

sessionsByUser = {}
#sliding window approach
for i, el in enumerate(events):
    url, visitorId, timestamp = el['url'], el['visitorId'], el['timestamp']
    #first event or new session for another user
    if i==0 or visitorId!=events[i-1]['visitorId']:
        firstSession = {'duration': 0, 'pages': [url], 'startTime': timestamp}
        sessionsByUser[visitorId] = [firstSession]
    #new event is within the 10 mins window
    elif timestamp - events[i-1]['timestamp'] <= MIN_MILLSECS:
        lastSession = sessionsByUser[visitorId][-1]
        lastSession['pages'].append(url)
        lastSession['duration']=timestamp - lastSession['startTime']
    #new event isn't a part of the last session
    else:
        newSession = {'duration': 0, 'pages': [url], 'startTime': timestamp}
        sessionsByUser[visitorId].append(newSession)

result = {"sessionsByUser": sessionsByUser}
r = requests.post("https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=1722175e22e122a9e19c9ec20211", json=result)
if r.status_code == 200:
    print("HOORAY!!!")
