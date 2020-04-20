from tkinter import *
import threading
import os
import tkinter.messagebox
from mutagen.mp3 import MP3
import time
from tkinter import filedialog
from pygame import mixer
root=Tk()
root.geometry("5000x10000")
root.configure(bg='#ff0055')
statusbar=Label(root,text="Welcome to melody",relief=SUNKEN,anchor=W)
statusbar.pack(side=BOTTOM,fill=X)

menubar=Menu(root)
root.config(menu=menubar)

Rightframe=Frame(root,bg="#000",bd='1',width='100',height='100')
Rightframe.pack(side=TOP,padx=5,pady=5)

Leftframe=Frame(root,bg="#000",bd='1',height='700',width='700')
Leftframe.pack(side=LEFT,padx=50)

Topframe=Frame(Rightframe,bg="#000",width='900',height='700')
Topframe.pack()

middleframe=Frame(Rightframe,bg="#000")
middleframe.pack()

bottomframe=Frame(root,bg="#000",width='40',height='1')
bottomframe.pack(pady=100,padx=100,side=LEFT)
 
def browse_file():
    global filename,musiclist
    musiclist=[]
    filename=filedialog.askopenfilename()
    musiclist.append(filename)
    lb1.insert(END,os.path.basename(filename))
    print(filename)

submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=submenu)
submenu.add_command(label="Open ",command=browse_file)
submenu.add_command(label="Exit ")

def About_us():
    tkinter.messagebox.showinfo("My new project",'project of music player')


submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=submenu)
submenu.add_command(label="About us",command=About_us)

mixer.init()
root.geometry('300x300')
root.title("Music player")

lengthlabel=Label(Topframe,text='Total Length=--:--',width='25',font=('arial',20),height='2')
lengthlabel.pack(padx=10,pady=10)

currenttimelabel=Label(Topframe,text='Current Time: --:--',width='25',font=('arial',20),height='2',relief=GROOVE)
currenttimelabel.pack(padx=10,pady=10)

lb1=Listbox(Leftframe,width='50',height='20')
lb1.pack(padx=5,pady=5)
 
btn1=Button(Leftframe,text='+ Add',width=20,font=('arial',20),height='1')
btn1.pack(padx=10,pady=10)
btn2=Button(Leftframe,text='- Delete',font=('arial',20),width=20,height='1')
btn2.pack(padx=10,pady=10)


def show_details():
    global  filename
    file_data=os.path.splitext(filename)
    if file_data[1]=='.mp3':
        audio=MP3(filename)
        total_length=audio.info.length
    else:
        a=mixer.Sound(filename)
        total_length=a.get_length()
    mins, secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text']="Total Length"+'-'+timeformat
    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time=0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs=divmod(current_time,60)
            mins=round(mins)
            secs=round(secs)
            timeformat='{:02d}:{:02d}'.format(mins,secs)
            currenttimelabel['text']="current time"+'-'+timeformat
            time.sleep(1)
            current_time += 1

def play_music():
    '''Function for Play the Music'''
    global paused,musiclist,filename  
    if paused:
        mixer.music.unpause()
        statusbar['text']="music Resumed"
        paused=FALSE
    else:
        index=lb1.curselection()[0]
        filename=musiclist[index]
        try:
            mixer.music.load(filename)
            mixer.music.play()
            print("PlayMusic")
            #statusbar['text']="Playing music"+" " +os.pathbasename(filename)
            show_details()
        except:
            tkinter.messagebox.showerror('File not found','please try again')
        
def stop_music():
    '''Function for Stop the Music'''
    mixer.music.stop()
    print("stopMusic")
    #statusbar['text']="music Stopped"
def rewind_music():
    '''Function for Rewind the Music'''
    play_music()
    statusbar['text']="music rewinded"

paused=FALSE

def pause_music():
    '''Function for Pause the Music'''
    global paused
    paused=TRUE
    mixer.music.pause()
    statusbar['text']="music paused"
muted=FALSE

def mute_music():
    '''Function for mute the Music'''
    global muted
    if muted:
         mixer.music.set_volume(0.3)
         volumebutton.configure(image=volumeicon)
         scale.set(30)
        
    else:
        mixer.music.set_volume(0)
        volumebutton.configure(image=muteicon)
        scale.set(0)
        muted=TRUE
    
def set_vol(val):
    volume=int(val)/100
    mixer.music.set_volume(volume)
    
#icon for Play button    
#playicon=PhotoImage(file='D:/Project Images/start-1.png')
playbutton=Button(middleframe,text='PLAY',font=('arial',14,'bold'),command=play_music,bg='#000',fg='#fff')
playbutton.grid(row=0,column=0,padx=10,pady=20)

#icon for Stop button
#stopicon=PhotoImage(file='D:/Project Images/stop-1.png')
stopbutton=Button(middleframe,text='STOP',font=('arial',14,'bold'),command=stop_music,bg='#000',fg='#fff')
stopbutton.grid(row=0,column=1,padx=10,pady=20)


#icon for Pause button
#pauseicon=PhotoImage(file='D:/Project Images/btn-2.png')
pausebutton=Button(middleframe,text='PAUSE',font=('arial',14,'bold'),command=pause_music,bg='#000',fg='#fff')
pausebutton.grid(row=0,column=2,padx=10,pady=20)

#rewindicon=PhotoImage(file='D:/Project Images/btn-1.png')
#rewindbutton=Button(bottomframe,command=rewind_music,bg='#000',fg='#fff')
#rewindbutton.grid(row=0,column=0)


#muteicon=PhotoImage(file='D:/Project Images/mute.png')
#volumeicon=PhotoImage(file='D:/Project Images/volume.png')
#volumebutton=Button(bottomframe,command=mute_music,bg='#000',fg='#fff')
#volumebutton.grid(row=0,column=2)

llabel=Label(bottomframe,text='SOUND',width='15',font=('arial',20),height='2',relief=GROOVE)
llabel.grid(column=0,row=0,padx=10,pady=10)

scale=Scale(bottomframe,from_=0,to_=100,orient=HORIZONTAL,font=('aria',15,'bold'),command=set_vol,width='25')
scale.set(30)
mixer.music.set_volume(0.3)
scale.grid(row=0,column=1,pady=15,padx=30)

newframe=Frame(root,bg="#ff0055",bd='1',height='700',width='700')
newframe.pack(side=RIGHT,padx=50)
x1=Label(newframe,text='MUSIC',width='15',bg="#ff0055",font=('gigi',50,'italic','bold'),height='1')
x1.pack(padx=10)
x1=Label(newframe,text='PLAYER',width='15',bg="#ff0055",font=('gigi',50,'italic','bold'),height='1')
x1.pack(padx=10)

def on_closing():
    stop_music()
    root.distroy()
    
#root.protocol("window close",on_closing)
root.mainloop()
