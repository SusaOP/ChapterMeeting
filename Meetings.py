from Meeting import Meeting
from Member import Member
import datetime
import yaml
import tkinter as tk

class Meetings:
    def __init__(self, meetings = []):
        self.meetings = meetings

    # loaded meetings from yaml file
    def loadMeetings(self, filename):
        with open(filename, 'r') as file:
            meetings = yaml.load(file, Loader=yaml.FullLoader)
            #print(meetings)
            self.meetings = []
            if (meetings == None):
                return
            for meeting in meetings:
                #print(meeting)
                self.meetings.append(Meeting(meeting['Meeting']['title'], meeting['Meeting']['date'],
                        meeting['Meeting']['start_time'], meeting['Meeting']['end_time'], 
                        meeting['Meeting']['members_attended'], meeting['Meeting']['comments']))
        print(f'Successfully loaded {len(self.meetings)} meetings from {filename}.')

    # add a meeting to the list
    def addMeeting(self, meeting):
        self.meetings.append(meeting)

    # return a list of meetings attended by a member
    def getMeetingsAttended(self, member):
        meetings_attended = []
        for meeting in self.meetings:
            if member in meeting.members_attended:
                meetings_attended.append(meeting)
        
        return meetings_attended
    
    # save meetings to yaml file
    def saveMeetings(self, filename):
        with open(filename, 'w') as file:
            for meeting in self.meetings:
                file.write(meeting.meeting_as_yaml())

    def displayMeetings(self, root):
        for meeting in self.meetings:
            print(meeting)

    def getMeeting(self, title):
        for meeting in self.meetings:
            if meeting.title == title:
                return meeting
        return None

