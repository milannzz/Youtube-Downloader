from tkinter import *
from tkinter.font import nametofont
from pytube  import YouTube
from threading import Thread
from tkinter import filedialog,messagebox
from pathlib import Path

# Clearer Ui using ctypes
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
root.geometry("500x200")
root.title("Youtube Downloader")

Label(root,text="Paste Link Here ...",font="arial 9").grid(row=0,column=0,padx=10,pady=(10,5))
root.grid_columnconfigure(0,weight = 1)

link = StringVar()

entryFrame = Frame(root)
entryFrame.grid(row=1,column=0,padx=10,pady=5)
root.grid_columnconfigure(1,weight = 1)

def on_entry_click(*args):
    paste = root.clipboard_get()
    entry.insert(0,paste)

entry = Entry(entryFrame,width=56,textvariable=link,font="arial 9 italic")
entry.grid(row=0,column=0,padx=10,ipady=5)

entry.bind('<Button-1>', on_entry_click)


def threading():
    thread= Thread(target = downloader)
    thread.start()

def downloader():
    global path
    try :
        path
    except NameError:
        downloads_path = str(Path.home() / "Downloads")
        path = downloads_path

    #https://www.youtube.com/watch?v=Wch3gJG2GJ4
    try :
        url = YouTube(str(link.get()))
        downloaded = Label(root,text = "Downloading - "+url.title,font="arial 11 bold",fg='#FFA500')
        downloaded.grid(row=2,column=0)
        root.grid_columnconfigure(2,weight = 1)
        video = url.streams.first()
        video.download(path)
        downloaded.config(text="Downloaded - "+url.title,fg='#008000')
    except :
        messagebox.showerror("Error","Invalid Video URL")

def saveLoc() :
    global path
    path=filedialog.askdirectory()

def quality():
    pass

frame = Frame(root)
frame.grid(row=4,column=0,padx=10,pady=5)
root.grid_columnconfigure(3,weight = 1)

QualityButton = Button(frame,text="Quality",font="arial 9",state = 'disable',padx=8,pady=2,command=quality)
QualityButton.grid(row=0,column=0,padx=10,pady=5)

DwnButton = Button(frame,text="Download",font="arial 9",padx=8,pady=2,command=threading)
DwnButton.grid(row=0,column=1,padx=10,pady=5)

saveButton = Button(frame,text="Save Location",font="arial 9",padx=8,pady=2,command=saveLoc)
saveButton.grid(row=0,column=2,padx=10,pady=5)

root.mainloop()