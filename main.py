from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

# ---------------------- CONSTANTS ---------------------------------#

BG_COLOR = '#34495E'
is_true = False
max_count = 0

class NavProgressbar(object):
    def __init__(self, canvas, x0, y0, x1, y1, width, start_ang=0):
        global is_true
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.width = width
        self.start_line, self.full_extent = start_ang, int(self.canvas["width"])
        w2 = width/2

        self.line = self.canvas.create_line(0, 10, int(self.canvas['width']), 10, fill="black")
        self.running = False
        self.after_id = None

    def start(self, interval):
        self.interval = interval+100
        self.increament = self.full_extent/interval
        self.extent = 0
        start_angle = 0  # Starting angle of the arc
        extent_angle = 0  # Angle in degrees (0 to 360)
        self.arc_id = self.canvas.create_arc(0, 10, int(canvas['width']), 10, start=start_angle, extent=extent_angle, outline='blue', width=10, style=tk.ARC)

        self.running = True
        self.after_id = self.canvas.after(interval, self.step, self.increament)

    def step(self, delta):
        if self.running:
            self.extent = (self.extent + delta) % int(self.canvas['width'])
            if self.extent == 187.5:
                self.stop()
                back_button = Button(text="Go Back", font=("Comic sans MS", 20, "bold"), command=refresh)
                back_button.config(padx=20, pady=20)
                back_button.place(x=180, y=600)
                event_handler.keypressed = True
                answer = messagebox.askretrycancel("Question", "Do you want to try that again?")
                if answer == True:
                    start_timer()
                else:
                    refresh()

            self.canvas.itemconfigure(self.arc_id, extent=self.extent)

            self.after_id = self.canvas.after(1000, self.step, delta)

    def stop(self):
        self.running = False
        self.extent = 0
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None

    def refresh_me(self):
        self.extent = 0

    def toggle_pause(self):
        self.running = not self.running



class CircularProgressbar(object):
    def __init__(self, canvas, x0, y0, x1, y1, width=2, start_ang=0, full_extent=360.):
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1-x0) / 2, (y1-y0) / 2
        self.width = width
        self.start_ang, self.full_extent =  start_ang, full_extent
        # draw static bar outline
        w2 = width / 2
        self.oval_id2 = self.canvas.create_oval(self.x0, self.y0,
                                                self.x1-w2, self.y1-w2, fill="white", outline="white")
        self.running = False
        self.after_id = None

    def start(self, interval=60):
        self.interval = interval  # Msec delay between updates.
        self.increment = self.full_extent / interval
        self.extent = 0
        self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                             start=self.full_extent, extent=self.extent,
                                             width=self.width, style='arc')

        self.running = True
        self.my_id = self.canvas.after(interval, self.step, self.increment)

    def step(self, delta):
        """Increment extent and update arc and label displaying how much completed."""
        if not event_handler.keypressed:
            if self.running:
                self.extent = (self.extent + delta) % 360
                print(delta)

                if self.extent == 354:
                    self.stop()
                    back_button = Button(text="Go Back", font=("Comic sans MS", 20, "bold"), command=refresh)
                    back_button.config(padx=20, pady=20)
                    back_button.place(x=180, y=600)
                    if 'navprogress' in globals():
                        navprogress.stop()
                    if 'timer_label' in globals():
                        timer_label.grid_remove()

                self.canvas.itemconfigure(self.arc_id, extent=self.extent)
                self.after_id = self.canvas.after(self.interval, self.step, delta)

    def stop(self):
        self.running = False
        self.extent = 0
        if self.after_id:
            print("I am triggered")
            self.canvas.after_cancel(self.after_id)
            self.canvas.after_cancel(self.my_id)
            self.after_id = None


    def toggle_pause(self):
        self.running = not self.running

    def change_fill(self, color):
        self.canvas.itemconfigure(self.oval_id2, fill= color)

    def remove(self):
        if 'one_more' in globals():
            one_more.grid_remove()
        self.stop()
        self.canvas.delete(self.arc_id)
        self.canvas.delete(self.oval_id2)


def space_press(event):
    if event.char == " ":
        my_count = 0
        event_handler.keypressed = False
        check_key_press(my_count)

def check_key_press(my_count):
    global after_count
    if my_count < 7:
        after_count = windows.after(900, lambda: check_key(my_count))

def check_key(my_count):
    global progressbar, timer_label, one_more
    if my_count < 7:
        if not event_handler.keypressed:

            if my_count == 2:
                make_canvas()
                if 'progressbar' in globals():
                    progressbar.start()
            if my_count >= 2:
                timer_label = Label(text=f"{7 - my_count}", font=("Comic sans ms", 14, "bold"), bg="white")
                timer_label.place(x=250, y=630)

            if my_count == 6:
                answer = messagebox.askretrycancel("Question", "Do you want to try that again?")
                if answer == True:
                    start_timer()
                else:
                    misminute(0)
                    refresh()
            my_count += 1
            check_key_press(my_count)

        else:

            if 'timer_label' in globals():
                timer_label.grid_remove()

            if 'after_count' in globals():
                windows.after_cancel(after_count)

            another_count = 0
            check_key_press(another_count)
            one_more = Canvas(width=180, height=110, bg="white", highlightthickness=0)
            one_more.place(x=180, y=600)
            if is_true:
                one_more.grid_remove()
            if 'progressbar' in globals():
                progressbar.remove()


def make_canvas():
    global progressbar
    my_canvas = Canvas(windows, width=100, height=100, bg='white', highlightthickness=0)
    my_canvas.place(x=210, y=600)
    progressbar = CircularProgressbar(my_canvas, 0, 0, 100, 100, 10)

def refresh():
    canvas = Canvas(width=500, height=800, bg=BG_COLOR, highlightthickness=0)
    canvas.grid(column=1, row=1, columnspan=5, rowspan=4)

    start_button = Button(text="HardCore Typing", font=("Comic sans MS", 20, "bold"), command=start_timer)
    start_button.config(padx=10, pady=10)
    start_button.grid(column=3, row=2)
    warning_label = Label(text="Stop and all your progress will be gone!", font=("Comic sans ms", 14, "bold"))
    warning_label.place(x=60, y=125)
    exit_button = Button(text="Exit", font=("Comic, sans MS", 20, "bold"), command=exit_me)
    exit_button.config(padx=10, pady=10)
    exit_button.grid(column=3, row=3)

def misminute(count):
    global max_count
    if count > max_count:
        max_count = count + 100

    if count == 0:
        navprogress.stop()
        return
    navprogress.start(interval=max_count)
    windows.after(1000, misminute, count - 1)

def start_timer():
    global my_entry, timer_label, navprogress, my_canvas
    start_button.grid_remove()
    my_entry = Text(windows, width=39, height=40, font=("Comic sans MS", 14, "bold"))
    my_entry.place(x=0, y=0)
    my_entry.config(padx=20, pady=30)
    my_entry.insert("1.0", "Start typing from here")
    my_entry.bind("<FocusIn>", func=lambda event: my_entry.delete("1.0", "end"))
    my_entry.bind("<FocusOut>", func=lambda event: my_entry.insert("1.0", "Start typing from here") if my_entry.get("1.0", "end") == "" else None)

    another_canvas = Canvas(windows, width=int(canvas['width']), height=30, bg="white", highlightthickness=0)
    another_canvas.place(x=0, y=0)
    if 'navprogress' in globals():
        navprogress.stop()
    navprogress = NavProgressbar(another_canvas, 100, 100, int(canvas["width"]) + 100, int(canvas["width"]) + 10, 10)
    misminute(60)



def on_any_key(event):
    event_handler.keypressed = True

class EventHandler:
    keypressed = False


def exit_me():
    windows.quit()

windows = Tk()
windows.title("Disappearing_text")

event_handler = EventHandler()
windows.bind_all("<Key>", on_any_key)
windows.bind_all("<space>", space_press)

canvas = Canvas(width= 500, height=800, bg=BG_COLOR, highlightthickness=0)
canvas.grid(column=1, row=1, columnspan=5, rowspan=4)


start_button = Button(text="HardCore Typing", font=("Comic sans MS", 20, "bold"), command=start_timer)
start_button.config(padx=10, pady=10)
start_button.grid(column=3, row=2)


warning_label = Label(text="Stop and all your progress will be gone!", font=("Comic sans ms", 14, "bold"))
warning_label.place(x=60, y=125)

exit_button = Button(text="Exit", font=("Comic, sans MS", 20, "bold"), command=exit_me)
exit_button.config(padx=10, pady=10)
exit_button.grid(column=3, row=3)

windows.mainloop()


