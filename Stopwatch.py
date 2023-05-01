import time
import tkinter as tk

class Stopwatch:

    def __init__(self):
        self.start_time = 0.00
        self.stop_time = 0.00
        self.running = False
        self.window = None
        self.buttons = []

    def start(self):
        if (self.running):
            return
        self.start_time = time.time()
        self.running = True

    def stop(self):
        if (not self.running):
            return
        self.stop_time = time.time()
        self.running = False

    def reset(self):
        self.start_time = 0.00
        self.stop_time = 0.00
        self.running = False

    def display(self):
        if (self.running):
            return self.format_time(time.time() - self.start_time)
        else:
            return self.format_time(self.stop_time - self.start_time)
        
    def format_time(self, time):
        hours = int(time / 3600)
        time = time - (hours * 3600)
        minutes = int(time / 60)
        time = time - (minutes * 60)
        seconds = int(time)
        time = time - seconds
        hundredths = int(time * 100)
        return f'{hours:02}:{minutes:02}:{seconds:02}.{hundredths:02}'
    
    def get_time(self):
        return time.time() - self.start_time
    
    def get_time_as_string(self):
        return self.format_time(time.time() - self.start_time)
    
    # build a tkinter window attached to the root window to display the stopwatch
    def display_stopwatch(self, rootwindow):

        # get dimensions of the root window
        rw_dimensions = rootwindow.winfo_geometry()
        rw_x = int(rw_dimensions.split('x')[0])
        rw_y = int(rw_dimensions.split('x')[1].split('+')[0])

        # Create a label to display the stopwatch
        stopwatch = tk.Label(rootwindow, text='00:00:00', font=('Helvetica', 20))
        stopwatch.place(x=int(0.626*rw_x), y=int(0.32*rw_y))
        
        # Create buttons with fixed sizes to start, stop, and reset the stopwatch 

        # Start button
        start_button = tk.Button(rootwindow, text='Start', width=6, height=1, command=lambda: self.start())
        start_button['bg'] = 'green'
        start_button.place(x=int(0.56*rw_x), y=int(0.4*rw_y))
        self.buttons.append(start_button)

        # Stop button lined up with the middle of the stopwatch button
        stop_button = tk.Button(rootwindow, text='Stop', width=6, height=1, command=lambda: self.stop())
        stop_button.place(x=int(0.66*rw_x), y=int(0.4*rw_y))
        stop_button['bg'] = 'red'
        self.buttons.append(stop_button)

        # Reset button
        reset_button = tk.Button(rootwindow, text='Reset', width=6, height=1, command=lambda: self.reset())
        reset_button.place(x=int(0.76*rw_x), y=int(0.4*rw_y))
        reset_button['bg'] = 'yellow'
        self.buttons.append(reset_button)

        # Update the stopwatch display every 10 milliseconds
        def update_stopwatch():
            stopwatch.config(text=self.display())
            stopwatch.after(10, update_stopwatch)
        
        update_stopwatch()
        
        # Return the stopwatch object
        self.window = stopwatch
        return stopwatch

    # Hide buttons and destroy the stopwatch window
    def destroy_stopwatch(self):
        for button in self.buttons:
            button.place_forget()
        self.window.destroy()
        self.window = None
        self.buttons = []
        return

