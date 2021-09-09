from tkinter import *
from pytube  import YouTube
from threading import Thread
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

# Clearer Ui using ctypes
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)


# <------- Functions / Definitions -------->

def download_thread():
    thread= Thread(target = downloader)
    thread.start()

def process_thread():
    thread= Thread(target = Process)
    thread.start()

def Process():
    global path
    status_string.set("Processing")
    try :
        status_string.set("Checking download path")
        path
    except NameError:
        downloads_path = str(Path.home() / "Downloads")
        path = downloads_path

    #https://www.youtube.com/watch?v=Wch3gJG2GJ4 lowquality
    #https://www.youtube.com/watch?v=_jYB-RpkmUc highquality

    root.grid_columnconfigure(2, weight = 1)

    try :
        status_string.set("Getting info ...")
        url = YouTube(str(link.get()))
    except :
        messagebox.showerror("Error", "Invalid Video URL")
        status_string.set("Failed,  Try again")
        return

    streams = url.streams
    for stream in streams:
        if(stream.type == "video"):
            status_string.set("getting videos")
            quality_settings.append(str(stream.itag) + " | " + "Video " + stream.resolution + " " + str(stream.fps) + "fps")
        if(stream.type == "audio"):
            status_string.set("getting audios")
            quality_settings.append(str(stream.itag) + " | " + "Audio " + stream.abr)
    quality_combo["values"] = quality_settings
    status_string.set("Processed")
    downloading_status.config(fg='green')
    root.update()


def downloader():
    global path
    try :
        path
    except NameError:
        downloads_path = str(Path.home() / "Downloads")
        path = downloads_path

    #https://www.youtube.com/watch?v=Wch3gJG2GJ4

    downloaded = Label(root, text = "Processing...", font="Helvetica 9 bold", fg='#808080')
    downloaded.grid(row=2, column=0)
    root.grid_columnconfigure(2, weight = 1)

    try :
        url = YouTube(str(link.get()))
    except :
        messagebox.showerror("Error", "Invalid Video URL")
        downloaded.config(text="")
        return

    if quality_combo.get() == "Auto" :
        video = url.streams.first()
    else :
        itag = quality_combo.get()
        s = ""
        for char in itag:
            if char == '|':
                break
            s += char
        video = url.streams.get_by_itag(s)

    downloaded.config(text = "Downloading: "+url.title+"| "+str(url.length / 60) +" min", fg='#FFA500')
    
    try :
        video.download(path)
    except:
        messagebox.showerror("Error", "Network Error,  Please check your connection.")
        return

    downloaded.config(text="Downloaded: "+url.title+"|"+str(url.length / 60) + " min", fg='#008000')
    
def saveLoc() :
    global path
    path=filedialog.askdirectory()

def quality():
    pass

def on_entry_click(*args):
    if entry.get()=="":
        paste = root.clipboard_get()
        entry.insert(0, paste)

# <----------------------- UI --------------------------->

root = Tk()
root.geometry("600x200")
root.title("Youtube Downloader")
root.resizable(0, 0)

Label(root, text="Paste Link Here ...", font="Helvetica 9").grid(row=0, column=0, padx=10, pady=(10, 5))
root.grid_columnconfigure(0, weight = 1)

link = StringVar()

entryFrame = Frame(root)
entryFrame.grid(row=1, column=0, padx=10, pady=5)
root.grid_columnconfigure(1, weight = 1)

entry = Entry(entryFrame, width=68, textvariable=link, font="Helvetica 9 italic")
entry.grid(row=0, column=0, padx=10, ipady=5, ipadx=5, pady=5)

entry.bind('<Button-1>',  on_entry_click)

frame = Frame(root)
frame.grid(row=4, column=0, padx=10, pady=5)
root.grid_columnconfigure(3, weight = 1)

quality_label = Label(frame, text="Quality:", font="Helvetica 9")
quality_label.grid(row=0, column=0)

status_string = StringVar()
status_string.set("")
downloading_status = Label(root, textvariable=status_string, font="Helvetica 9 bold", fg='#808080')
downloading_status.grid(row=2, column=0)

quality_settings = ["Auto"]
quality_combo = ttk.Combobox(frame, values=quality_settings, font="Helvetica 9", width=16)
quality_combo.grid(row=0, column=1, padx=10, pady=5, ipady=4)
quality_combo.set("Auto")

process_button = Button(frame, text="Process", font="Helvetica 9", padx=8, pady=2, command=process_thread)
process_button.grid(row=0, column=2, padx=10, pady=5)

Download_button = Button(frame, text="Download", font="Helvetica 9", padx=8, pady=2, command=download_thread)
Download_button.grid(row=0, column=3, padx=10, pady=5)

save_button = Button(frame, text="Save Location", font="Helvetica 9", padx=8, pady=2, command=saveLoc)
save_button.grid(row=0, column=4, padx=10, pady=5)

root.mainloop()