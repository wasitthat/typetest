from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import time

NUM_WORDS = 10000
lines = open('words.txt', 'r')
words = lines.readlines()


def hex_to_rgba(hexa):
    rgb = []
    for i in (1, 3, 5):
        decimal = int(hexa[i:i + 2], 16)
        rgb.append(decimal)
    rgb.append(255)
    return tuple(rgb)


class SpeedTest:
    def __init__(self, root):
        self.i = 0
        self.j = 0
        self.iter_times = []
        self.bg = '#374273'
        self.game_text = [x.split('\n')[0] for x in words]
        self.logoImg = Image.open('tt.png')
        self.logoImg = self.logoImg.resize((150, 60))
        self.logoImg = ImageTk.PhotoImage(self.logoImg)
        self.text_bg = '#66b3db'
        self.goImg = Image.open('go.png')
        self.goImg = self.goImg.resize((85, 65))
        self.goImg = ImageTk.PhotoImage(self.goImg)
        self.color = '#ffffffff'
        self.opacity = IntVar()
        self.opacity.set(100)
        self.fill = hex_to_rgba(self.color)
        self.icon = PhotoImage(file='key.png')
        self.gameImg = Image.new('RGBA', (400, 400))
        print(type(self.gameImg))
        self.wpm = 0.0
        self.cor_words = []
        self.incor_words = []
        self.correct_words = 0
        self.correct_chars = 0
        self.incorrect_words = 0
        self.incorrect_chars = 0
        self.current_key = ''
        self.finish_time = None
        self.words_shown = []
        self.red_letter = StringVar()
        self.green_letter = StringVar()
        self.game_running = False
        root.iconphoto(False, self.icon)
        root.resizable(False, False)
        root.bind_all('<KeyPress>', lambda e: self.onKeyPress(event=e))
        self.photo = Image.open('stars.jpg')
        self.photo = self.photo.resize((1000, 800))
        self.photo = ImageTk.PhotoImage(self.photo)
        self.start_time = None
        self.wt = None
        self.font = ImageFont.truetype('tahoma', 30)
        self.text_mask = Image.new('RGBA', (400, 400))
        self.mdr = ImageDraw.Draw(self.text_mask)
        self.ht = self.font.getsize(text=self.game_text[0])[1]
        self.window = Frame(root, width=1000, height=800, padx=20, pady=20, bg=self.bg)
        self.window.grid(column=0, row=0)
        self.end_screen = Label(width=500, height=350)

        # logo
        self.logo_label = Label(self.window, image=self.logoImg, bg=self.bg)
        self.logo_label.image = self.logoImg
        self.logo_label.grid(column=2, row=0, sticky=NSEW)

        # background image
        self.bg_image = Label(self.window, image=self.photo)
        self.bg_image.image = self.photo

        # go button
        self.go_button = Button(self.window, image=self.goImg,
                                width=90, height=80, bg=self.bg, command=self.load_words)
        self.go_button.image = self.goImg
        self.go_button.grid(column=2, row=2)
        self.text_screen = Label(window, width=800, height=500)

        # copyright
        Label(self.window, text='\u00A9 John Oden 2022', bg=self.bg).grid(column=1, row=12)

    def onKeyPress(self, event):
        if event.char == '\x1b':
            self.end_game()
        if event.keysym == 'Return':
            if not self.game_running:
                self.load_words()
                return
        if event.char.isalpha():
            if not self.game_running:
                self.game_running = True
                self.i, self.j = 0, 0
        if self.game_running:
            if not self.start_time:  # check for start time
                self.start_time = time.time()  # set if not already
            if self.current_key is '':
                self.current_key = event.char
            if self.words_shown is not None:  # only if there are words...
                if self.current_key:  # if the user entered a key
                    if self.i < len(self.words_shown) and \
                            self.j < len(self.words_shown[self.i]):  # don't segfault
                        self.wt = self.font.getsize(text=self.words_shown[self.i][self.j])[0]  # letter width
                        if self.words_shown[self.i][self.j] == ' ':  # ---- at the end of the word?----#
                            if self.current_key != ' ':  # user should enter 'space'
                                self.incorrect_chars += 1  # if not,
                                self.incorrect_words += 1  # ding the score
                                self.mdr.text(text=' ', xy=(self.w, self.h), fill='#ff0000ff',
                                              font=self.font)  # post the fail
                                self.w += self.font.getsize(' ')[0] + 15
                            else:  # otherwise
                                self.correct_chars += 1  # score a letter
                                self.correct_words += 1  # score a word
                                self.cor_words.append(self.words_shown[self.i])  # add it to the list
                                self.mdr.text(text=' ', xy=(self.w, self.h), fill='#00ff00ff',
                                              font=self.font)  # post the score
                                self.w += self.font.getsize(' ')[0] + 15
                            if self.words_shown[self.i + 1] == '\n':
                                self.h += self.ht * 2  # line down by one
                                self.i += 1  # first letter of next word
                                self.w = 0  # carriage return to zero
                                self.j = 0  # next letter
                            self.j = 0
                            self.i += 1
                        else:  # ---- otherwise ----#
                            if self.words_shown[self.i][self.j] == self.current_key:  # letter matches?
                                self.mdr.text(text=self.current_key, xy=(self.w, self.h),
                                              fill='#00ff00ff', font=self.font)  # post it
                                self.correct_chars += 1  # score it

                            else:  # you screwed up
                                self.incorrect_chars += 1  # ding
                                self.mdr.text(text=self.words_shown[self.i][self.j],
                                              xy=(self.w, self.h), fill='#ff0000ff',
                                              font=self.font)  # post fail
                            self.j += 1  # next letter
                            self.w += self.wt
                        self.current_key = ''
                        self.update_screen()
                    if self.i >= len(self.words_shown)-1:
                        if self.j >= len(self.words_shown[self.i-1])-1:  # don't segfault
                            self.end_game()

    def update_screen(self):
        try:
            self.gameImg.paste(self.text_mask, (0, 0), self.text_mask)  # format screen
            self.gameImg.image = ImageTk.PhotoImage(self.gameImg)  # convert thingy
            self.text_screen = Label(self.window, image=self.gameImg.image, bg=self.text_bg)  # frame it
            self.text_screen.grid(column=1, row=1)
        except:
            pass

    def get_word(self):
        return self.game_text[random.randint(0, NUM_WORDS - 1)]

    def load_words(self):
        try:
            self.text_screen.grid_forget()
            self.text_screen.destroy()
        except:
            pass
        self.text_screen = Label(self.window, width=800, height=500)
        self.gameImg = Image.new('RGBA', (400, 400))
        self.text_mask = Image.new('RGBA', (400, 400))
        self.mdr = ImageDraw.Draw(self.text_mask)
        self.font = ImageFont.truetype('tahoma', 30)
        self.h = 0
        self.w = 0
        W = 400
        H = 300
        while self.h < H:
            self.w = 0
            while self.w < W:
                self.j = 0
                word = self.get_word()
                width = self.font.getsize(text=word + ' ')[0]
                while (width + 30 + self.w > W) and self.j < 7:
                    word = self.get_word()
                    self.j += 1
                if (width + 30 + self.w > W) and self.j >= 7:
                    self.words_shown.append('\n')
                    pass
                else:
                    self.mdr.text(text=word, xy=(self.w, self.h), fill=self.fill, font=self.font)
                    self.words_shown.append(word + ' ')
                self.w += width + 15
            self.h += self.ht * 2
        self.gameImg.paste(self.text_mask, (0, 0), self.text_mask)
        photo = ImageTk.PhotoImage(self.gameImg)
        self.gameImg.image = photo
        self.text_screen = Label(self.window, image=photo, bg=self.text_bg)
        self.text_screen.grid(column=1, row=1)
        self.iter_times.append(time.time())
        self.h = 0
        self.i = 0
        self.j = 0
        self.w = 0

    def end_game(self):
        self.finish_time = time.time()
        self.text_mask = Image.new('L', (400, 400))
        self.mdr = ImageDraw.Draw(self.text_mask)
        self.font = ImageFont.truetype('ebrima', 25)
        game_summary = f' Your scores: \nwords correct: {self.correct_words},'\
                       f' \ncharacters correct: {self.correct_chars}'\
                       f'\n\n Your misses: \nwords incorrect: {self.incorrect_words},' \
                       f' \ncharacters incorrect: {self.incorrect_chars}'\
                       f'\nTotal time taken: {round(self.finish_time - self.start_time, 2)}'\
                       f'\nWords per minute: {self.correct_words / round(self.finish_time-self.start_time,2)/60}'
        self.mdr.text(text=game_summary, xy=(0, 0),
                      fill="#77ffff", font=self.font,)
        self.gameImg = Image.open('stars.jpg')
        self.gameImg = self.gameImg.resize((400, 400))
        self.gameImg.paste(self.text_mask, (0, 0), self.text_mask)
        self.update_screen()
        self.words_shown = []
        self.game_running = False



window = Tk()
SpeedTest(window)
window.mainloop()
