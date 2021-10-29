'''
Created on 6 February 2019; Last edited on 4 March 2019

@author: Bill Zhang
'''
import tkinter as tk
from SinglePlayer import game
from Autoplay import autoplay
from tkinter import PhotoImage


class title:
    BACKGROUND = 'darkgreen'

    def __init__(self):

        self.window = tk.Tk()

        self.window.title("Blackjack")
        self.window['bg'] = title.BACKGROUND
        self.background_image = PhotoImage(file=r"Images\Blackjack.png")
        self.title_frame = self.create_frame()

        self.background_label, self.titleLabel, self.single_Button, self.auto_Button = self.create_widgets(
        )
        self.set_callbacks()

    def create_frame(self):

        title_frame = tk.Frame(self.window,
                               bg=title.BACKGROUND,
                               width=715,
                               height=480)
        title_frame.pack_propagate(0)
        title_frame.pack()

        return title_frame

    def create_widgets(self):
        background_label = tk.Label(self.title_frame,
                                    image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        spacer = tk.Label(self.title_frame, text=" ", bg=title.BACKGROUND)
        spacer.config(font=('arial', 80))
        spacer.pack(side="top", fill=tk.Y)

        titleLabel = tk.Label(self.title_frame,
                              text="Welcome To the Game of Blackjack!",
                              fg='white')
        titleLabel.config(font=('ALGERIAN', 28))
        titleLabel.pack(side='top')

        spacer = tk.Label(self.title_frame, text=" ", bg=title.BACKGROUND)
        spacer.config(font=('arial', 10))
        spacer.pack(side='top', fill=tk.Y)

        titleLabel = tk.Label(
            self.title_frame,
            text="Select the game mode you want to play below:",
            bg=title.BACKGROUND,
            fg='white')
        titleLabel.config(font=('ALGERIAN', 12))
        titleLabel.pack(side='top')

        spacer = tk.Label(self.title_frame, text=" ", bg=title.BACKGROUND)
        spacer.config(font=('arial', 40))
        spacer.pack(side='top', fill=tk.Y)

        single_Button = tk.Button(self.title_frame,
                                  text="Single Player",
                                  bg='lightgray')
        single_Button.pack(side='top', ipadx=50)

        spacer = tk.Label(self.title_frame, text=" ", bg=title.BACKGROUND)
        spacer.config(font=('arial', 20))
        spacer.pack(side='top', fill=tk.Y)

        auto_Button = tk.Button(self.title_frame,
                                text="Auto-Play",
                                bg='lightgray')
        auto_Button.pack(side='top', ipadx=50)

        return background_label, titleLabel, single_Button, auto_Button

    def set_callbacks(self):
        self.single_Button['command'] = self.SinglePlayer
        self.auto_Button['command'] = self.Autoplay

    def SinglePlayer(self):
        self.window.destroy()
        program = game()
        program.window.mainloop()

    def Autoplay(self):
        self.window.destroy()
        program = autoplay()
        program.window.mainloop()