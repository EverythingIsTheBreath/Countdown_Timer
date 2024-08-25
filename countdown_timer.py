import tkinter as tk
from tkinter import ttk
import pygame
import json
import os

class CountdownTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Countdown Timer")
        self.master.geometry("400x400")

        self.time_left = 0
        self.running = False

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load saved times
        self.load_times()

        self.create_widgets()

    def create_widgets(self):
        # Large time display and entry
        self.time_entry = tk.Entry(self.master, font=("Arial", 48), justify='center', width=8)
        self.time_entry.insert(0, "00:00:00")
        self.time_entry.pack(pady=20)

        # Start/Pause and Reset buttons
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)

        self.start_pause_button = ttk.Button(button_frame, text="Start", command=self.start_pause)
        self.start_pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Saved times grid
        saved_times_frame = ttk.Frame(self.master)
        saved_times_frame.pack(pady=20)

        self.saved_time_entries = []
        self.saved_time_buttons = []
        for i in range(6):
            entry = tk.Entry(saved_times_frame, width=10, justify='center')
            entry.insert(0, self.saved_times[i])
            entry.grid(row=i//3*2, column=i%3, padx=5, pady=5)
            entry.bind('<FocusOut>', lambda e, i=i: self.save_time(i))
            self.saved_time_entries.append(entry)

            start_button = ttk.Button(saved_times_frame, text="Start", command=lambda i=i: self.start_saved_timer(i))
            start_button.grid(row=i//3*2+1, column=i%3, padx=5, pady=5)
            self.saved_time_buttons.append(start_button)

    def start_pause(self):
        if not self.running:
            try:
                time_parts = self.time_entry.get().split(':')
                if len(time_parts) == 3:
                    hours, mins, secs = map(int, time_parts)
                    self.time_left = hours * 3600 + mins * 60 + secs
                    if self.time_left > 0:
                        self.running = True
                        self.start_pause_button.config(text="Pause")
                        self.time_entry.config(state='disabled')
                        self.update()
                    else:
                        raise ValueError("Time must be greater than zero")
                else:
                    raise ValueError("Invalid time format")
            except ValueError as e:
                tk.messagebox.showerror("Error", str(e))
        else:
            self.running = False
            self.start_pause_button.config(text="Start")
            self.time_entry.config(state='normal')

    def reset(self):
        self.running = False
        self.time_left = 0
        self.time_entry.config(state='normal')
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "00:00:00")
        self.start_pause_button.config(text="Start")

    def update(self):
        if self.running:
            if self.time_left >= 0:
                mins, secs = divmod(self.time_left, 60)
                hours, mins = divmod(mins, 60)
                time_string = f"{hours:02d}:{mins:02d}:{secs:02d}"
                self.time_entry.config(state='normal')
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, time_string)
                self.time_entry.config(state='disabled')
                
                if self.time_left == 3:
                    pygame.mixer.music.load("sounds/t-0.wav")  # Load the sound file for t-03
                    pygame.mixer.music.play()  # Play the sound file
                elif self.time_left == 2:
                    pygame.mixer.music.load("sounds/t-0.wav")  # Load the sound file for t-02
                    pygame.mixer.music.play()  # Play the sound file
                elif self.time_left == 1:
                    pygame.mixer.music.load("sounds/t-0.wav")  # Load the sound file for t-01
                    pygame.mixer.music.play()  # Play the sound file
                elif self.time_left == 0:
                    pygame.mixer.music.load("sounds/alert.wav")  # Load the sound file for t-00
                    pygame.mixer.music.play()  # Play the sound file
                
                self.time_left -= 1
                self.master.after(1000, self.update)
            else:
                self.running = False
                self.start_pause_button.config(text="Start")
                self.time_entry.config(state='normal')

    def save_time(self, button_index):
        time_string = self.saved_time_entries[button_index].get()
        try:
            hours, mins, secs = map(int, time_string.split(':'))
            if 0 <= hours <= 23 and 0 <= mins <= 59 and 0 <= secs <= 59:
                formatted_time = f"{hours:02d}:{mins:02d}:{secs:02d}"
                self.saved_time_entries[button_index].delete(0, tk.END)
                self.saved_time_entries[button_index].insert(0, formatted_time)
                self.saved_times[button_index] = formatted_time
                self.save_times()
            else:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid time format. Use HH:MM:SS")
            self.saved_time_entries[button_index].delete(0, tk.END)
            self.saved_time_entries[button_index].insert(0, "00:00:00")

    def start_saved_timer(self, button_index):
        time_string = self.saved_time_entries[button_index].get()
        try:
            time_parts = time_string.split(':')
            if len(time_parts) == 3:
                hours, mins, secs = map(int, time_parts)
                self.time_left = hours * 3600 + mins * 60 + secs
                if self.time_left > 0:
                    self.time_entry.delete(0, tk.END)
                    self.time_entry.insert(0, time_string)
                    self.start_pause()
                else:
                    raise ValueError("Time must be greater than zero")
            else:
                raise ValueError("Invalid time format")
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def save_times(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        with open("data/saved_times.json", "w") as file:
            json.dump(self.saved_times, file)

    def load_times(self):
        if os.path.exists("data/saved_times.json"):
            with open("data/saved_times.json", "r") as file:
                self.saved_times = json.load(file)
        else:
            self.saved_times = ["00:00:00"] * 6

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
