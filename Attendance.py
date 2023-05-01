# Module interface to take chapter meeting attendance
import tkinter as tk
from tkinter import messagebox
import datetime
import yaml

from Member import Member
from AnalyzeAttendance import *
from Stopwatch import *
from Meeting import *
from Meetings import *


global r

# Initialize all the members as objects

# Create a GUI interface using tkinter
root = tk.Tk()

root.title('Attendance')
root.geometry('1000x800')

# window dimensions
dimensions = [1000, 800]

# boolean to see if all data have saved to file yet
saved = False
# displays boolean dictionary (what displays are being shown)
booleans = {'saved': False, 'stopwatch': False, 'meeting_started': False}

global thisMeeting

# clock out all and get final yaml
def clock_out_all(members):
    final_yaml = ""
    for member in members:
        if member.clocked_in:
            member.clock_out()
        final_yaml += member.member_as_yaml()
    
    # Write all member objects to yaml
    with open('attendance.yaml', 'w') as f:
        f.write(final_yaml)
        booleans['saved'] = True
        saved = True

# load in yaml file to member objects
def load_yaml():
    with open('attendance.yaml', 'r') as f:
        #yaml_data = f.read()
        members = yaml.safe_load(f)
    return members

# save member data to yaml file
def save_yaml():

    final_yaml = ""
    for member in members:
        final_yaml += member.member_as_yaml()

    with open('attendance.yaml', 'w') as f:
        f.write(final_yaml)
        booleans['saved'] = True
        saved = True


members = [] # "members" for Member objects
members_ = load_yaml() # "members_" for loaded yaml

for member_ in members_:
    members.append(Member(name=member_['Member']['name'], dates_attended=member_['Member']['dates_attended']))

# Change color of button when clicked
def button_pressed(event):
    event.widget.config(bg='yellow')
    

# Change color of all passed buttons based on whether or not member is clocked in
def highlight_all_clocked_in(buttons, mems):
    if (len(buttons) != len(mems)):
        print(f'Mismatched button-member ratio: {len(buttons)} buttons to {len(mems)} members.')
        return

    # highlight all buttons for members that never clocked_in as red (others as green)
    for i in range(len(buttons)):
        if (mems[i].clocked_in):
            buttons[i].config(bg='green')
        else:
            buttons[i].config(bg='red')


# Create button for each member, as well as 2 buttons to the right of each member name button for clock in and clock out for each member

name_buttons = []
r = 0
for member in members:
    print(f'Created button for {member.name}')

    # Button to the left to display member name
    name_b = tk.Button(root, text=member.name, command=lambda m=member: add_comment(m.name), width=15,height=1)
    name_b.grid(row=r, column=0)
    name_b.bind('<Button-1>', button_pressed)
    name_buttons.append(name_b)
    # Create button to the right of the first button to clock in member
    clock_in_b = tk.Button(root, text='Clock In', command=lambda m=member: m.clock_in()).grid(row=r, column=1)

    # Create button to the right of the second button to clock out member
    clock_out_b = tk.Button(root, text='Clock Out', command=lambda m=member: m.clock_out()).grid(row=r, column=2)
    r+=1

# Create button to clock out all present members
tk.Button(root, text='Clock Out All', command=lambda: (highlight_all_clocked_in(name_buttons, members), clock_out_all(members))).place(x=30, y=750)


# Create button to trigger a pop-up warning screen with yes and no options
tk.Button(root, text='Clear All Attendance', command=lambda: clear_all_attendance(members)).place(x=800, y=750)


# Create a button to open a new window and input a new member
#tk.Button(root, text='Add New Member', command=lambda: add_member()).grid(row=r, column=3, sticky='s'+'ew')
tk.Button(root, text='Add New Member', command=lambda: add_member()).place(x=300, y=750)

# function to open a popup window that prompts user for input into a textbox and click a "Submit" button
def add_member():
    # Create a new window
    new_window = tk.Toplevel(root)
    new_window.title('Add New Member')
    new_window.geometry('400x300')

    def submit_new_member(name, window):
        global r
        new_member = Member(name=name)
        members.append(new_member)
        print(f'Added new member: {new_member.name}')

        name_b = tk.Button(root, text=new_member.name, command=lambda m=new_member: print(m.name), width=15,height=1)
        name_b.grid(row=r, column=0)
        name_b.bind('<Button-1>', button_pressed)
        name_buttons.append(name_b)

        # Create button to the right of the first button to clock in member
        clock_in_b = tk.Button(root, text='Clock In', command=lambda m=new_member: m.clock_in()).grid(row=r, column=1)

        # Create button to the right of the second button to clock out member
        clock_out_b = tk.Button(root, text='Clock Out', command=lambda m=new_member: m.clock_out()).grid(row=r, column=2)

        r+=1
        window.destroy()

    # Create a label to display instructions
    tk.Label(new_window, text='Enter the name of the new member below:').grid(row=0, column=0)

    # Create a textbox to enter the name of the new member
    new_member_name = tk.Entry(new_window, width=50)
    new_member_name.grid(row=1, column=0)

    # Create a button to submit the new member name
    tk.Button(new_window, text='Submit', command=lambda: submit_new_member(new_member_name.get(), new_window)).grid(row=2, column=0)


# Run a function based on the presvious askyesno() function
def clear_all_attendance(mems):
    if tk.messagebox.askyesno('Warning', 'Are you sure you want to clear all members attendance logs?'):
        if (saved or booleans['saved']):
            mems = load_yaml()

        for mem in mems:
            mem.clear_attendance()
            #print(f'Cleared attendance for {member.name}')
        print('Cleared all attendance')
        save_yaml()


# Button to show attendance for every member
tk.Button(root, text='Show Attendance', command=lambda: showMembersAttendance(members, root)).place(x=150, y=750)

# --------------------------------------------------------------------------------
# Time Visual Display

# Put a display box on the unoccupied right side of the screen to show the current time
time_display = tk.Label(root, text=datetime.datetime.now().strftime('%H:%M:%S'), font=('Helvetica', 20))
time_display.place(x=650, y=0)

# Update the time display every second
def update_time():
    time_display.config(text=datetime.datetime.now().strftime('%H:%M:%S'))
    time_display.after(1000, update_time)

update_time()

# Open a new window to display the stopwatch
def stopwatch_window():

    # if the stopwatch window is already open, close it and hide its buttons
    if (booleans['stopwatch']):
        destroy_stopwatch_window()
        booleans['stopwatch'] = False
        return

    # Create a stopwatch object
    global stopwatch
    stopwatch = Stopwatch()

    # Create a new window from the stopwatch
    stopwatch.display_stopwatch(root)
    booleans['stopwatch'] = True

# Destroy the stopwatch window
def destroy_stopwatch_window():
    booleans['stopwatch'] = False
    stopwatch.destroy_stopwatch()

# Create a button to open stopwatch window
stopwatch_b = tk.Button(root, text='Stopwatch', command=lambda: stopwatch_window()).place(x=650, y=200)
# --------------------------------------------------------------------------------
# Create a window to view previous meetings
meetings = Meetings()
meetings.loadMeetings('meetings.yaml')

def initializeMeetingWindow():
    #meetings.loadMeetings('meetings.yaml')

    # Create a new tkinter window to display the meetings
    meeting_window = tk.Toplevel(root)
    meeting_window.title('Meetings')
    meeting_window.geometry('400x300')

    # Create a label to display instructions
    tk.Label(meeting_window, text='Select a meeting to view:').grid(row=0, column=0)

    # Create a listbox to display the meetings
    meeting_listbox = tk.Listbox(meeting_window, width=50)
    meeting_listbox.grid(row=1, column=0)

    # Create a button to view the selected meeting
    tk.Button(meeting_window, text='View Meeting', command=lambda: viewMeeting(meeting_listbox.get(tk.ACTIVE), meeting_window)).grid(row=2, column=0)

    # Create a button to delete the selected meeting
    #tk.Button(meeting_window, text='Delete Meeting', command=lambda: deleteMeeting(meeting_listbox.get(tk.ACTIVE), meeting_window)).grid(row=3, column=0)

    # Create a button to close the window
    tk.Button(meeting_window, text='Close', command=lambda: meeting_window.destroy()).grid(row=4, column=0)

    # Populate the listbox with the meetings
    for meeting in meetings.meetings:
        meeting_listbox.insert(tk.END, meeting.title)

# View the selected meeting
def viewMeeting(meeting_name, window):
    # Create a new window to display the meeting
    meeting_window = tk.Toplevel(root)
    meeting_window.title(meeting_name)
    meeting_window.geometry('600x300')

    # Create a label to display instructions
    tk.Label(meeting_window, text='Members in Attendance:').grid(row=0, column=0)

    # Create a frame to hold the listbox 
    member_frame = tk.Frame(meeting_window)
    member_frame.grid(row=0, column=0)

    # Create a new frame to display the comments
    comment_frame = tk.Frame(meeting_window)
    comment_frame.grid(row=0, column=1)


    # Create a listbox to display the members in the left "memberframe"
    member_listbox = tk.Listbox(member_frame, width=20)
    member_listbox.grid(row=0, column=0)

    # create a scrollbar and attach it to the frame
    scrollbar = tk.Scrollbar(comment_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a display for the comments in the right "commentframe"
    comment_display = tk.Text(comment_frame, width=40, height=10, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    comment_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)   

    scrollbar.config(command=comment_display.yview)

    # Create a button to close the window
    tk.Button(meeting_window, text='Close', command=lambda: meeting_window.destroy()).grid(row=3, column=0)

    # Populate the listbox with the members
    for name in meetings.getMeeting(meeting_name).members_attended.split(','):
        if (name == ''): continue
        member_listbox.insert(tk.END, name)

    # View comments for a selected member and put it on the right side of the screen
    def viewComments(member_name):
        if (len(meetings.getMeeting(meeting_name).comments[member_name]) == 0):
            comment_display.delete("1.0", tk.END)
            comment_display.insert(tk.END, 'No Comments.\n')
            return
        # Display comments in the frame
        for comment in meetings.getMeeting(meeting_name).comments[member_name]:
            #textbox = tk.Text(comment_f).pack()
            print(comment)
            comment_display.delete("1.0", tk.END)
            if (comment == ''): 
                continue
            comment_display.insert(tk.END, comment)


    # Create a button to view the comments for the selected member
    
    tk.Button(meeting_window, text='View Comments', command=lambda: viewComments(member_listbox.get(tk.ACTIVE))).grid(row=2, column=0)


# Create a textbox to input the name of the meeting
meeting_name = tk.Entry(root, width=32)
meeting_name.place(x=50, y=450)

# Create a button to create a new meeting
startMeeting_b = tk.Button(root, text='New Meeting', command=lambda: create_new_meeting(), bg="green")
startMeeting_b.place(x=50, y=500)

# Create a button to end the meeting
endMeeting_b = tk.Button(root, text='End Meeting', command=lambda: end_meeting())
default_color = endMeeting_b.cget('bg')
endMeeting_b.place(x=200, y=500)

# Add comment
def add_comment(commentor):
    # open a window to input a comment
    comment_window = tk.Toplevel(root)
    comment_window.title('Add Comment')
    comment_window.geometry('400x300')

    # Create a label to display instructions
    tk.Label(comment_window, text='Enter a comment:').grid(row=0, column=0)

    # Create a textbox to input the comment
    comment = tk.Text(comment_window, width=32, height=10)
    comment.grid(row=1, column=0)

    # Create a button to add the comment
    tk.Button(comment_window, text='Add Comment', command=lambda: add_comment_to_meeting(comment.get("1.0", "end"), commentor, comment_window)).grid(row=2, column=0)

    # Create a button to close the window
    tk.Button(comment_window, text='Close', command=lambda: comment_window.destroy()).grid(row=3, column=0)

def add_comment_to_meeting(comment, commentor, window):
    global thisMeeting
    print("Adding comment: " + comment + " to " + commentor)
    thisMeeting.add_comment(comment, commentor)
    thisMeeting.comments[commentor].append(comment)
    print(thisMeeting.comments[commentor])

    # Close the window
    window.destroy()



#


# Create a button to open the meetings window
tk.Button(root, text='Meetings', command=lambda: initializeMeetingWindow()).place(x=550, y=750)

# Create a new meeting
def create_new_meeting():
    global thisMeeting
    input_meeting = meeting_name.get()
    print("Creating new meeting: " + input_meeting)

    if (input_meeting == ''):
        return

    if (booleans['meeting_started']):
        return
    
    attendees = ""
    for member in members:
        if member.clocked_in:
            attendees += member.name + ','

    thisMeeting = Meeting(title=input_meeting, members_attended=attendees, date=datetime.datetime.now().strftime('%m/%d/%Y'),
         start_time=datetime.datetime.now().strftime('%H:%M:%S'), end_time=datetime.datetime.now().strftime('%H:%M:%S'), comments={})
    booleans['meeting_started'] = True
    #startMeeting_b.config(bg='SystemButtonFace')
    startMeeting_b['bg']=default_color
    endMeeting_b.config(bg='red')


# End the meeting
def end_meeting():
    global thisMeeting
    global booleans

    if (booleans['meeting_started'] == False):
        return
    
    thisMeeting.end_time = datetime.datetime.now().strftime('%H:%M:%S')
    for member in members:

        if (member.clocked_in and thisMeeting.comments[member.name] == []):
            print(member.name + " did not have any comments")
            thisMeeting.comments[member.name] = []

    meetings.addMeeting(thisMeeting)
    print("Ending meeting: " + thisMeeting.title)
    print("Members in attendance: " + thisMeeting.members_attended)
    meetings.saveMeetings('meetings.yaml')
    booleans['meeting_started'] = False

    startMeeting_b.config(bg='green')
    endMeeting_b.config(bg=default_color)



# --------------------------------------------------------------------------------

# Run the GUI
root.mainloop()


