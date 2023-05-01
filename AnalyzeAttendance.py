import tkinter as tk
import datetime

from Member import Member

# Return a list of strings for each member and their attendance
def getMeetingsAttended(members):
    all_member_attendance = []
    for member in members:
        # attendance format: ['Name', [meetings_attended]]
        # meetings_attended[i] = ['date', 'clock in time', 'clock out time', duration]
        # 
        member_attendance = []
        member_attendance.append(member.name+":")
        meetings_attended = []

        total_meeting_time = 0.0

        if len(member.dates_attended) == 0:
            member_attendance.append(meetings_attended)
            all_member_attendance.append(member_attendance)
            continue

        for meeting_info in member.dates_attended:
            meeting = []
            split_info = meeting_info.split(',')

            #['date', 'clock in time', 'clock out time', duration]
            meeting.append(split_info[0]+':')
            meeting.append(str('Clock in: '+split_info[1]+ '\n Clock out: '+ split_info[2]))
            timeattended = datetime.datetime.strptime(split_info[2], '%H:%M:%S') - datetime.datetime.strptime(split_info[1], '%H:%M:%S')
            meeting.append(f'Meeting Duration: {timeattended}')

            total_meeting_time += timeattended.total_seconds()

            meetings_attended.append(meeting)
            
        member_attendance.append(meetings_attended)
        member_attendance.append(f'Overall Time: \n{datetime.timedelta(seconds=total_meeting_time)}')

        all_member_attendance.append(member_attendance)

    return all_member_attendance

def getMemberAttendance(member):
    member_attendance = []
    member_attendance.append(member.name+":")
    meetings_attended = []

    if len(member.dates_attended) == 0:
        member_attendance.append(meetings_attended)
        return member_attendance

    for meeting_info in member.dates_attended:
        meeting = []
        split_info = meeting_info.split(',')

        #['date', 'clock in time', 'clock out time', duration]
        meeting.append(split_info[0]+':')
        meeting.append(str('Clock in: '+split_info[1]+ ', Clock out: '+ split_info[2]))
        timeattended = datetime.datetime.strptime(split_info[2], '%H:%M:%S') - datetime.datetime.strptime(split_info[1], '%H:%M:%S')
        meeting.append(f'Total Time at meeting: {timeattended}')
        print(meeting)
        meetings_attended.append(meeting)
        
    member_attendance.append(meetings_attended)

    return member_attendance

# Create a new window that displays all the members and their attendance    
def showMembersAttendance(members, rootwindow):
    # Create a new window
    attendance_window = tk.Toplevel(rootwindow)
    attendance_window.title('Attendance')
    attendance_window.geometry('800x600')
    attendance_window.configure(bg='white')

    # Create a label for each member and their attendance
    member_attendance = getMeetingsAttended(members)

    print(member_attendance)

    for i in range(len(member_attendance)):

        if len(member_attendance[i][1]) == 0:
            tk.Label(attendance_window, text=member_attendance[i][0], borderwidth=1, relief='solid', highlightthickness=1).grid(row=i, column=0, sticky='w')
            tk.Label(attendance_window, text='No meetings attended', borderwidth=1, relief='solid', highlightthickness=1).grid(row=i, column=1, sticky='w')
            continue

        tk.Label(attendance_window, text=member_attendance[i][0], borderwidth=1, relief='solid', highlightthickness=1).grid(row=i, column=0, sticky='w')
        for j in range(len(member_attendance[i][1])):
            fixed_meeting = '\n'.join(member_attendance[i][1][j])
            tk.Label(attendance_window, text=fixed_meeting, borderwidth=1, relief='solid', highlightthickness=1).grid(row=i, column=j+1, sticky='w')

        # Add a label for the total time at meetings
        tk.Label(attendance_window, text=member_attendance[i][2], borderwidth=1, relief='solid', highlightthickness=1).grid(row=i, column=len(member_attendance[i][1])+1, sticky='w')

    # Create a button to close the window
    tk.Button(attendance_window, text='Close', command=attendance_window.destroy).grid(row=len(member_attendance), column=0, sticky='w')
