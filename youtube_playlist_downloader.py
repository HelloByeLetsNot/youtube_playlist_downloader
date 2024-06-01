import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from ttkthemes import ThemedTk
from yt_dlp import YoutubeDL


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.playlist_url = tk.StringVar()
        self.output_path = tk.StringVar()
        self.progress_var = tk.IntVar()
        self.create_widgets()

    def create_widgets(self):
        self.root.title("YouTube Playlist Downloader")
        self.root.configure(bg='black')

        tk.Label(self.root, text="Playlist URL:", bg='black', fg='white').grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.playlist_url, width=50, bg='#3e3e3e', fg='white',
                 insertbackground='white').grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Download Directory:", bg='black', fg='white').grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.output_path, width=50, bg='#3e3e3e', fg='white',
                 insertbackground='white').grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_directory, bg='#3e3e3e', fg='white').grid(row=1,
                                                                                                          column=2,
                                                                                                          padx=10,
                                                                                                          pady=10)

        self.progress_bar = Progressbar(self.root, length=400, variable=self.progress_var)
        self.progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.status_label = tk.Label(self.root, text="Status: Waiting to start", bg='black', fg='white')
        self.status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        tk.Button(self.root, text="Download", command=self.start_download_thread, bg='#3e3e3e', fg='white').grid(row=4,
                                                                                                                 column=0,
                                                                                                                 columnspan=3,
                                                                                                                 padx=10,
                                                                                                                 pady=10)

        self.root.attributes('-alpha', 0.9)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def start_download_thread(self):
        threading.Thread(target=self.start_download).start()

    def start_download(self):
        playlist_url = self.playlist_url.get()
        output_path = self.output_path.get()
        if not playlist_url or not output_path:
            messagebox.showerror("Error", "Please provide both a playlist URL and a download directory.")
            return

        self.status_label.config(text="Status: Downloading...")
        self.progress_var.set(0)

        def download_hook(d):
            if d['status'] == 'finished':
                self.downloaded_videos += 1
                self.progress_var.set(self.downloaded_videos)
                self.status_label.config(text=f"Downloaded: {d['info_dict']['title']}")
            elif d['status'] == 'downloading':
                self.status_label.config(text=f"Downloading: {d['info_dict']['title']} ({d['_percent_str']})")

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [download_hook],
            'noplaylist': False,  # Allow downloading playlists
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

        self.status_label.config(text="Download complete!")


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = YouTubeDownloader(root)
    root.mainloop()
