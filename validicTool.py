#validicTool
#Tool that scrapes Validic API for fitness data
#Author: Lewis Yates
#Date: 20/02/2018

import json, requests, time

#Variable Declaration

#5a4f8fd1fe065b4b027f4d0a - Lewis
#5a560faf84cf4c0019d96f1c - John
#5a500925fe35fd4ad88c534d - Nash
org_token = "57cf1569ff9d930009000082"
access_token = "0c0ebc2587463e3da2c785c6d8cd2d5cfb3fbe51af07d2e873b50d2aac67c4a4"

print("")
print("Welcome to Validic Tool (roadtohealth)")
print("")

user_token = input("Please enter your Validic user token:\n")
print("")

#start_date = input("Please enter your start date (YYYY-MM-DD):\n")
#end_date = input("Please enter your end date (YYYY-MM-DD):\n")
#start_time = input("Please enter your start time (HH:MM:SS):\n")
#end_time = input("Please enter your end time (HH:MM:SS):\n")

start_date = '2018-02-20'
end_date = '2018-02-20'
start_time = '00:00:00'
end_time = '23:59:59'

#Set activity type
temp_activity = input("Please enter your activity type:\n[1] Fitness\n[2] Routine\n")

if temp_activity == '1':
    user_activity = "fitness"
elif temp_activity == '2':
    user_activity = "routine"

url = 'https://api.validic.com/v1/organizations/' + org_token + '/users/' + user_token + '/' + user_activity + '.json?access_token=' + access_token + '&start_date=' + start_date + '%20' + start_time + '&end_date=' + end_date + '%20' + end_time + '&expanded=1'

print(url)

#get API response in JSON format
try:
    resp = requests.get(url=url)
#Else respond with appropriate Error Message
except:
    print(resp)
    exit()

#load data into JSON format
data = json.loads(resp.text)
print(data)
#foreach different type of activity - display the results
if user_activity == "routine":
    print("\nSource:\t\t", data['routine'][0]['source_name'])
    print("Steps:\t\t", data['routine'][0]['steps'])
    print("Duration:\t",round((data['routine'][0]['active_duration'])/60, 2),"mins")
    print("Calories:\t",data['routine'][0]['calories_burned'],"kcal")
    print("Distance:\t",data['routine'][0]['distance'],"km")
    print("Floors:\t\t",data['routine'][0]['floors'])

#declare iteration counters
x = 0

if user_activity == "fitness":
    while x < len(data['fitness']):
        for activity in data['fitness']:
            if activity['source'] == 'fitbit':
                print("\nFitness Activity: ", x + 1, "\n")
                print("Category:\t", activity['activity_category'])
                print("Source:\t\t", activity['source_name'])
                print("Avg HR:\t\t", activity['average_heart_rate'],"bpm")
                print("Calories:\t", activity['calories'],"kcal")
                print("Duration:\t", round((activity['duration'])/60, 2),"mins")
                print("Distance:\t", activity['distance'],"km\n")
                x += 1
                y = 0
                z = 0
                while y < len(activity['heart_rate_zones']):
                    print(" Heart Rate Zones ")
                    print("==================")
                    for hrz in activity['heart_rate_zones']:
                        print("Zone:\t", hrz['name'])
                        print("Mins:\t", hrz['minutes'],"mins\n")
                        y += 1
                while z < len(activity['activity_level']):
                    print("  Activity Level  ")
                    print("==================")
                    for level in activity['activity_level']:
                        print("Name:\t", level['name'])
                        print("Mins:\t", level['minutes'],"mins\n")
                        z += 1
            elif activity['source_name'] == 'Garmin Connect':
                print("\nFitness Activity: ", x + 1, "\n")
                print("Date/Time:\t", start_date, time.strftime('%H:%M:%S', time.gmtime(activity['start_time_in_seconds'])))
                print("Category:\t", activity['activity_category'])
                print("Source:\t\t", activity['source_name'])
                print("Avg HR:\t\t", activity['average_heart_rate_in_beats_per_minute'],"bpm")
                print("Max HR:\t\t", activity['max_heart_rate_in_beats_per_minute'], "bpm")
                print("Calories:\t", activity['calories'],"kcal")
                print("Steps:\t\t", activity['steps'])
                print("Duration:\t", round((activity['duration'])/60, 2),"mins")
                print("Distance:\t", (activity['distance'])/60,"km\n")
                x += 1