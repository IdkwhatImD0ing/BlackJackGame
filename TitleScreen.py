'''
@author: Bill Zhang
'''
import tkinter as tk
from SinglePlayer import game
from Autoplay import autoplay
from tkinter import PhotoImage
from tkinter import Canvas
from tkinter import simpledialog
from SingleBet import bet
from CampaignSelection import campaignSelect
from BetCampaignSelection import betCampaignSelect
import settings
from tkinter import messagebox


class title:
    BACKGROUND = 'darkgreen'

    def __init__(self):  #Loads the window and several key variables

        self.window = tk.Tk()
        self.window.resizable(width=False, height=False)

        settings.player = simpledialog.askstring(
            "What is your name?",
            "Please type your name below>")  #Gets the name
        if settings.player == None or settings.player == "":
            settings.player = "Player"

        self.window.title("Blackjack")
        self.window['bg'] = title.BACKGROUND
        self.background_image = PhotoImage(file=r"Images\Blackjack.png")

        self.title_frame = self.create_frame()

        self.canvas = Canvas(self.title_frame,
                             width=800,
                             height=480,
                             bg='green')
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0,
                                 0,
                                 image=self.background_image,
                                 anchor='nw')

        self.title, self.subtitle, self.single, self.singlebet = self.create_text(
        )

        self.single1_Button, self.single2_Button, self.single3_Button, self.auto_Button, self.singlebet1_Button, self.singlebet2_Button, self.singlebet3_Button, self.campaign_Button, self.betCampaign_Button, self.unlock_Button = self.create_widgets(
        )

        self.set_callbacks()

    def create_text(self):  #All the text in the window
        title = self.canvas.create_text(
            400,
            160,
            text="Welcome to the game of Blackjack!!",
            font=('ALGERIAN', 28),
            fill='white')
        subtitle = self.canvas.create_text(400,
                                           220,
                                           text="Select the game mode below:",
                                           font=('ALGERIAN', 14),
                                           fill='white')
        single = self.canvas.create_text(260,
                                         270,
                                         text="Single player modes:",
                                         font=('ALGERIAN', 14),
                                         fill='white')
        singlebet = self.canvas.create_text(
            260,
            310,
            text="Single player betting modes:",
            font=('ALGERIAN', 14),
            fill='white')
        return title, subtitle, single, singlebet

    def create_frame(self):  #Frame of the window

        title_frame = tk.Frame(self.window,
                               bg=title.BACKGROUND,
                               width=800,
                               height=480)
        title_frame.pack_propagate(0)
        title_frame.pack()

        return title_frame

    def create_widgets(self):  #All the buttons in the window
        #background_label = tk.Label(self.title_frame, image=self.background_image)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)

        single1_Button = tk.Button(self.title_frame,
                                   text="Easy",
                                   bg='lightgray')
        single1_Button.place(x=380, y=260, relwidth=0.08, relheight=0.05)

        single2_Button = tk.Button(self.title_frame,
                                   text="Normal",
                                   bg='lightgray')
        single2_Button.place(x=460, y=260, relwidth=0.08, relheight=0.05)

        single3_Button = tk.Button(self.title_frame,
                                   text="Hard",
                                   bg='lightgray')
        single3_Button.place(x=540, y=260, relwidth=0.08, relheight=0.05)

        singlebet1_Button = tk.Button(self.title_frame,
                                      text="Easy",
                                      bg='lightgray')
        singlebet1_Button.place(x=420, y=300, relwidth=0.08, relheight=0.05)

        singlebet2_Button = tk.Button(self.title_frame,
                                      text="Normal",
                                      bg='lightgray')
        singlebet2_Button.place(x=500, y=300, relwidth=0.08, relheight=0.05)

        singlebet3_Button = tk.Button(self.title_frame,
                                      text="Hard",
                                      bg='lightgray')
        singlebet3_Button.place(x=580, y=300, relwidth=0.08, relheight=0.05)

        campaign_Button = tk.Button(self.title_frame,
                                    text="Normal Campaign!",
                                    bg='lightgray')
        campaign_Button.place(x=320, y=340, relwidth=0.2, relheight=0.05)

        betCampaign_Button = tk.Button(self.title_frame,
                                       text="Hard Campaign!",
                                       bg='lightgray')
        betCampaign_Button.place(x=320, y=380, relwidth=0.2, relheight=0.05)

        auto_Button = tk.Button(self.title_frame,
                                text="Auto-Play",
                                bg='lightgray')
        auto_Button.place(x=320, y=420, relwidth=0.2, relheight=0.05)

        unlock_Button = tk.Button(self.title_frame,
                                  text="Unlock all missions",
                                  bg='lightgray')
        unlock_Button.place(x=320, y=460, relwidth=0.2, relheight=0.05)

        return single1_Button, single2_Button, single3_Button, auto_Button, singlebet1_Button, singlebet2_Button, singlebet3_Button, campaign_Button, betCampaign_Button, unlock_Button

    def set_callbacks(self):  #Binds commands to the buttons
        self.single1_Button['command'] = self.Easy
        self.single2_Button['command'] = self.Normal
        self.single3_Button['command'] = self.Hard
        self.singlebet1_Button['command'] = self.betEasy
        self.singlebet2_Button['command'] = self.betNormal
        self.singlebet3_Button['command'] = self.betHard
        self.campaign_Button['command'] = self.campaign
        self.betCampaign_Button['command'] = self.betCampaign
        self.auto_Button['command'] = self.Autoplay
        self.unlock_Button['command'] = self.unlock


#The following functions each represent one game mode with its accompanying variables

    def Easy(self):
        settings.difficulty = 9
        self.window.destroy()
        program = game()
        program.window.mainloop()

    def Normal(self):
        settings.difficulty = 13
        self.window.destroy()
        program = game()
        program.window.mainloop()

    def Hard(self):
        settings.difficulty = 17
        self.window.destroy()
        program = game()
        program.window.mainloop()

    def betEasy(self):
        settings.difficulty = 9
        self.window.destroy()
        program = bet()
        program.window.mainloop()

    def betNormal(self):
        settings.difficulty = 13
        self.window.destroy()
        program = bet()
        program.window.mainloop()

    def betHard(self):
        settings.difficulty = 17
        self.window.destroy()
        program = bet()
        program.window.mainloop()

    def campaign(self):  #Opens a campaign select screen
        self.window.destroy()
        program = campaignSelect()
        program.window.mainloop()

    def betCampaign(self):  #Opens the  hard campaign select screen
        self.window.destroy()
        program = betCampaignSelect()
        program.window.mainloop()

    def Autoplay(self):  #Autoplay Mode
        self.window.destroy()
        program = autoplay()
        program.window.mainloop()

    def unlock(self):  #Used for testing purposes to unlock all campaign levels
        for x in range(0, 5):
            settings.campaignTracker[x] = True
            settings.betCampaignTracker[x] = True
        messagebox.showinfo("Security Breach!!!",
                            "All mission access granted!")
