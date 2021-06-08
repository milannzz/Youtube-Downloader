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
label.grid(row=0,column=0,padx=20,pady=(30,10))

entry = Entry(root,width=55,textvariable=link)
entry.grid(row=1,column=0,padx=20,pady=10)

def threading():
    thread= Thread(target = downloader)
    thread.start()

def downloader():
    downloaded = Label(root,text = "Downloading...",font="arial 11",fg='#FFA500')
    downloaded.grid(row=2,column=0)
    url = YouTube(str(link.get()))
    video = url.streams.first()
    video.download()
    downloaded.config(text="Downloaded",fg='#008000')

DwnButton = Button(root,text="Download",font="arial 11 bold",command=threading)
DwnButton.grid(row=3,column=0,padx=20,pady=10)

root.mainloop()