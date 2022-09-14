import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
window = tk.Tk()

import requests
import bs4
import random

beatles_song_lst=['The Ballad of John and Yoko','Getting Better','I Feel Fine','All My Loving' ,'Hello Goodbye',
'From Me to You','Drive My Car','Youve Got to Hide Your Love Away','Yellow Submarine','Nowhere Man','Lucy in the Sky With Diamonds',
'This Boy','The Long and Winding Road','We Can Work It Out','Taxman','Revolution','Paperback Writer','Here Comes the Sun','Helter Skelter',
'Day Tripper','Get Back','Eight Days a Week','I Am the Walrus','Got to Get You Into My Life','Twist and Shout','Rain','All You Need Is Love',
'With a Little Help From My Friends','Cant Buy Me Love','Come Together','A Hard Days Night','I Saw Her Standing There','Eleanor Rigby',
'Norwegian Wood This Bird Has Flown','She Loves You','Help','Yesterday','Hey Jude','Ticket to Ride','I Want to Hold Your Hand','Penny Lane',
'Something','Let It Be','In My Life','While My Guitar Gently Weeps','Strawberry Fields Forever','A Day in the Life','When Im Sixty Four']


rand_lst_of_int=[]
songname = ""
score = 0

def get_lines(num_lines, songname):
    result = requests.get("https://genius.com/The-beatles-" + songname.replace(' ','-') + "-lyrics")
    soup = bs4.BeautifulSoup(result.text,'lxml')
    lyrics = soup.select('p')[0].getText()
    lines = list(lyrics.split('\n'))
    use=[]
    for i in lines:
        if '[' in i or i == '':
            pass
        else:
            use.append(i)
    print(len(use))
    lyric_str=''
    rand_ind = random.randint(0,(len(use)-num_lines))
    for i in use[rand_ind:rand_ind+num_lines]:
        lyric_str = lyric_str+i+'\n'
    return lyric_str

def getNextSongName(songnames):
    rnd = random.randint(0, len(songnames))
    return songnames[rnd].lower()

def start(nlines, songnames):
    global songname

    songname = getNextSongName(songnames)
    print("Name of randomly chosen song: " + songname)

    lyrics['text'] = get_lines(nlines, songname)

def check_if_correct(guess):

    global songname
    global score

    while score < 10 and score >= 0:
        if guess == songname:
            messagebox.showinfo("Correct", "You are correct")
            score += 1
            current_score['text'] = f'Current Score: {score}'
            guess_input['text'] = ""
            break
        else:
            messagebox.showinfo("Wrong", "You are wrong. Showing next song.")
            score = 0
            current_score['text'] = f'Current Score: {score}'
            guess_input['text'] = ""
            break

        lyrics['text'] = ""
        
#####TKINTER#####
window.title('GUESS THE BEATLES')

canvas = tk.Canvas(window, height =600, width=1000,bg='gray')
canvas.pack()

bg_photo=tk.PhotoImage(file='bg.png')

frame = tk.Label(window, image=bg_photo)
frame.place(relheight=1, relwidth=1)

fonts = list(font.families())
font_title = fonts.index('Imprint MT Shadow')

title_label=tk.Label(frame, text="GUESS THE BEATLES' SONG",bg='black',fg='white', font=(fonts[font_title],25))
title_label.place(relx=0.33,rely=0.01)

rules_photo=tk.PhotoImage(file='rules.png')

rules_label=tk.Button(frame, image=rules_photo,state='disabled')
rules_label.place(relx=0.015,rely=0.1)

#######
#SCORE#
#######
textvar= f'Current Score: {score}'
current_score=tk.Label(frame,text=textvar, bg='white',fg='black',font=('Courier',30))
current_score.place(relx=0.015,rely=0.40)

max_score=tk.Label(frame,text='Maximum Score: 10', bg='white',fg='black',font=('Courier',30))
max_score.place(relx=0.015,rely=0.47)

##############
#GUESS AREA###
##############

guess_label=tk.Label(frame,text='Guess the name of the song: ',bg='black',fg='white',font=('Helvetica',20),height=1)
guess_label.place(relx=0.01,rely=0.76)

#guess_input=tk.Text(frame,height=1, width=35, font=('Helvetica',20),highlightbackground='black',highlightthickness=5)
#guess_input.place(relx=0.01,rely=0.80)

guess_input=Entry(frame, width=35, font=('Helvetica',20),highlightbackground='black',highlightthickness=5)
guess_input.place(relx=0.01,rely=0.80)

disclaimer_label=tk.Label(frame,text='Only letters. No special characters.',bg='black',fg='white',font=('Helvetica',15),height=1)
disclaimer_label.place(relx=0.01,rely=0.85)

def getGuess():
    return guess_input.get().strip().lower()

###########
##BUTTONS##
###########

easy_photo = tk.PhotoImage(file='easy_button.png')
nlines = 0

easy_button=tk.Button(frame,image= easy_photo ,bg='gray',fg='black', state='normal',command=lambda:start(20,beatles_song_lst))
easy_button.place(relx=0.015, rely=0.22)

medium_photo = tk.PhotoImage(file='medium_button.png')

medium_button=tk.Button(frame,image= medium_photo ,bg='gray',fg='black', state='normal',command=lambda:start(10,beatles_song_lst))
medium_button.place(relx=0.11, rely=0.22)

hard_photo = tk.PhotoImage(file='hard_button.png')

hard_button=tk.Button(frame,image= hard_photo ,bg='gray',fg='black', state='normal',command=lambda:start(5,beatles_song_lst))
hard_button.place(relx=0.207, rely=0.22)

submit_photo=tk.PhotoImage(file='submit_button.png')

submit_button=tk.Button(frame, image= submit_photo, bg='gray',fg='black', state='normal',command=lambda:check_if_correct(getGuess()))
submit_button.place(relx=0.01, rely=0.90)



#-----------
###LYRICS###
#-----------

lyric_box = tk.Frame(window, bg='white',highlightbackground='black',highlightthickness=5)
lyric_box.place(relheight=0.8, relwidth=0.35, relx=0.6, rely=0.1)


lyrics=tk.Label(lyric_box,font=('Helvetica',10))
lyrics.pack()

window.mainloop()
