from tkinter import *
import math
import pygame

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
count_paused = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)    
    canvas.itemconfig(timer_text, text="00:00")
    start_button.config(text="Start", command=start_timer)
    title_label.config(text="Timer")
    tick_label.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER PAUSE --------------------------------#
def pause_timer():
    window.after_cancel(timer)
    start_button.config(text="Resume", command=resume_timer)
    
    
# --------------------------- TIMER RESUME ----------------------------#
def resume_timer():
    global count_paused
    start_button.config(text="Pause", command=pause_timer)
    count_down(count_paused)
    
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    start_button.config(text="Pause", command=pause_timer)
    
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    
    
    # Long break
    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    # Short break
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    # Work
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
        global count_paused
        count_paused = count
    else:
        play_notification()
        start_timer()
        tick_count = ""
        work_sessions = math.floor(reps/2)
        for ticks in range(work_sessions):
            tick_count += "✔"
        tick_label.config(text=tick_count)
    

# ---------------------------- SOUND -----------------------------------#
def play_notification():
    
    pygame.mixer.init()
    pygame.mixer.music.load("notification.mp3")
    pygame.mixer.music.play()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


# Tomato background image with timer
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 28, "bold"))
canvas.grid(column=1, row=1)


# Timer title
title_label = Label(text="Timer", font=(FONT_NAME, 32, "bold"), bg=YELLOW, fg=GREEN)
title_label.grid(column=1, row=0)


# Start button
start_button = Button(text="Start", highlightthickness=0, width=6, command=start_timer)
start_button.grid(column=0, row=2)


# Reset button
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)


# Tick label
tick_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 15, "bold"))
tick_label.grid(column=1, row=3)


window.mainloop()