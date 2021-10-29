'''
@author: Bill Zhang
'''
import tkinter as tk
from tkinter import Canvas
from tkinter import PhotoImage
from BetCampaign import betCampaign
from tkinter import messagebox
import settings

#Bet Campaign selection screen with 5 Levels


class betCampaignSelect:
    BACKGROUND = 'darkgreen'

    def __init__(self):

        self.window = tk.Tk()
        self.window.resizable(width=False, height=False)

        self.window.title("Blackjack")
        self.window['bg'] = betCampaignSelect.BACKGROUND
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

        self.title = self.create_text()

        self.single1_Button, self.single2_Button, self.single3_Button, self.single4_Button, self.single5_Button = self.create_widgets(
        )

        self.set_callbacks()

        #Make Buttons green after completing level
        if settings.betCampaignTracker[0] == True:
            self.single1_Button.configure(bg='green')

        if settings.betCampaignTracker[1] == True:
            self.single2_Button.configure(bg='green')

        if settings.betCampaignTracker[2] == True:
            self.single3_Button.configure(bg='green')

        if settings.betCampaignTracker[3] == True:
            self.single4_Button.configure(bg='green')

        if settings.betCampaignTracker[4] == True:
            self.single5_Button.configure(bg='green')

    def create_text(self):
        title = self.canvas.create_text(400,
                                        180,
                                        text="Choose the level below:",
                                        font=('ALGERIAN', 28),
                                        fill='white')
        return title

    def create_frame(self):

        title_frame = tk.Frame(self.window,
                               bg=betCampaignSelect.BACKGROUND,
                               width=800,
                               height=480)
        title_frame.pack_propagate(0)
        title_frame.pack()

        return title_frame

    def create_widgets(self):
        single1_Button = tk.Button(self.title_frame,
                                   text="Mission 1",
                                   bg='lightgray')
        single1_Button.place(x=150, y=280, relwidth=0.08, relheight=0.05)

        single2_Button = tk.Button(self.title_frame,
                                   text="Mission 2",
                                   bg='lightgray')
        single2_Button.place(x=260, y=280, relwidth=0.08, relheight=0.05)

        single3_Button = tk.Button(self.title_frame,
                                   text="Mission 3",
                                   bg='lightgray')
        single3_Button.place(x=370, y=280, relwidth=0.08, relheight=0.05)

        single4_Button = tk.Button(self.title_frame,
                                   text="Mission 4",
                                   bg='lightgray')
        single4_Button.place(x=480, y=280, relwidth=0.08, relheight=0.05)

        single5_Button = tk.Button(self.title_frame,
                                   text="Mission 5",
                                   bg='lightgray')
        single5_Button.place(x=590, y=280, relwidth=0.08, relheight=0.05)

        return single1_Button, single2_Button, single3_Button, single4_Button, single5_Button  #background_label

    def set_callbacks(self):
        self.single1_Button['command'] = self.Level1
        self.single2_Button['command'] = self.Level2
        self.single3_Button['command'] = self.Level3
        self.single4_Button['command'] = self.Level4
        self.single5_Button['command'] = self.Level5

    def Level1(self):
        settings.campaign = 1
        settings.campaignBoss = "Ariel"
        settings.country = "Canada"
        self.window.destroy()
        program = betCampaign()
        program.window.mainloop()

    def Level2(self):
        settings.campaign = 2
        if settings.betCampaignTracker[1] == True:
            settings.campaignBoss = "Percy"
            settings.country = "United States"
            self.window.destroy()
            program = betCampaign()
            program.window.mainloop()
        else:
            messagebox.showerror("Access Denied",
                                 "Finish the previous mission first.")

    def Level3(self):
        settings.campaign = 3
        if settings.betCampaignTracker[2] == True:
            settings.campaignBoss = "Harry"
            settings.country = "England"
            self.window.destroy()
            program = betCampaign()
            program.window.mainloop()
        else:
            messagebox.showerror("Access Denied",
                                 "Finish the previous mission first.")

    def Level4(self):
        settings.campaign = 4
        if settings.betCampaignTracker[3] == True:
            settings.campaignBoss = "Zai"
            settings.country = "China"
            self.window.destroy()
            program = betCampaign()
            program.window.mainloop()
        else:
            messagebox.showerror("Access Denied",
                                 "Finish the previous mission first.")

    def Level5(self):
        settings.campaign = 5
        if settings.betCampaignTracker[4] == True:
            settings.campaignBoss = "Loki"
            settings.country = "Asgard"
            self.window.destroy()
            program = betCampaign()
            program.window.mainloop()
        else:
            messagebox.showerror("Access Denied",
                                 "Finish the previous mission first.")
