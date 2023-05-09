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
# --------------------Create a GUI window--------------------------
root = tk.Tk()
root.title("Music Player")
root.geometry("920x735+400+85")
root.configure(background='#A43B84')
root.resizable(False,False)
# --------------------tao bien toan cuc-----------------------------
#style.theme_settings('warning',{'TScale':{'configure':{'background':'#0f1a2b'}}})
Song_selected=False
auto=True
count=0
allstop=False
tempstop=False
ButtonPlay = Image.open("music/playresize(2).png")
ButtonStop= Image.open("music/stopMusic.png")
ButtonPause=Image.open("music/pauseresize.png")
ButtonResume=Image.open("music/resumeMusic.png")
ButtonRandom=Image.open("music/random.png")
ButtonPLaylist=Image.open("music/playlist.png")
ButtonOpenFile=Image.open("music/openFile.png")
#...........
mixer.init()
pygame.init()
# Create a function to open a file
def AddMusic():
    path = filedialog.askopenfilename()
    print(path)
    if path.endswith(".mp3") or path.endswith(".wav") or path.endswith(".flac") :
    	Playlist.insert(END,path)
#----------------PlaylistSong----------------------------------------------------------- 	
def PlayListSong():
    global allstop
    global count
    global tempstop
    allstop=False
    global Song_selected
    x=0
    num_items = Playlist.size()
    flag=False
    if num_items > 0:
        while not allstop:
            if allstop:
                 break
            i=0
            while(i<=num_items):
                if allstop:
                     break
                if(i==num_items):
                    i=0
                if(flag==True):
                    flag=False
                    i=i-1
                    item = Playlist.get(i)
                    count=MusicProgess_slider.get()
                    mixer.music.play(0,period*count)
                else:
                    item = Playlist.get(i)
                    Song_selected=True
                    mixer.music.load(item)
                    mixer.music.play()
                    count=0
        # Wait for the song to finish playing
                while mixer.music.get_busy():
                    root.update()
                if(tempstop):
                    music = mixer.Sound(Playlist.get(ACTIVE))
                    music_length_in_seconds = music.get_length()
                    period=(music_length_in_seconds/100)
                    while tempstop:
                        flag=True
                        root.update()
                        if not tempstop:
                            break
                i+=1
#--------------------PLAYRANDOMSONG-----------------------------------------
def PlayRandomSong():
    global count
    global Song_selected
    global allstop
    global tempstop
    mark=-1
    flag=False
    allstop=False
    x=0
    num_items = Playlist.size()
    if num_items > 1:
        while not allstop:
            if allstop:
                 break
            random_index = random.randint(0, num_items - 1)
            if (random_index!=x or num_items==1):
                if allstop:
                 break
                if(flag==True):
                    flag=False
                    random_index=mark
                    item = Playlist.get(random_index)
                    count=MusicProgess_slider.get()
                    mixer.music.play(0,period*count)
                else:
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
                if(tempstop):
                    music = mixer.Sound(Playlist.get(ACTIVE))
                    music_length_in_seconds = music.get_length()
                    period=(music_length_in_seconds/100)
                    mark=random_index
                    while tempstop:
                        flag=True
                        root.update()
                        if not tempstop:
                        	break
#-----------function PLay music--------------
def PlayMusic():
    global allstop
    allstop=False
    global count
    global Song_selected
    Music_Name = Playlist.get(ACTIVE)
    print(Music_Name)
    Song_selected=True
    mixer.music.load(Playlist.get(ACTIVE))
    mixer.music.play()
    count=0
#-----------function Stop music--------------
def onstop():
    global allstop
    mixer.music.stop()
    allstop=True

#-----------function Pause music--------------
def onpause():
    global tempstop
    mixer.music.pause()
    tempstop=True
#-----------function Resume music--------------
def onresume():
    global tempstop
    mixer.music.unpause()
    tempstop=False
#---------------adjust progess------------------
def adjust_progess(event):
	dem=0	
def on_slider_press():
    global tempstop
    global auto
    auto= False
    tempstop=True
    mixer.music.stop()
def on_slider_release():
    global tempstop
    global auto
    global count
    tempstop=False
    mixer.music.load(Playlist.get(ACTIVE))
    music = mixer.Sound(Playlist.get(ACTIVE))
    music_length_in_seconds = music.get_length()
    period=(music_length_in_seconds/100)
    auto= True
    count=MusicProgess_slider.get()
    mixer.music.play(0,period*count)

#-------------update progess UI(thread 2)------

def update_progess():
    global allstop
    global auto
    global tempstop
    allstop=False
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
                        if allstop:
                             MusicProgess_slider.set(0)
                        if not tempstop:
                            pygame.time.wait(int(period))
                            MusicProgess_slider.set(count)
                            count+=1
             		

#-----------function adjust volume--------------
def set_volume(volumelabel,volumeslider):
    volumelabel.config(text="Volume: "+str(int(volumeslider.get())))
    mixer.music.set_volume(volumeslider.get()/100)
#-----------function handle button Hover-------------
def button_hover(event,original):
   print("hover")
  # width,height=original.size
   #ButtonTest=original.resize((width+30,height+30))
  # ButtonTestTK=ImageTk.PhotoImage(ButtonTest)
  # event.config(image=ButtonTestTK)
  # event.image=ButtonTestTK
def button_leave(event,original):
   print('leave')
   #width,height=original.size
   #ButtonTest=original.resize((width+20,height+20))
   #ButtonTestTK=ImageTk.PhotoImage(ButtonTest)
   #event.config(image=ButtonTestTK)
   #event.image=ButtonTestTK
#-----------------------------------------------------
# icon
image_icon = PhotoImage(file="music/logo.png")
root.iconphoto(False, image_icon)
#top
Top = PhotoImage(file="music/topMusic.png")
Label(root, image=Top, bg="#A43B8F").pack()

#body
#MyMusic=PhotoImage(file="music/Mymusic.png")
#musiclabel=Label(root, image=MyMusic,bg="#A43B84",bd=0).place(x=13, y=370)
Body=PhotoImage(file="music/bodyMusic.png")
bodymusic=Label(root,image=Body,bg="#A43B8F",bd=0).place(x=0,y=241)
# logo
logo = PhotoImage(file="music/logoMusic.png")
logolabel=Label(root, image=logo,bg="#A43B8F",bd=0).place(x=51, y=180)
# Button
#----------------------------------PLAY------------------------
width,height=ButtonPlay.size
ButtonPlay1=ButtonPlay.resize((width+30,height+30))
ButtonPlay1=ImageTk.PhotoImage(ButtonPlay1)
buttonplay=Button(root, image=ButtonPlay1, bg="#7e36b4", bd=0,highlightbackground="#7e36b4",activebackground="#7e36b4",cursor="hand2",
       command=PlayMusic)
buttonplay.place(x=750, y=530)
buttonplay.bind("<Enter>",lambda event:button_hover(buttonplay,ButtonPlay ))
buttonplay.bind("<Leave>",lambda event:button_leave(buttonplay,ButtonPlay ))
#----------------------------------STOP------------------------
ButtonStop1 =ImageTk.PhotoImage(ButtonStop)
buttonstop=Button(root, image=ButtonStop1, bg="#7e36b4", bd=0,highlightbackground="#7e36b4",activebackground="#7e36b4",cursor="hand2",
       command=onstop)
buttonstop.place(x=400, y=570)
buttonstop.bind("<Enter>",lambda event:button_hover(buttonstop,ButtonStop))
buttonstop.bind("<Leave>",lambda event:button_leave(buttonstop,ButtonStop))
#----------------------------------RESUME------------------------
ButtonResume1 = ImageTk.PhotoImage(ButtonResume)
buttonresume=Button(root, image=ButtonResume1, bg="#7e36b4", bd=0,highlightbackground="#7e36b4",activebackground="#7e36b4",cursor="hand2",
       command=onresume)
buttonresume.place(x=680, y=610)
buttonresume.bind("<Enter>",lambda event:button_hover(buttonresume,ButtonResume))
buttonresume.bind("<Leave>",lambda event:button_leave(buttonresume,ButtonResume))
#----------------------------------PAUSE------------------------
ButtonPause1 =ImageTk.PhotoImage(ButtonPause)
buttonpause=Button(root, image=ButtonPause1, bg="#7e36b4", bd=0,highlightbackground="#7e36b4",activebackground="#7e36b4",cursor="hand2",
       command=onpause)
buttonpause.place(x=600, y=610)
buttonpause.bind("<Enter>",lambda event:button_hover(buttonpause,ButtonPause))
buttonpause.bind("<Leave>",lambda event:button_leave(buttonpause,ButtonPause))
#-------------------------------------VOLUME SLIDER---------------
myVolume=("Helvetica",10)
VolumeLabel=Label(root,text="Volume: 0",bg="#7e36b4",fg="white",font=myVolume)
VolumeLabel.place(x=382,y=515)
Volume_slider=tk.Scale(root,from_=100,to=0,orient=VERTICAL,bd=5,bg="#7e36b4",troughcolor="#3b1434",width=8,sliderlength=10,length=120,fg="White",highlightbackground="#7e36b4",showvalue=False,command=lambda event: set_volume(VolumeLabel,Volume_slider))
Volume_slider.place(x=400,y=380)
#------------------------------------------------------------------
#-------------------------------------MUSIC PROGESS----------------
MusicProgess_slider=tk.Scale(root,from_=0,to=100,orient=HORIZONTAL,bg="#7e36b4",troughcolor="#3b1434",width=8,sliderlength=15,length=370,fg="White",highlightbackground="#A43B84",showvalue=False,command=adjust_progess)
MusicProgess_slider.place(x=470,y=530)
MusicProgess_slider.bind("<ButtonPress-1>", lambda event: on_slider_press())
MusicProgess_slider.bind("<ButtonRelease-1>", lambda event: on_slider_release())
#------------------------------------------------------------------
# Label
Menu = PhotoImage(file="music/listbox.png")
Label(root, image=Menu, bg="#A43B8F").pack(padx=0, pady=50, side=RIGHT)

Frame_Music = Frame(root, bd=2, relief=RIDGE)
Frame_Music.place(x=482, y=388, width=370, height=130)
#-------------------BUTTON OPEN FILE-----------------------------------------
ButtonOpenFile1 =ImageTk.PhotoImage(ButtonOpenFile)
buttonopen=Button(root, image=ButtonOpenFile1, bg="#3a1433", bd=0,highlightbackground="#3a1433",activebackground="#3a1433",cursor="hand2", command=AddMusic)
buttonopen.place(x=420,y=300)
#-------------------BUTTON RANDOM-----------------------------------------
ButtonRandom1 =ImageTk.PhotoImage(ButtonRandom)
buttonrandom=Button(root, image=ButtonRandom1, bg="#3a1433", bd=0,highlightbackground="#3a1433",activebackground="#3a1433",cursor="hand2", command=PlayRandomSong)
buttonrandom.place(x=480,y=300)
#-------------------BUTTON PLAYLIST----------------------------------------
ButtonPLayList1 =ImageTk.PhotoImage(ButtonPLaylist)
buttonplaylist=Button(root, image=ButtonPLayList1, bg="#3a1433", bd=0,highlightbackground="#3a1433",activebackground="#3a1433",cursor="hand2", command=PlayListSong)
buttonplaylist.place(x=520,y=300)

Scroll = Scrollbar(Frame_Music)
Playlist = Listbox(Frame_Music, width=100, font=("Times new roman", 15,"bold"), bg="#333333", fg="white", selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=LEFT, fill=BOTH)
# Execute Tkinter
t = threading.Thread(target=update_progess,daemon=True)
t.start()
buttonplay.lift()
buttonresume.lift()
buttonstop.lift()
buttonpause.lift()
Volume_slider.lift()
VolumeLabel.lift()
MusicProgess_slider.lift()
print(logo)
root.mainloop()
