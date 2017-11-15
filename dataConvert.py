import json
import csv
from datetime import timezone
import datetime

fileName = "peterHr"

with open(fileName + '.json') as data_file:
    data = json.load(data_file)

with open(fileName + ".csv", 'w', newline="") as csv_file:
    wr = csv.writer(csv_file)

    for item in data:
        tmpList = []

        origTimeStr = item["dt"]
        timeObj = datetime.datetime.strptime(origTimeStr, '%B %d %Y %H:%M:%S')
        timezoned = timeObj.replace(tzinfo=timezone.utc).astimezone(tz=None)

        completeTimeStr = timezoned.strftime('%m/%d/%Y %H:%M:%S')

        timeStampArray = completeTimeStr.rsplit(' ', 1)
        date = timeStampArray[0]
        time = timeStampArray[1]

        tmpList.append(date)
        tmpList.append(time)

        for val in item["v"]:
            tmpList.append(val)

        wr.writerow(tmpList)
