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
root.geometry("400x200")
root.title("Youtube Downloader")

link = StringVar()

label = Label(root,text="Paste Link Here ...",font ="arial 11 bold")
label.grid(row=0,column=0,padx=10,pady=5)
root.grid_columnconfigure(0,weight = 1)

entry = Entry(root,width=55,textvariable=link)
entry.grid(row=1,column=0,padx=10,pady=5)
root.grid_columnconfigure(1,weight = 1)

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
        downloaded = Label(root,text = "Downloading - "+url.title,font="arial 11",fg='#FFA500')
        downloaded.grid(row=2,column=0)
        root.grid_columnconfigure(2,weight = 1)
        video = url.streams.first()
        video.download(path)
        downloaded.config(text="Downloaded - "+url.title,fg='#008000')
    except :
        messagebox.showerror("Error","Invalid URL")

def saveLoc() :
    global path
    path=filedialog.askdirectory()
    
frame = Frame(root)
frame.grid(row=4,column=0)
root.grid_columnconfigure(3,weight = 1)

DwnButton = Button(frame,text="Download",font="arial 11 bold",command=threading)
DwnButton.grid(row=0,column=0,padx=10,pady=5)

saveButton = Button(frame,text="Save Location",font="arial 11 bold",command=saveLoc)
saveButton.grid(row=0,column=1,padx=10,pady=5)

root.mainloop()