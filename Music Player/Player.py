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
import os


class Player:

    def __init__(self):

        self.bgColor = '#141a28'
        self.sound = mixer.music
        self.root = tk.ThemedTk()

        self.root.set_theme('plastik', background=self.bgColor)  # set theme for ttk

        ttk.Style().configure('Horizontal.TScale', background=self.bgColor)  # set bg for scale slider

        self.title_font = font.Font(family='Helvetica', size=14, weight='bold')
        self.length_font = font.Font(family='Helvetica', size=14, weight='bold')
        self.list_font = font.Font(family='Helvetica', size=12)
        self.label_list_font = font.Font(family='Helvetica', size=10)
        font.families()

        # set image for play, pause, next, previous and browse button
        self.mPlayImage = Image.open("play.png")
        self.mPauseImage = Image.open("pause.png")
        self.mAddSong = Image.open("add.png")
        self.mVolumeOn = Image.open("speaker.png")
        self.mVolumeOff = Image.open("speakeroff.png")
        self.mNext = Image.open("next-track.png")
        self.mBack = Image.open("backt-track.png")
        self.artworkM = Image.open("image.png")

        # resize all images
        self.mPlayImage = self.mPlayImage.resize((40, 40), Image.ANTIALIAS)
        self.mPauseImage = self.mPauseImage.resize((40, 40), Image.ANTIALIAS)
        self.mNext = self.mNext.resize((25, 25), Image.ANTIALIAS)
        self.mBack = self.mBack.resize((25, 25), Image.ANTIALIAS)
        self.mAddSong = self.mAddSong.resize((28, 28), Image.ANTIALIAS)
        self.mVolumeOn = self.mVolumeOn.resize((40, 40), Image.ANTIALIAS)
        self.mVolumeOff = self.mVolumeOff.resize((40, 40), Image.ANTIALIAS)
        self.artworkM = self.artworkM.resize((220, 220), Image.ANTIALIAS)

        # set imageTK for all button
        self.pauseImage = ImageTk.PhotoImage(self.mPauseImage)
        self.playImage = ImageTk.PhotoImage(self.mPlayImage)
        self.nextImage = ImageTk.PhotoImage(self.mNext)
        self.backImage = ImageTk.PhotoImage(self.mBack)
        self.volumeOnImage = ImageTk.PhotoImage(self.mVolumeOn)
        self.volumeOffImage = ImageTk.PhotoImage(self.mVolumeOff)
        self.mArtwork = ImageTk.PhotoImage(self.artworkM)
        self.add = ImageTk.PhotoImage(self.mAddSong)

        # variables
        self.is_playing = False
        self.playButton = None
        self.volume = None
        self.file = None
        self.title = 'Title'
        self.image_file = None
        self.title_label = None
        self.list_label = None
        self.list_box = None
        self.list_length = None
        self.timeformat = None
        self.muted = False
        self.slider = None
        self.index = 0
        self.playList = []
        self.selected_song = 0
        self.frequancy = 22050

        mixer.init(frequency=72050)

        self.initUI()

    # set title and image
    def set_title_image(self, file):
        path = File(file)
        mp3 = MP3(file)

        if mp3:
            try:
                if path:
                    artWork = path.tags['APIC:'].data
                    stream = io.BytesIO(artWork)
                    photo = Image.open(stream)
                    photo = photo.resize((220, 220), Image.ANTIALIAS)
                    self.mArtwork = ImageTk.PhotoImage(photo)
            except:
                self.mArtwork = ImageTk.PhotoImage(self.artworkM)
            try:
                self.title = mp3['TIT2'][0]
            except:
                self.title = file.split('/')[-1][:-4]

            # delete old image
            self.image_file.place_forget()

            # set title of music
            self.title_label['text'] = self.title

            # set image of music
            self.image_file = Label(self.root, image=self.mArtwork, bg=self.bgColor)
            self.image_file.place(x=100, y=100)

    def open_music(self):
        # get file of music
        try:
            self.file = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
            if self.file:
                mp3 = MP3(self.file)
                self.get_length(mp3.info.length)
                self.add_to_playlist(self.file)
                self.list_length.insert(self.index, self.timeformat)
                self.list_label['text'] = ''
        except:
            tkinter.messagebox.showerror('Something went wrong', 'this file not working here')

    def set_speed(self):
        frequancy = int(self.input.get()) / 10
        mixer.init(frequency=int(frequancy * self.frequancy))

    def play_music(self, event=None, selected=None):

        if event:
            self.is_playing = False

        if not self.is_playing:
            try:
                if not selected:
                    mSelected_song = self.list_box.curselection()
                    self.selected_song = int(mSelected_song[0])
                    selected = self.selected_song
                self.list_box.activate(selected)
                self.list_box.selection_set(selected)
                play_it = self.playList[selected]
                self.sound.load(play_it)
                self.set_title_image(play_it)
                self.sound.play()
                # switch to pause button
                self.playButton.configure(image=self.pauseImage, command=self.pause_music)

            except:
                tkinter.messagebox.showerror("File not found", "Can't find music \n "
                                                               "press the magnifying in the top to add to your list ")
        else:
            # switch to pause button
            self.playButton.configure(image=self.pauseImage, command=self.pause_music)
            self.sound.unpause()
            self.is_playing = False

    def pause_music(self):
        self.sound.pause()
        self.is_playing = True
        # switch to pause button
        self.playButton.configure(image=self.playImage, command=self.play_music)

    def set_volume(self, val):
        volume = float(val) / 100
        self.sound.set_volume(volume)

    def add_to_playlist(self, file):
        file = os.path.basename(file)
        self.list_box.insert(self.index, file)
        self.playList.insert(self.index, self.file)
        self.index += 1

    def get_length(self, total_length):
        mMin, mSec = divmod(total_length, 60)
        mMin = round(mMin)
        mSec = round(mSec)
        self.timeformat = '{:02d}:{:02d}'.format(mMin, mSec)

    def next_music(self):
        self.selected_song = self.selected_song + 1
        next_selection = self.selected_song
        if next_selection > self.list_box.size() - 1:
            next_selection = 0
            self.selected_song = next_selection
        self.play_music(None, next_selection)
        print(str(self.list_box.size()) + 'size')
        print(str(next_selection) + '  next')

    def prev_music(self):
        self.selected_song = self.selected_song - 1
        prev_selection = self.selected_song
        if prev_selection < 0:
            prev_selection = self.list_box.size() - 1
            self.selected_song = prev_selection
        self.play_music(None, prev_selection)
        print(str(prev_selection) + '  prev')

    def mute_music(self):
        if self.muted:  # Unmute the music
            mixer.music.set_volume(0.7)
            self.volume.configure(image=self.volumeOnImage)
            self.slider.set(70)
            self.muted = False
        else:  # mute the music
            mixer.music.set_volume(0)
            self.volume.configure(image=self.volumeOffImage)
            self.slider.set(0)
            self.muted = True

    def initUI(self):

        # intilaize window
        self.root.resizable(False, False)
        self.root.geometry('800x500')
        self.root.title('Music Player')
        self.root.iconbitmap(r'icon.ico')
        self.root.configure(bg=self.bgColor)

        # initialize button
        self.playButton = Button(self.root, image=self.playImage, bg=self.bgColor,
                                 border='0', activebackground=self.bgColor, command=self.play_music)
        self.playButton.place(x=75, y=445)

        self.nextButton = Button(self.root, image=self.nextImage, bg=self.bgColor,
                                 border='0', activebackground=self.bgColor, command=self.next_music)
        self.nextButton.place(x=130, y=453)

        self.backButton = Button(self.root, image=self.backImage, bg=self.bgColor,
                                 border='0', activebackground=self.bgColor, command=self.prev_music)
        self.backButton.place(x=35, y=452)

        addButton = Button(self.root, image=self.add, bg=self.bgColor,
                           border='0', activebackground=self.bgColor, command=self.open_music).place(x=750, y=450)

        # Button of volume
        self.volume = Button(self.root, image=self.volumeOnImage, bg=self.bgColor,
                             border='0', activebackground=self.bgColor, command=self.mute_music)
        self.volume.place(x=250, y=450)

        # image of file
        self.image_file = Label(self.root, image=self.mArtwork, bg=self.bgColor)
        self.image_file.place(x=100, y=100)

        # slider for volume
        self.slider = ttk.Scale(self.root, from_=0, to=100, orient=HORIZONTAL, command=self.set_volume, length=200,
                                style='Horizontal.TScale')
        self.slider.set(70)
        mixer.music.set_volume(.7)
        self.slider.pack(side=BOTTOM, pady=20)

        # label of title
        self.title_label = Label(self.root, text='', bg=self.bgColor, fg='#ffffff',
                                 font=self.title_font)

        self.title_label.pack(side=BOTTOM)

        # list for music
        self.list_box = Listbox(self.root, bg=self.bgColor, bd=0, height='12', width='55', highlightthickness=0,
                                font=self.list_font, fg='#ffffff', selectbackground=self.bgColor,
                                highlightcolor='#ffffff')
        self.list_box.bind('<Double-1>', self.play_music)
        self.list_box.place(x=350, y=120)

        # list for length
        self.list_length = Listbox(self.root, bg=self.bgColor, bd=0, height='12', width='5', highlightthickness=0,
                                   font=self.list_font, fg='#ffffff', selectbackground=self.bgColor,
                                   highlightcolor='#ffffff', selectforeground='#ffffff')
        self.list_length.place(x=650, y=120)

        self.list_label = Label(self.root, text='there is no items in your list\n '
                                                'click add button to add to your list', bg=self.bgColor, fg='#ffffff',
                                font=self.label_list_font)
        self.list_label.place(x=440, y=200)

        # infinite loop to show window
        self.root.mainloop()


if __name__ == '__main__':
    player = Player()
