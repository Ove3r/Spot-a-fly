import vlc
import tkinter as tk
from os import listdir
from threading import Thread
from urllib.parse import unquote


class Player:
    def __init__(self):
        # Window set up
        self.window = tk.Tk()
        self.window.title("Spot-A-Fly")
        self.window.wm_iconbitmap("icon.ico")
        self.window.resizable(0,0)
        

        # Previous Song Button
        self.back_button = tk.Button(
            text="Previous",
            fg="black",
            bg="white"
        )
        self.back_button.bind("<Button-1>", self.back_song)
        self.back_button.grid(row=1, column=0)

        # Play/Pause Button
        self.play_button = tk.Button(
            text="Play",
            fg="black",
            bg="white"
        )
        self.play_button.bind("<Button-1>", self.play_song)
        self.play_button.grid(row=1, column=1)

        # Next Song Button
        self.next_button = tk.Button(
            text="Next",
            fg="black",
            bg="white"
        )
        self.next_button.bind("<Button-1>", self.next_song)
        self.next_button.grid(row=1, column=2)

        # Music player related initializations
        self.get_saved_songs()

        # Creates the playlist label for testing currently and display
        self.songs_list_label = tk.Label(text="<-->")
        self.songs_list_label.grid(row=0, column=0, columnspan=3)

        # VLC Initialization
        self.player = vlc.Instance()
        self.media_list = self.player.media_list_new()
        for song in self.available_songs: # Adds all the songs to the player sequence
            self.media_list.add_media(f"songs/{song}")
        # Adds the sequence to the player and creates a player
        self.current_player = self.player.media_list_player_new()
        self.current_player.set_media_list(self.media_list)
        self.media_player = self.current_player.get_media_player()
        self.media_player.audio_set_volume(50)
        # Starts app
        thread = Thread(target=self.title_loop)
        thread.start()
        self.window.mainloop()

    def play_song(self, event):
        # Changes the play button to pause
        self.play_button["text"] = "Pause"
        self.play_button.bind("<Button-1>", self.pause_song)
        # Plays the music
        
        self.current_player.play()

    def pause_song(self, event):
        # Changes the pause button to play
        self.play_button["text"] = "Play"
        self.play_button.bind("<Button-1>", self.play_song)
        
        # Pauses the music
        self.current_player.pause()

    def next_song(self, event):
        self.current_player.next()

    def back_song(self, event):
        self.current_player.previous()

    def get_saved_songs(self):
        all_files = listdir("songs")
        self.available_songs = []
        for entry in all_files:
            if entry.split(".")[-1] == "mp3":
                self.available_songs.append(entry)
        return self.available_songs

    def title_loop(self):
        while True:
            if self.current_player.is_playing():  
                # Gets the title from file name. 
                media = self.media_player.get_media()
                track = media.get_mrl()
                self.current_track = track.split("/songs/")[1:]
                # Removes url formatting and sets the title
                self.songs_list_label["text"] = unquote("".join(self.current_track))


if __name__ == "__main__":
    player = Player()
