import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pytube import Playlist, YouTube
from ttkthemes import ThemedTk

def download_video(video_url, output_path, progress_callback):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        stream.download(output_path=output_path)
        progress_callback(yt.title)
    except Exception as e:
        print(f"Failed to download {video_url}: {e}")

def download_playlist(playlist_url, output_path, progress_callback):
    playlist = Playlist(playlist_url)
    for video_url in playlist.video_urls:
        download_video(video_url, output_path, progress_callback)

def start_download():
    playlist_url = url_entry.get()
    output_path = dir_entry.get()
    if not playlist_url or not output_path:
        messagebox.showerror("Error", "Please provide both a playlist URL and a download directory.")
        return

    def progress_callback(video_title):
        progress_var.set(progress_var.get() + 1)
        status_label.config(text=f"Downloading: {video_title}")

    def download_thread():
        total_videos = len(Playlist(playlist_url).video_urls)
        progress_var.set(0)
        progress_bar.config(maximum=total_videos)
        download_playlist(playlist_url, output_path, progress_callback)
        status_label.config(text="Download complete!")

    threading.Thread(target=download_thread).start()

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, directory)

# Create the main window with a themed style
root = ThemedTk(theme="equilux")
root.title("YouTube Playlist Downloader")
root.configure(bg='black')

# URL Entry
tk.Label(root, text="Playlist URL:", bg='black', fg='white').grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50, bg='#3e3e3e', fg='white', insertbackground='white')
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Directory Entry
tk.Label(root, text="Download Directory:", bg='black', fg='white').grid(row=1, column=0, padx=10, pady=10)
dir_entry = tk.Entry(root, width=50, bg='#3e3e3e', fg='white', insertbackground='white')
dir_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_directory, bg='#3e3e3e', fg='white').grid(row=1, column=2, padx=10, pady=10)

# Progress Bar
progress_var = tk.IntVar()
progress_bar = Progressbar(root, length=400, variable=progress_var)
progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Status Label
status_label = tk.Label(root, text="Status: Waiting to start", bg='black', fg='white')
status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Download Button
tk.Button(root, text="Download", command=start_download, bg='#3e3e3e', fg='white').grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Make the window transparent
root.attributes('-alpha', 0.9)

# Start the GUI event loop
root.mainloop()