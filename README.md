# Cowin Vaccination Slot ALert Script
Ultra light Python script for cowin alerts for available slots in current week.

Run this script on any system having python installed.
To run execute: 

```bash
python slot_finder.py
```

This will keep running unless you force quit and will try to fetch info every 15 seconds (default). Frequency can be changed. Read below to know how.

## INPUT: 
**distrct_id:** district id for your district (default 294 for bengaluru bbmp). Find your district's ID in district_ids.csv file. Districts are sorted statewise and states are sorted alphabetically in this file.

**age_group:** 18 for 18+ and 45 for 45+ (default 18)

**dose:** 1 for dose1 and 2 for dose2 (default 1)

**centers:** names of centers of your choice, comment selected centers and uncomment ```centers=['All']``` (line 49) for selecting all centers in the district

**update_time:** update time in minutes (default 15 seconds)

## OUTPUT: 
**Case 1:** *when a slot is not available:* 
nothing (99.99% time for 18+, facepalm)

**Case 2:** *when a slot for selected dose is available for your age group:* 
a beep sound to alert with details of date of availability, 
center name, its address, available slots and fee type
same info is stored in cowin_slots.csv file

*To stop the script interrupt by pressing Ctrl+c*

## Trick: 
Most hospitals in BBMP open slots after 4.30PM
