from tkinter import *
from pytube  import YouTube
from threading import Thread

# Clearer Ui using ctypes
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
root.geometry("500x300")
root.title("Youtube Downloader")

link = StringVar()

label = Label(root,text="Paste Link Here ...",font ="arial 11 bold")
label.grid(row=0,column=0,padx=10,pady=(10,5))

entry = Entry(root,width=55,textvariable=link)
entry.grid(row=1,column=0,padx=10,pady=5)

def threading():
    thread= Thread(target = downloader)
    thread.start()

def downloader():
    url = YouTube(str(link.get()))
    downloaded = Label(root,text = "Downloading - "+url.title,font="arial 11",fg='#FFA500')
    downloaded.grid(row=2,column=0)
    video = url.streams.first()
    video.download()
    downloaded.config(text="Downloaded - "+url.title,fg='#008000')

def saveLoc() :
    pass

frame = Frame(root)
frame.grid(row=4,column=0)

DwnButton = Button(frame,text="Download",font="arial 11 bold",command=threading)
DwnButton.grid(row=0,column=0,padx=10,pady=5)

saveButton = Button(frame,text="Save Location",font="arial 11 bold",command=saveLoc)
saveButton.grid(row=0,column=1,padx=10,pady=5)

root.mainloop()