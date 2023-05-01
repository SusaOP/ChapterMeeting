# Member class
import datetime
import yaml

class Member:

    def __init__(self, name = "", dates_attended = []):
        self.name = name
        self.clocked_in = False
        self.clock_in_time = ""
        self.dates_attended = dates_attended

    # Define functions to clock in and clock out members. Note the date and time
    def clock_in(self):
        if (self.clocked_in):
            return
        
        # Get the current date and time
        now = datetime.datetime.now()
        date = now.strftime('%m/%d/%Y')
        time = now.strftime('%H:%M:%S')
        self.clock_in_time = time
        self.clocked_in = True
        print(f'{self.name} clocked in at {time} on {date}')

    def clock_out(self):

        # Get the current date and time
        now = datetime.datetime.now()
        date = now.strftime('%m/%d/%Y')
        co_time = now.strftime('%H:%M:%S')

        self.dates_attended.append(f'{date},{self.clock_in_time},{co_time}')
        self.clock_in_time = ""
        self.clocked_in = False
        print(f'{self.name} clocked out. Period was {self.dates_attended[-1]}')

    # Return a string for the dates and times attended
    def getDatesTimesAttendance(self):
        attendance = ""
        for date in self.dates_attended:
            split_date = date.split(',')
            attendance += (f'{split_date[0]},{split_date[1]},{split_date[2]}')
        
        return attendance
    
    # Clear attendance for member
    def clear_attendance(self):
        self.dates_attended = []
        print(f'Attendance for {self.name} cleared. ')


    # Return string for member to add to yaml file
    
    def member_as_yaml(self):
        mem_str = "- Member:\n"
        mem_str += "    clock_in_time: " + self.clock_in_time + "\n"
        mem_str += "    clocked_in: " + str(self.clocked_in) + "\n"
        mem_str += "    dates_attended: " + str(self.dates_attended) + "\n"
        mem_str += "    name: " + self.name + "\n"

        return mem_str

