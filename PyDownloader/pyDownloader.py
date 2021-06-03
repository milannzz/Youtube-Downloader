from ssl import ALERT_DESCRIPTION_ACCESS_DENIED
from tkinter import *
from pytube  import YouTube
from threading import Thread

# Clearer Ui using ctypes
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()


root.title("Youtube Downloader")

link = StringVar()

label = Label(root,text="Paste Link Here ...",font ="arial 11 bold")
label.place(x=200,y=20)

entry = Entry(root,width=55,textvariable=link)
label.place(x=20,y=40)

def threadingg():
    thread= Thread(target = downloader)
    thread.start()

def downloader():
    downloaded = Label(root,text = "Downloading...",font="arial 11",fg='#FFA500')
    label.place(x=20,y=60)
    url = YouTube(str(link.get()))
    video = url.streams.first()
    video.download()
    downloaded.config(text="Downloaded",fg='#008000')

DwnButton = Button(root,text="Download",font="arial 11 bold",command=threadingg)
label.place(x=200,y=80)

root.mainloop()