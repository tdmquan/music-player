#importing libraries

import os
import time
import threading
import random
import tkinter as tk
from tkinter import *
from tkinter import Tk
from tkinter import filedialog
from pygame import mixer
from pygame import time
import pygame
from PIL import Image, ImageTk
# Create a GUI window
root = tk.Tk()
root.title("Music Player")
root.geometry("920x720+400+85")
root.configure(background='#0f1a2b')
# tao bien toan cuc
Song_selected=False
auto=True
count=0
ButtonPlay = Image.open("music/play.png")
ButtonStop= Image.open("music/stop.png")
ButtonPause=Image.open("music/pause.png")
ButtonResume=Image.open("music/resume.png")
#...........
mixer.init()
pygame.init()
# Create a function to open a file
def AddMusic():
    path = filedialog.askopenfilename()
    print(path)
    if path.endswith(".mp3") or path.endswith(".wav") or path.endswith(".flac") :
    	Playlist.insert(END,path)

def PlayListSong():
    global count
    global Song_selected
    x=0
    num_items = Playlist.size()
    if num_items > 1:
        while True:
            for i in range (0,num_items):
                item = Playlist.get(i)
                Song_selected=True
                mixer.music.load(item)
                mixer.music.play()
                count=0
                print(i)
                print(item)
        # Wait for the song to finish playing
                while mixer.music.get_busy():
                    root.update()
    if num_items == 1:
         while True:
            mixer.music.load(0)
            mixer.music.play()
            print(0)
            print(item)
            while mixer.music.get_busy():
                root.update()


def PlayRandomSong():
    global count
    global Song_selected
    x=0
    num_items = Playlist.size()
    if num_items > 1:
        while True:
            random_index = random.randint(0, num_items - 1)
            if random_index!=x:
                item = Playlist.get(random_index)
                Song_selected=True
                mixer.music.load(item)
                mixer.music.play()
                count=0
                print(random_index)
                print(item)
                x=random_index
        # Wait for the song to finish playing
                while mixer.music.get_busy():
                    root.update()
            
    if num_items == 1:
         while True:
            mixer.music.load(0)
            mixer.music.play()
            print(random_index)
            print(item)
            while mixer.music.get_busy():
                root.update()
              
#-----------function PLay music--------------
def PlayMusic():
    global count
    global Song_selected
    Music_Name = Playlist.get(ACTIVE)
    print(Music_Name)
    Song_selected=True
    mixer.music.load(Playlist.get(ACTIVE))
    mixer.music.play()
    count=0
#---------------adjust progess------------------
def adjust_progess(event):
	if not auto:
		print(MusicProgess_slider.get())
def on_slider_press():
    global auto
    auto= False
    mixer.music.stop()
def on_slider_release():
    global auto
    global count
    mixer.music.load(Playlist.get(ACTIVE))
    music = mixer.Sound(Playlist.get(ACTIVE))
    music_length_in_seconds = music.get_length()
    period=(music_length_in_seconds/100)
    auto= True
    count=MusicProgess_slider.get()
    mixer.music.play(0,period*count)
	
#-------------update progess UI(thread 2)------
def update_progess():
	global auto
	global count
	if(auto==True):
		global Song_selected
		while(Song_selected==False):
			pygame.time.wait(100)
		if(Song_selected):
			if(mixer.music.get_busy()):
				music = mixer.Sound(Playlist.get(ACTIVE))
				music_length_in_seconds = music.get_length()
				period=(music_length_in_seconds/100)*1000
				while(1):
					pygame.time.wait(int(period))
					MusicProgess_slider.set(count)
					count+=1
#-----------function adjust volume--------------
def set_volume(volumelabel,volumeslider):
    volumelabel.config(text="Volume: "+str(int(volumeslider.get())))
    mixer.music.set_volume(volumeslider.get()/100)
#-----------function handle button Hover-------------
def button_hover(event,original):
   width,height=original.size
   ButtonTest=original.resize((width+30,height+30))
   ButtonTestTK=ImageTk.PhotoImage(ButtonTest)
   event.config(image=ButtonTestTK)
   event.image=ButtonTestTK
def button_leave(event,original):
   width,height=original.size
   ButtonTest=original.resize((width+20,height+20))
   ButtonTestTK=ImageTk.PhotoImage(ButtonTest)
   event.config(image=ButtonTestTK)
   event.image=ButtonTestTK
#-----------------------------------------------------
# icon
image_icon = PhotoImage(file="music/logo.png")
root.iconphoto(False, image_icon)

Top = PhotoImage(file="music/top.png")
Label(root, image=Top, bg="#0f1a2b").pack()

# logo
logo = PhotoImage(file="music/logo.png")
Label(root, image=logo, bg="#0f1a2b", bd=0).place(x=70, y=115)
# Button
#----------------------------------PLAY------------------------
width,height=ButtonPlay.size
ButtonPlay1=ButtonPlay.resize((width+30,height+30))
ButtonPlay1=ImageTk.PhotoImage(ButtonPlay1)
buttonplay=Button(root, image=ButtonPlay1, bg="#0f1a2b", bd=0,highlightbackground="#0f1a2b",activebackground="#0f1a2b",cursor="hand2",
       command=PlayMusic)
buttonplay.place(x=100, y=320)
buttonplay.bind("<Enter>",lambda event:button_hover(buttonplay,ButtonPlay ))
buttonplay.bind("<Leave>",lambda event:button_leave(buttonplay,ButtonPlay ))
#----------------------------------STOP------------------------
ButtonStop1 =ImageTk.PhotoImage(ButtonStop)
buttonstop=Button(root, image=ButtonStop1, bg="#0f1a2b", bd=0,highlightbackground="#0f1a2b",activebackground="#0f1a2b",cursor="hand2",
       command=mixer.music.stop)
buttonstop.place(x=20, y=450)
buttonstop.bind("<Enter>",lambda event:button_hover(buttonstop,ButtonStop))
buttonstop.bind("<Leave>",lambda event:button_leave(buttonstop,ButtonStop))
#----------------------------------RESUME------------------------
ButtonResume1 = ImageTk.PhotoImage(ButtonResume)
buttonresume=Button(root, image=ButtonResume1, bg="#0f1a2b", bd=0,highlightbackground="#0f1a2b",activebackground="#0f1a2b",cursor="hand2",
       command=mixer.music.unpause)
buttonresume.place(x=120, y=450)
buttonresume.bind("<Enter>",lambda event:button_hover(buttonresume,ButtonResume))
buttonresume.bind("<Leave>",lambda event:button_leave(buttonresume,ButtonResume))
#----------------------------------PAUSE------------------------
ButtonPause1 =ImageTk.PhotoImage(ButtonPause)
buttonpause=Button(root, image=ButtonPause1, bg="#0f1a2b", bd=0,highlightbackground="#0f1a2b",activebackground="#0f1a2b",cursor="hand2",
       command=mixer.music.pause)
buttonpause.place(x=220, y=450)
buttonpause.bind("<Enter>",lambda event:button_hover(buttonpause,ButtonPause))
buttonpause.bind("<Leave>",lambda event:button_leave(buttonpause,ButtonPause))
#-------------------------------------VOLUME SLIDER---------------
myVolume=("Helvetica",16)
VolumeLabel=Label(root,text="Volume: 0",bg="#0f1a2b",fg="white",font=myVolume)
VolumeLabel.place(x=105,y=555)
Volume_slider=tk.Scale(root,from_=0,to=100,orient=HORIZONTAL,bd=5,bg="#0f1a2b",troughcolor="#014958",width=8,sliderlength=10,length=250,fg="White",highlightbackground="#0f1a2b",showvalue=False,command=lambda event: set_volume(VolumeLabel,Volume_slider))
Volume_slider.place(x=20,y=580)
#------------------------------------------------------------------
#-------------------------------------MUSIC PROGESS----------------
MusicProgess_slider=tk.Scale(root,from_=0,to=100,orient=HORIZONTAL,bd=5,bg="#0f1a2b",troughcolor="#014958",width=8,sliderlength=10,length=280,fg="White",highlightbackground="#0f1a2b",showvalue=False,command=adjust_progess)
MusicProgess_slider.place(x=5,y=620)
MusicProgess_slider.bind("<ButtonPress-1>", lambda event: on_slider_press())
MusicProgess_slider.bind("<ButtonRelease-1>", lambda event: on_slider_release())
#------------------------------------------------------------------
# Label
Menu = PhotoImage(file="music/menu.png")
Label(root, image=Menu, bg="#0f1a2b").pack(padx=10, pady=50, side=RIGHT)

Frame_Music = Frame(root, bd=2, relief=RIDGE)
Frame_Music.place(x=330, y=350, width=550, height=300)

Button(root, text="Open Folder", width=15, height=2, cursor="hand2", font=("times new roman",
       12, "bold"), fg="White", bg="#014958",activebackground="#014958", command=AddMusic).place(x=330, y=300)
Button(root,text="PLay Random song",width=20,height=2,cursor="hand2",font=("times new roman",
       12, "bold"), fg="White",bg="#014958",activebackground="#014958", command=PlayRandomSong).place(x=480,y=300)
Button(root,text="PLay List song",width=20,height=2,cursor="hand2",font=("times new roman",
       12, "bold"), fg="White",bg="#014958",activebackground="#014958", command=PlayListSong).place(x=675,y=300)

Scroll = Scrollbar(Frame_Music)
Playlist = Listbox(Frame_Music, width=100, font=("Times new roman", 10), bg="#333333", fg="grey", selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=LEFT, fill=BOTH)
# Execute Tkinter
t = threading.Thread(target=update_progess,daemon=True)
t.start()
root.mainloop()
