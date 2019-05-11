from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
import tkinter.messagebox
from ttkthemes import themed_tk as tk
from PIL import Image, ImageTk
from pygame import mixer
from mutagen import File
from mutagen.mp3 import MP3
import io


class Player:

    def __init__(self):
        self.is_playing = False
        self.bgColor = '#141a28'
        self.sound = mixer.music
        self.root = tk.ThemedTk()
        self.root.set_theme('scidsand', background=self.bgColor)  # set theme for ttk
        s = ttk.Style()
        s.configure('Horizontal.TScale', background=self.bgColor)  # set bg for scale slider
        mixer.init()

        self.title_font = font.Font(family='Helvetica', size=24, weight='bold')
        self.length_font = font.Font(family='Helvetica', size=14, weight='bold')

        font.families()

        # set image for play and pause button
        self.mPlayImage = Image.open("play.png")
        self.mPlayImage = self.mPlayImage.resize((48, 48), Image.ANTIALIAS)
        self.mPauseImage = Image.open("pause.png")
        self.mPauseImage = self.mPauseImage.resize((48, 48), Image.ANTIALIAS)
        self.pauseImage = ImageTk.PhotoImage(self.mPauseImage)
        self.playImage = ImageTk.PhotoImage(self.mPlayImage)

        self.mSearchImage = Image.open("search.png")
        self.mSearchImage = self.mSearchImage.resize((28, 28), Image.ANTIALIAS)

        self.mArtwork = ImageTk.PhotoImage(Image.open("music.png"))

        self.playButton = None
        self.lengthlabel = None
        self.file = None
        self.title = 'Title'
        self.is_selected = False
        self.image = None
        self.title_label = Label()
        self.initUI()

    def open_music(self):

        # get file of music
        self.file = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        path = File(self.file)
        mp3 = MP3(self.file)

        total_length = mp3.info.length
        mMin, mSec = divmod(total_length, 60)
        mMin = round(mMin)
        mSec = round(mSec)
        timeformat = '{:02d}:{:02d}'.format(mMin, mSec)
        self.lengthlabel['text'] = timeformat

        # delete old data
        self.image.place_forget()

        try:
            artWork = path.tags['APIC:'].data
            stream = io.BytesIO(artWork)
            photo = Image.open(stream)
            photo = photo.resize((128, 128), Image.ANTIALIAS)
            self.mArtwork = ImageTk.PhotoImage(photo)
        except:

            self.mArtwork = ImageTk.PhotoImage(Image.open("music.png"))
        try:
            self.title = mp3['TIT2'][0]
        except:

            self.title = self.file.split('/')[-1][:-4]

        try:

            self.artist = mp3['TPE1'][0]

        except:
            self.artist = "Unknown"

        self.title_label['text'] = self.title

        self.image = Label(self.root, image=self.mArtwork, bg=self.bgColor)
        self.image.place(x=60, y=150)
        self.is_selected = True


    def play_music(self):

        if not self.is_playing:
            try:
                self.sound.load(self.file)
                self.sound.play()
                # switch to pause button
                self.playButton.configure(image=self.pauseImage, command=self.pause_music)

            except:
                tkinter.messagebox.showerror("File not found", "Music couldn't find the file")

        else:
            # switch to pause button
            self.playButton.configure(image=self.pauseImage, command=self.pause_music)
            self.sound.unpause()

    def pause_music(self):
        self.sound.pause()
        self.is_playing = True
        # switch to pause button
        self.playButton.configure(image=self.playImage, command=self.play_music)

    def set_volume(self, val):
        volume = float(val) / 100
        self.sound.set_volume(volume)

    def initUI(self):

        # intilaize window
        self.root.resizable(False, False)
        self.root.geometry('800x500')
        self.root.title('Music Player')
        self.root.iconbitmap(r'icon.ico')
        self.root.configure(bg=self.bgColor)

        # intilaize button
        self.playButton = Button(self.root, image=self.playImage, bg=self.bgColor,
                                 border="0", activebackground=self.bgColor, command=self.play_music)
        self.playButton.place(x=100, y=350)

        searchImage = ImageTk.PhotoImage(self.mSearchImage)
        search = Button(self.root, image=searchImage, bg=self.bgColor,
                        border="0", activebackground=self.bgColor, command=self.open_music).place(x=750, y=10)
        # label of volume
        Label(self.root, text='Volume', bg=self.bgColor, fg='#ffe063').place(x=45, y=300)
        self.lengthlabel = Label(self.root, text='--:--', bg=self.bgColor, fg='#ffe063',font=self.length_font)
        self.lengthlabel.place(x=100, y=120)

        # label of title
        self.title_label = Label(self.root, text="Title", bg=self.bgColor, fg='#ffe063',
                                 font=self.title_font)

        self.title_label.pack(side=TOP, anchor=NE, padx=80)

        self.image = Label(self.root, image=self.mArtwork, bg=self.bgColor)
        self.image.place(x=60, y=150)

        print(type(self.title_label))
        # slider for volume
        slider = ttk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL, command=self.set_volume, length=110,
                           style='Horizontal.TScale')
        slider.set(70)
        mixer.music.set_volume(.7)
        slider.place(x=65, y=320)

        # infinite loop to show window
        self.root.mainloop()


if __name__ == '__main__':
    player = Player()
