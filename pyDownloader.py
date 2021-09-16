from tkinter import *
from pytube  import YouTube, exceptions
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

def get_qualities_thread():
    thread= Thread(target = get_qualities)
    thread.start()

def get_qualities():
    global path
    status_string.set("Gathering video information ...")
    try :
        status_string.set("Checking download path")
        path
    except NameError:
        downloads_path = str(Path.home() / "Downloads")
        path = downloads_path

    #https://www.youtube.com/watch?v=Wch3gJG2GJ4 lowquality
    #https://www.youtube.com/watch?v=_jYB-RpkmUc highquality

    root_window.grid_columnconfigure(2, weight = 1)
    downloading_status.config(fg='grey')
    try :
        status_string.set("Gathering video information ...")
        url = YouTube(str(video_URL.get()))
    except :
        downloading_status.config(fg='red')
        status_string.set("Invalid URL")
        return

    quality_settings_list = []
    streams = url.streams
    for stream in streams:
        if(stream.type == "video"):
            status_string.set("Processing video codecs")
            quality_settings_list.append(str(stream.itag) + " | " + "Video " + stream.resolution + " " + str(stream.fps) + "fps")
        if(stream.type == "audio"):
            status_string.set("Processing audio codecs")
            quality_settings_list.append(str(stream.itag) + " | " + "Audio " + stream.abr)
    quality_combobox["values"] = quality_settings_list
    status_string.set("Processing completed")
    downloading_status.config(fg='green')
    root_window.update()


def downloader():
    global path
    downloading_status.config(fg="grey")
    status_string.set("Checking download path")
    try :
        path
    except NameError:
        downloads_path = str(Path.home() / "Downloads")
        path = downloads_path
    status_string.set("Connecting to servers")

    try :
        url = YouTube(str(video_URL.get()))
    except :
        downloading_status.config(fg='red')
        status_string.set("Invalid URL")        
        return

    if quality_combobox.get() == "Auto" :
        video = url.streams.first()
    else :
        itag = quality_combobox.get()
        s = ""
        for char in itag:
            if char == '|':
                break
            s += char
        video = url.streams.get_by_itag(s)
    video_length = "{:.2f}".format(url.length / 60)
    downloading_status.config(fg="orange")
    status_string.set("Downloading :" + url.title + " | "+ video_length +" min ")
    try :
        video.download(path)
    except:
        messagebox.showerror("Error", "Network Error,  Please check your connection.")
        return
    downloading_status.config(fg="green")
    status_string.set("Downloaded :" + url.title + " | "+ video_length + " min ")
    
def saveLoc() :
    global path
    path=filedialog.askdirectory()

def on_entry_click(*args):
    if URL_entry.get()=="":
        paste = root_window.clipboard_get()
        URL_entry.insert(0, paste)
        get_qualities_thread()

# <----------------------- UI --------------------------->

root_window = Tk()
root_window.geometry("630x180")
root_window.title("Youtube Downloader")
root_window.minsize(630, 180)
root_window.resizable(1, 1)

Label(root_window, text="Paste Link Here ...", font="Helvetica 9").grid(row=0, column=0, padx=10, pady=(10, 5))
root_window.grid_columnconfigure(0, weight = 1)
root_window.grid_rowconfigure(0, weight = 1)

video_URL = StringVar()

URL_container = Frame(root_window)
URL_container.grid(row=1, column=0, padx=10, pady=5)
root_window.grid_columnconfigure(1, weight = 1)

URL_entry = Entry(URL_container, width=68, textvariable=video_URL, font="Helvetica 9 italic")
URL_entry.grid(row=0, column=0, padx=10, ipady=5, ipadx=5, pady=5)
URL_entry.bind('<Button-1>',  on_entry_click)

frame = Frame(root_window)
frame.grid(row=4, column=0, padx=10, pady=5)
root_window.grid_columnconfigure(3, weight = 1)

quality_label = Label(frame, text="Quality:", font="Helvetica 9")
quality_label.grid(row=0, column=0, padx=0, pady=0, sticky=W)

status_string = StringVar()
status_string.set("")
downloading_status = Label(root_window, textvariable=status_string, font="Helvetica 11", fg='#808080')
downloading_status.grid(row=2, column=0)

quality_settings_list = ["Auto"]
quality_combobox = ttk.Combobox(frame, values=quality_settings_list, font="Helvetica 9", width=20)
quality_combobox.grid(row=0, column=1, padx=10, pady=5, ipady=4)
quality_combobox.set("Auto")

process_button = Button(frame, text="Process", font="Helvetica 9", padx=8, pady=2, command=get_qualities_thread)
process_button.grid(row=0, column=2, padx=10, pady=5)

download_button = Button(frame, text="Download", font="Helvetica 9", padx=8, pady=2, command=download_thread)
download_button.grid(row=0, column=3, padx=10, pady=5)

save_button = Button(frame, text="Save Location", font="Helvetica 9", padx=8, pady=2, command=saveLoc)
save_button.grid(row=0, column=4, padx=10, pady=5)

root_window.mainloop()