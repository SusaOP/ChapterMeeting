import yaml
import datetime
from Member import Member

# Class to organize meetings
class Meeting:

    def __init__(self, title="", date = "", start_time="", end_time="", members_attended = [], comments = {}):
        self.title = title
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.members_attended = members_attended
        if (comments == {}):
            self.comments = {name: [] for name in members_attended.split(",") if name != ''}
        else:
            self.comments = comments

    # Add a member to the meeting
    def add_member(self, member):
        self.members_attended.append(member)

    # Return a string for the members attended
    def getMembersAttended(self):
        members = ""
        for name in self.members_attended.split(','):
            members += (name + ",")
        
        return members
    
    # Add comment to meeting
    def add_comment(self, comment, member_name):
        print(member_name)
        print(comment)
        self.comments[member_name].append(comment)

    # Return a string for the comments
    def getAllComments(self):
        comments = ""
        for member in self.members_attended:
            comments += (member.name + ": ")
            for comment in self.comments[member.name]:
                comments += (comment + ",")
            comments += "\n"
        
        return comments

    # Get a string for the comments for a specific member
    def getComments(self, member):
        comments = ""
        for comment in self.comments[member.name]:
            comments += (comment + "\n\n")
        
        return comments

    # format comments for yaml file??
    def formatComments(self):
        comments = {}
        for member in self.members_attended:
            comments[member.name] = self.comments[member.name]
        
        return comments

    # Return string for meeting to add to yaml file
    def meeting_as_yaml(self):
        meet_str = "- Meeting:\n"
        meet_str += "    title: " + self.title + "\n"
        meet_str += "    date: " + str(self.date) + "\n"
        meet_str += "    start_time: " + str(self.start_time) + "\n"
        meet_str += "    end_time: " + str(self.end_time) + "\n"
        meet_str += "    members_attended: " + self.getMembersAttended() + "\n"
        meet_str += "    comments: " + str(self.comments) + "\n"
        return meet_str
    
    # Get duration of meeting
    def getDuration(self):
        start = datetime.datetime.strptime(self.start_time, '%H:%M:%S')
        end = datetime.datetime.strptime(self.end_time, '%H:%M:%S')
        duration = end - start
        return duration
    

    
