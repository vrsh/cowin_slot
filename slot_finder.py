'''
A vaccination slot alert system
Alerts for available slots in current week

Run this script on any system having python installed
to run execute: python cowin_dist_weekly.py
This will keep running unless you force quit and will 
try to fetch info every 5 minute (default)
frequency can be changed. Read below to know how.

INPUT: 
distrct_id: district id for your district (default 294 for bengaluru bbmp)
age_group: 18 for 18+ and 45 for 45+ (default 18)
dose: 1 for dose1 and 2 for dose2 (default 1)
centers: names of centers of your choice. (default centers=['All'] for all centers). 
for selecting nearby centers remove 'All' from centers list and add the selected
centers to the centers list as show in the code.
update_time: update time in minutes (default 15 seconds/ 0.25 minutes)

OUTPUT: 
Case 1: when a slot is not available: 
nothing (99.99% time for 18+, thanks to our planning and execution system)

Case 2: when a slot for dose is available for your age group: 
a beep sound to alert with details of date of availability, 
center name, its address, available slots and fee type
same info is stored in cowin_slots.csv file

Author: Ritesh Sharma
'''

import requests
import datetime
import json
import time

# find your district id in district_ids.csv file
district_id = 294

# 18 or 45
age_group = 18

# 1 or 2
dose = 1

# All or selcted
# centers = ['AGARA GOVT SCHOOL', 'AGARA UPHC C1', 'APOLLO CLINIC HSR', 
#             'APOLLO CRADLE - Koramangala', 'APOLLO SPECTRA HOSPITAL -1', 
#             'Columbia Asia Sarjapur P3', 'Doddakannalli UPHC COVAXIN', 
#             'Fortis Hospital BG ROAD P3', 'Fortis Lafemme BLOCK 1', 
#             'HSR CLUB', 'Koramangala UPHC', 'St Johns Hospital', 
#             'CLOUDNINE BELLANDUR P3']
centers = ['All']

# in minutes
update_time = 0.25

slots = open('cowin_slots.csv', 'w')
slots.write('Alert Time,Date,Center,Address,Availability,Fee Type\n')

try:
    while True:
        # date = (datetime.date.today()+datetime.timedelta(1)).strftime("%d-%m-%Y")
        date = datetime.date.today().strftime("%d-%m-%Y")
        URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}"
        response = requests.get(URL)
    
        if response.ok:
            resp_json = response.json()
            if resp_json["centers"]:
                for center in resp_json["centers"]:
                    if (centers[0]=='All') or (center["name"] in centers):
                        for session in center["sessions"]:
                            if session["min_age_limit"] == age_group:
                                if session[f"available_capacity_dose{dose}"] > 0:
                                    print('\n~~~~~~~~~~~~~~~~~\n')
                                    print(f'Alert Time: {datetime.datetime.now()}')
                                    print(f'Date: {session["date"]}')
                                    print(f'Center: {center["name"]}')
                                    print(f'Address: {center["address"]}')
                                    print(f'Availability: {session[f"available_capacity_dose{dose}"]}')
                                    print(f'Fee Type: {center["fee_type"]}')
                                    print('\a')
                                    slots.write(f'{datetime.datetime.now()},{session["date"]},{center["name"]},{center["address"]},{session[f"available_capacity_dose{dose}"]},{center["fee_type"]}\n')
        # print('\nSearch Complete')
        slots.write('---,---,---,---,---,---\n')
        time.sleep(update_time*60)
except KeyboardInterrupt:
    print("\ninterrupted by USER")
except:
    print('\nsome exception')
finally:
    print("\nSearch Halted")
    print("Output saved to slots.csv")

