"""
IDK WHAT RFC 3339 FORMAT IS BUT IM LEARNING WHILE IM GOING
startDate, endDate = VALUES OF INTEREST

Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Ahmed’s Apple Watch" value="HKCategoryValueSleepAnalysisInBed"

I DONT STRESS ABOUT THIS HOBBY PROJECT WILL BE DR EITHER WAY
STRESS WENT SO DOWN THANKS, ALL DONE!
"""
# not yet set up start end date setting here
START_DATE = ""
END_DATE = ""

from bs4 import BeautifulSoup
import googleCalendar

def convert_applehealth_datetime_to_gcalendar_format(applehealth_datetime):
    words = applehealth_datetime.split(" ")
    g_calendar_datetime = words[0] + "T" + words[1]
    return g_calendar_datetime

with open('export.xml', "r") as file:
    data = file.read()
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
xml_data = BeautifulSoup(data, "xml")
# print(xml_data)


#  FILTER DATA FOR RECORD TYPE AND SAVE
#  FILTER DATA FOR SOURCENAME AND VALUE AND SAVE
#  AWAKE OR IN BED (= ASLEEP)
records = xml_data.find_all(type="HKCategoryTypeIdentifierSleepAnalysis",value="HKCategoryValueSleepAnalysisInBed", sourceName="Ahmed’s Apple Watch")

# TODO EXTRACT DATE, STARTDATE(TIME) AND ENDDATE(TIME) TO PY OBJECT
data = []
for record in records:
    record_data_to_be_saved = {
        "Data Type": record["value"],
        "Source": record["sourceName"],
        "Start DateTime": record["startDate"],
        "End DateTime": record["endDate"],
    }
    data.append(record_data_to_be_saved)


#  MANIPULATE DATA TO FIT REQUIREMENTS OF GOOGLECALENDAR API - PENDING (DATETIME REQUIREMENTS)
for record in data:
    fixed_source_name = ""
    if record["Source"] == 'Ahmed’s Apple\xa0Watch':
        record["Source"] = 'Apple Watch'
    record["Start DateTime"] = convert_applehealth_datetime_to_gcalendar_format(record["Start DateTime"])
    record["End DateTime"] = convert_applehealth_datetime_to_gcalendar_format(record["End DateTime"])


# TODO OPTIONAL SAVE TO CSV
# TODO OPTIONAL SWITCH TO PANDAS
# TODO OPTIONAL GRAPH RESULTS

#TODO MAKE THE DATA SHORTER SO I DONT BLOW UP MY CALENDAR
# PUSH AND BUGFIX

print(len(data))
# print(data[-1])
# print("MINUS 1 ABOVE")
# shortdata = data[-10:]
# print(shortdata)
# print(len(shortdata))


# TODO OPTIONAL CHECK IF SLEEP EVENT ALREADY EXISTS
API = googleCalendar.GoogleCalendarAPI()

# MAKE EVENT PUSHING CODE INTEGRATING DATA
for record in data:
    # print(record)
    # print(record['Source'])
    # print(record['Start DateTime'])
    # print(record['End DateTime'])
    API.create_event(event_name=f"Sleep ({record['Source']})", startDateTime=record['Start DateTime'], endDateTime=record["End DateTime"], colorId= None)
    print(f"Event for record starting on {record['Start DateTime']} added.")

