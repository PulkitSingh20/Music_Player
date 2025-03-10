import os
import pygame
import tkinter as tk
from tkinter import filedialog, ttk
from mutagen.mp3 import MP3
import random

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Music Player")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e2e")

        pygame.mixer.init()
        self.playlist = []
        self.current_track_index = 0
        self.is_playing = False
        self.is_paused = False

        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self.root, bg="#1e1e2e")
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Music Player", font=("Arial", 24, "bold"), bg="#1e1e2e", fg="white").pack(pady=10)
        
        self.track_var = tk.StringVar()
        tk.Label(frame, textvariable=self.track_var, font=("Arial", 14), bg="#1e1e2e", fg="white", wraplength=500).pack(pady=5)

        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(frame, variable=self.progress_var, maximum=100, length=500).pack(pady=5)

        time_frame = tk.Frame(frame, bg="#1e1e2e")
        time_frame.pack(fill=tk.X)
        self.current_time_var, self.total_time_var = tk.StringVar(value="00:00"), tk.StringVar(value="00:00")
        tk.Label(time_frame, textvariable=self.current_time_var, bg="#1e1e2e", fg="white").pack(side=tk.LEFT)
        tk.Label(time_frame, textvariable=self.total_time_var, bg="#1e1e2e", fg="white").pack(side=tk.RIGHT)

        control_frame = tk.Frame(frame, bg="#1e1e2e")
        control_frame.pack(pady=10)

        button_style = {"bg": "#2c2c3e", "fg": "white", "font": ("Arial", 12), "width": 10}
        tk.Button(control_frame, text="Select Folder", command=self.select_folder, **button_style).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Previous", command=self.play_previous, **button_style).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Play", command=self.play_music, **button_style).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Pause", command=self.pause_music, **button_style).grid(row=0, column=3, padx=5)
        tk.Button(control_frame, text="Next", command=self.play_next, **button_style).grid(row=0, column=4, padx=5)

        self.playlist_box = tk.Listbox(frame, width=70, height=10, bg="#2c2c3e", fg="white", selectbackground="#4c4c5e")
        self.playlist_box.pack(pady=10)
        self.playlist_box.bind('<<ListboxSelect>>', self.on_select)

        option_frame = tk.Frame(frame, bg="#1e1e2e")
        option_frame.pack()
        self.shuffle_var, self.repeat_var = tk.BooleanVar(), tk.BooleanVar()
        tk.Checkbutton(option_frame, text="Shuffle", variable=self.shuffle_var, bg="#1e1e2e", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Checkbutton(option_frame, text="Repeat", variable=self.repeat_var, bg="#1e1e2e", fg="white").pack(side=tk.LEFT, padx=10)

        self.update_progress()

    def select_folder(self):
        self.playlist.clear()
        self.playlist_box.delete(0, tk.END)

        folder = filedialog.askdirectory()
        if not folder:
            return

        for file in os.listdir(folder):
            if file.endswith(('.mp3', '.wav', '.ogg', '.flac')):
                self.playlist.append(os.path.join(folder, file))
                self.playlist_box.insert(tk.END, file)

        if self.playlist:
            self.current_track_index = 0
            self.play_music()

    def play_music(self):
        if not self.playlist:
            return

        pygame.mixer.music.stop()
        track = self.playlist[self.current_track_index]
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()

        self.track_var.set(os.path.basename(track))
        self.total_time_var.set(self.format_time(MP3(track).info.length))

        self.is_playing, self.is_paused = True, False

    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.unpause() if self.is_paused else pygame.mixer.music.pause()
            self.is_paused = not self.is_paused

    def play_next(self):
        if not self.playlist:
            return
        self.current_track_index = random.randint(0, len(self.playlist) - 1) if self.shuffle_var.get() else (self.current_track_index + 1) % len(self.playlist)
        self.play_music()

    def play_previous(self):
        if not self.playlist:
            return
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.play_music()

    def on_select(self, event):
        selection = self.playlist_box.curselection()
        if selection:
            self.current_track_index = selection[0]
            self.play_music()

    def update_progress(self):
        if self.is_playing and not self.is_paused:
            current_pos = pygame.mixer.music.get_pos() / 1000  
            self.current_time_var.set(self.format_time(current_pos))

            if not pygame.mixer.music.get_busy():
                self.play_music() if self.repeat_var.get() else self.play_next()

        self.root.after(1000, self.update_progress)

    def format_time(self, seconds):
        return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"

if __name__ == "__main__":
    root = tk.Tk()
    MusicPlayer(root)
    root.mainloop()