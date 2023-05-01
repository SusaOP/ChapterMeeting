# Chapter Meeting
An interface for keeping attendance and records for small organizational meetings.

Setup:
1. Initialize 2 ".yaml" files (see formatting below):
  attendance.yaml
  meetings.yaml (optional)

2. Usage: python3 Attendance.py


***Formatting examples:***

*attendance.yaml*
```
- Member:
    clock_in_time: 
    clocked_in: False
    dates_attended: []
    name: John Smith
- Member:
    clock_in_time: 
    clocked_in: False
    dates_attended: []
```
*meetings.yaml*
```
- Meeting:
    title: Example Title
    date: 04/30/2023
    start_time: 80715
    end_time: 80717
    members_attended: John Smith,Jane Doe,
    comments: {'John Smith': ['This is one comment','This is another comment'], 'Jane Doe': []}
```


