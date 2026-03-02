import tkinter as tk
import pygame
import os
from threading import Thread
import time

class CalculatorOfDoom:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator of doom and despair")
        self.root.geometry("420x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1A1A2E") 
        self.total = 0
        self.current = ""
        self.operator = ""
        self.reset_next = False
        self.music_playing = False

        try:
            pygame.mixer.pre_init(44100, -16, 2, 4096)
            pygame.mixer.init()
            if pygame.mixer.get_init() is None:
                print("Audio system failed to initialize")
                self.has_music = False
            else:
                print("Audio system initialized successfully")
                possible_paths = [
                    r"C:\Users\TUF\Downloads\sino-x-multo-x-back-to-friends.mp3"
                ]
                
                self.music_file = None
                for path in possible_paths:
                    if os.path.exists(path):
                        self.music_file = path
                        break
                
                if self.music_file:
                    print(f"Found music file at: {self.music_file}")
                    try:
                        pygame.mixer.music.load(self.music_file)
                        pygame.mixer.music.set_volume(0.5)
                        self.has_music = True
                    except pygame.error as e:
                        print(f"Failed to load music: {e}")
                        self.has_music = False
                else:
                    print("Music file not found in any of the searched locations")
                    self.has_music = False
        except Exception as e:
            print(f"Audio initialization error: {e}")
            self.has_music = False

        self.display = tk.Label(
            root,
            text="0",
            anchor='e',
            justify="right",
            font=("Helvetica", 26),
            bg="#1A1A2E",  
            fg="#E6F7FF", 
            padx=24,
            wraplength=380,
            height=3
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.create_buttons()

        for i in range(6):
            self.root.rowconfigure(i, weight=1)
        for i in range(4):
            self.root.columnconfigure(i, weight=1)

        for child in self.root.winfo_children():
            if isinstance(child, tk.Button):
                child.configure(pady=10)

    def create_buttons(self):
        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for r, row in enumerate(buttons, start=1):
            for c, key in enumerate(row):
                if key == "0":
                    btn = tk.Button(
                        self.root, text=key, font=("Helvetica", 24),
                        bg="#4A4A6A", fg="#E6F7FF", bd=0, 
                        activebackground="#6A6A8A", activeforeground="#FFFFFF",
                        command=lambda x=key: self.button_press(x)
                    )
                    btn.grid(row=r, column=0, columnspan=2, sticky="nsew", padx=1, pady=1)
                elif key == "." and len(row) == 3:
                    btn = tk.Button(
                        self.root, text=key, font=("Helvetica", 24),
                        bg="#4A4A6A", fg="#E6F7FF", bd=0, 
                        activebackground="#6A6A8A", activeforeground="#FFFFFF",
                        command=lambda x=key: self.button_press(x)
                    )
                    btn.grid(row=r, column=2, sticky="nsew", padx=1, pady=1)
                elif key == "=" and len(row) == 3:
                    btn = tk.Button(
                        self.root, text=key, font=("Helvetica", 24),
                        bg="#4ECDC4", fg="#1A1A2E", bd=0,  
                        activebackground="#7EE8FA", activeforeground="#1A1A2E",
                        command=lambda x=key: self.button_press(x)
                    )
                    btn.grid(row=r, column=3, sticky="nsew", padx=1, pady=1)
                else:
                    btn = tk.Button(
                        self.root, text=key, font=("Helvetica", 24),
                        bg=self.get_color(key), fg=self.get_text_color(key), bd=0,
                        activebackground=self.get_active_color(key), activeforeground=self.get_text_color(key),
                        command=lambda x=key: self.button_press(x)
                    )
                    btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

    def get_color(self, key):
        if key in ["+", "-", "×", "÷", "="]:
            return "#4ECDC4"  
        elif key in ["AC", "+/-", "%"]:
            return "#6D72C3"  
        else:
            return "#4A4A6A" 

    def get_text_color(self, key):
        if key in ["AC", "+/-", "%"]:
            return "#1A1A2E" 
        else:
            return "#E6F7FF"  

    def get_active_color(self, key):
        if key in ["+", "-", "×", "÷", "="]:
            return "#7EE8FA"  
        elif key in ["AC", "+/-", "%"]:
            return "#8D93E8"  
        else:
            return "#6A6A8A"  

    def button_press(self, key):
        if key == "AC":
            self.total = 0
            self.current = ""
            self.operator = ""
            self.display.config(text="0")
            self.reset_next = False
            self.stop_music()

        elif key in "+-×÷":
            if self.current:
                self.total = float(self.current)
                self.operator = key
                self.reset_next = True

        elif key == "=":
            self.lyrics = [
                " ",
                "Patuloy kong hahanapin",
                "kahulugan ng pagibig",
                "at habang buhay na mag iisa",
                "hindi na na nanaginip",
                "hindi na ma makagising",
                "pa sindi nga ng ilaw",
                "Minumulto nako ng damdamin ko",
                "ng damdamin ko",
                "how can we go back to being friends",
                "dinadalaw moko bawat gabi",
                "pag papahirap sakin",
                "how can you look at me and pretend",
                "haplost moy ramdam parin sa dilim",
                "how can we go back to being friends",
                "when we just shared a bed?"
            ]
            self.timings = [5000, 5500, 4000, 9000, 4300, 4700, 4000, 3700, 3500, 3500, 3000, 3000, 3500, 4500, 4000, 2500]  
            self.current_line = 0
            
            if self.has_music:
                self.play_music()
            self.show_lyrics_with_timing()

        elif key == "+/-":
            if self.current:
                if self.current.startswith("-"):
                    self.current = self.current[1:]
                else:
                    self.current = "-" + self.current
                self.display.config(text=self.current)

        elif key == "%":
            if self.current:
                self.current = str(float(self.current) / 100)
                self.display.config(text=self.format_number(self.current))

        else:  
            if self.reset_next:
                self.current = ""
                self.reset_next = False

            if key == "." and "." in self.current:
                return

            self.current += key
            self.display.config(text=self.current)
    
    def play_music(self):
        if not self.has_music or self.music_playing:
            return
            
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            
            pygame.mixer.music.stop()
            
            pygame.mixer.music.rewind()
            
            pygame.mixer.music.play(loops=0)
            self.music_playing = True
            print("Music playback started")
            
            Thread(target=self.monitor_music_status, daemon=True).start()
        except Exception as e:
            print(f"Error in play_music: {e}")
            self.music_playing = False

    def stop_music(self):
        if self.has_music and self.music_playing:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
                print("Music stopped")
            except Exception as e:
                print(f"Error stopping music: {e}")

    def monitor_music_status(self):
        while self.music_playing:
            if not pygame.mixer.music.get_busy():
                self.music_playing = False
                print("Music finished playing")
                break
            time.sleep(0.1)

    def show_lyrics_with_timing(self):
        if self.current_line < len(self.lyrics):
            line = self.lyrics[self.current_line]
            self.display.config(text=line)
            delay = self.timings[self.current_line]
            self.current_line += 1
            self.root.after(delay, self.show_lyrics_with_timing)
        else:
            self.reset_next = True
            self.current = ""
            self.operator = ""
            self.total = 0

    def format_number(self, num_str):
        num = float(num_str)
        return str(int(num)) if num == int(num) else str(round(num, 8))


if __name__ == "__main__":
    try:
        pygame.init()
        print("Pygame initialized successfully")
    except Exception as e:
        print(f"Pygame failed to initialize: {e}")
    
    root = tk.Tk()
    app = CalculatorOfDoom(root)
    root.mainloop()
