'''
Created on 6 February 2019; Last edited on 4 March 2019

@author: Bill Zhang
'''

from card import Card
from cards import Cards
from player import Player
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import simpledialog
from tkinter import scrolledtext
from time import sleep
import winsound

#Final Version of the first version of the GUi


def main():
    program = game()

    program.window.mainloop()


class BlackjackCard(Card):

    SUIT = ['H', 'D', 'S', 'C']
    RANK = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.image = PhotoImage(file=r"Images\{}{}.png".format(rank, suit))

    def getValue(
        self
    ):  # Changes value for Ace to 11; changes value for Face Cards to 10
        if self.rank == 'A':
            return (11)
        elif self.rank == 'J':
            return (10)
        elif self.rank == 'Q':
            return (10)
        elif self.rank == 'K':
            return (10)
        elif self.rank in '23456789' or self.rank == '10':
            return (int(self.rank))
        else:
            raise ValueError('{} is of unknown value'.format(
                self.rank))  # Returns an error for any invalid cards


class BlackjackHand(Cards):
    def createDeck(self):  # Creates a deck of 52 cards
        for rank in BlackjackCard.RANK:
            for suit in BlackjackCard.SUIT:
                self.add(BlackjackCard(rank, suit))

    def getTotalWithAce(
        self
    ):  # Applies a value of either 11 or 1 to Aces; all other cards have their respective values
        total = 0
        for card in self:
            if (card.getValue() == 11 and (total + 11) > 21):
                total += 1
            elif (card.getValue() == 11 and (total + 11) <= 21):
                total += 11
            else:
                total += card.getValue()
        return total

    def bust(self):  # Command called to see if Player/Dealer busts
        if (self.getTotalWithAce() > 21):
            return True
        return False


class BlackjackPlayer(Player):
    pass


class BlackjackDealer(Cards):
    pass


class game:
    HUD_BACKGROUND = 'lightgray'
    COUNTER_BACKGROUND = 'lightgray'
    NUM_CARDS_ACROSS = 5
    NUM_CARDS_DOWN = 2

    def __init__(self):

        self.music = random.randrange(0, 28)
        winsound.PlaySound(r'Sounds\{}.wav'.format(self.music),
                           winsound.SND_ALIAS | winsound.SND_ASYNC)

        self.window = tk.Tk()
        self.window.title("Blackjack")
        self.window['bg'] = 'lightgray'

        messagebox.showinfo("Copyright",
                            "© 2019 Bill Zhang No Rights Reserved")

        self.playerName = simpledialog.askstring("Input",
                                                 "What is your name?",
                                                 parent=self.window)
        if self.playerName == "" or self.playerName == None:
            self.playerName = "Player"

        self.playerRound = False
        self.dealerRound = False
        self.canRun = True
        self.playerHandValue = 0
        self.dealerHandValue = 0
        self.blackjackDeck = BlackjackHand()
        self.blackjackDeck.createDeck()
        self.hit = 0

        self.blank = PhotoImage(file=r"Images\purple_back.png")

        self.game_frame, self.hud_frame, self.counter_frame = self.create_frame(
        )

        self.card_labels = self.originalCards()

        self.playerPoints = 0
        self.dealerPoints = 0
        self.roundCount = 0

        self.playerCounter, self.dealerCounter, self.start_button, self.quit_button, self.hit_button, self.end_button, self.deal_button, self.rules_button = self.create_hud_widgets(
        )

        self.playerHandCounter, self.dealerHandCounter = self.create_game_widgets(
        )

        self.set_callbacks()

        self.dealer = BlackjackPlayer("Dealer", 1)
        self.player = BlackjackPlayer("Player", 1)

        self.game_is_running = False

        if messagebox.askyesno("Rules", "Do you know the rules?") == False:
            messagebox.showinfo(
                "Rules",
                "The standard 52-card pack is used, but in most casinos several decks of cards are shuffled together. In this game we will be using the standard deck. The object of the game is for the participant to attempt to beat the dealer by getting a count as close to 21 as possible, without going over 21. It is up to each individual player if an ace is worth 1 or 11. Face cards are 10 and any other card is its pip value. Before the deal begins, each player places a bet, in chips, in front of him in the designated area. Minimum and maximum limits are established on the betting, and the general limits are from $2 to $500. When all the players have placed their bets, the dealer gives one card face up to each player in rotation clockwise, and then one card face up to himself. Another round of cards is then dealt face up to each player, but the dealer takes his second card face down. Thus, each player except the dealer receives two cards face up, and the dealer receives one card face up and one card face down. If a player's first two cards are an ace and a 'ten-card' (a picture card or 10), giving him a count of 21 in two cards, this is a natural or 'blackjack.'  The player automatically wins.The player to the left goes first and must decide whether to 'stand' (not ask for another card) or 'hit' (ask for another card in an attempt to get closer to a count of 21, or even hit 21 exactly). Thus, a player may stand on the two cards originally dealt him, or he may ask the dealer for additional cards, one at a time, until he either decides to stand on the total (if it is 21 or under), or goes 'bust' (if it is over 21). In the latter case, the player loses. When the dealer has served every player, his face-down card is turned up. If the total is 17 or more, he must stand. If the total is 16 or under, he must take a card. He must continue to take cards until the total is 17 or more, at which point the dealer must stand. If the dealer has an ace, and counting it as 11 would bring his total to 17 or more (but not over 21), he must count the ace as 11 and stand. The dealer's decisions, then, are automatic on all plays, whereas the player always has the option of taking one or more cards. "
            )
        messagebox.showinfo("Welcome to Blackjack!!!",
                            "Click the Start button to start the game!")

    def create_frame(self):
        game_frame = tk.Frame(self.window, bg='green', width=1000, height=500)
        game_frame.grid(row=1, column=1)

        hud_frame = tk.Frame(self.window,
                             bg='lightblue',
                             width=1000,
                             height=100)
        hud_frame.grid(row=5, column=1)

        counter_frame = tk.Frame(self.window,
                                 bg='white',
                                 width=1000,
                                 height=100)
        counter_frame.grid(row=0, column=1)

        return game_frame, hud_frame, counter_frame

    def create_game_widgets(self):
        playerHandLabel = tk.Label(self.counter_frame,
                                   text="{}'s Hand Value:".format(
                                       self.playerName),
                                   bg=game.COUNTER_BACKGROUND)
        playerHandLabel.pack(side="left", fill=tk.Y, expand=True)

        playerHandCounter = tk.Label(self.counter_frame,
                                     text=str(self.playerHandValue),
                                     bg=game.COUNTER_BACKGROUND)
        playerHandCounter.pack(side="left", fill=tk.Y, expand=True)

        dealerHandCounter = tk.Label(self.counter_frame,
                                     text=str(self.dealerHandValue),
                                     bg=game.COUNTER_BACKGROUND)
        dealerHandCounter.pack(side="right", fill=tk.Y, expand=True)

        dealerHandLabel = tk.Label(self.counter_frame,
                                   text="Dealer's Hand Value:",
                                   bg=game.COUNTER_BACKGROUND)
        dealerHandLabel.pack(side="right", fill=tk.Y, expand=True)

        return playerHandCounter, dealerHandCounter

    def create_hud_widgets(self):
        rules_button = tk.Button(self.hud_frame,
                                 text="Rules",
                                 bg='darkblue',
                                 fg='white')
        rules_button.pack(side='left', fill=tk.Y, expand=True, ipadx=10)

        spacer = tk.Label(self.hud_frame, text=" ", bg='lightgray')
        spacer.pack(side="left", fill=tk.Y, expand=True)

        playerLabel = tk.Label(self.hud_frame,
                               text="{}'s points:".format(self.playerName),
                               bg=game.HUD_BACKGROUND)
        playerLabel.pack(side="left", fill=tk.Y, expand=True)

        playerCounter = tk.Label(self.hud_frame,
                                 text=str(self.playerPoints),
                                 bg=game.HUD_BACKGROUND)
        playerCounter.pack(side="left", fill=tk.Y, expand=True)

        spacer = tk.Label(self.hud_frame, text="", bg=game.HUD_BACKGROUND)
        spacer.pack(side="right", fill=tk.Y, expand=True)

        dealerLabel = tk.Label(self.hud_frame,
                               text="Dealer points:",
                               bg=game.HUD_BACKGROUND)
        dealerLabel.pack(side="left", fill=tk.Y, expand=True)

        dealerCounter = tk.Label(self.hud_frame,
                                 text=str(self.dealerPoints),
                                 bg=game.HUD_BACKGROUND)
        dealerCounter.pack(side="left", fill=tk.Y, expand=True)

        spacer = tk.Label(self.hud_frame, text=" ", bg=game.HUD_BACKGROUND)
        spacer.pack(side="right", fill=tk.Y, expand=True)

        quit_button = tk.Button(self.hud_frame, text="Quit", bg='red')
        quit_button.pack(side="right", fill=tk.Y, expand=True, ipadx=10)

        spacer = tk.Label(self.hud_frame, text=" ", bg=game.HUD_BACKGROUND)
        spacer.pack(side="right", fill=tk.Y, expand=True)

        start_button = tk.Button(self.hud_frame, text="Start", bg='green')
        start_button.pack(side="right", fill=tk.Y, expand=True, ipadx=10)

        spacer = tk.Label(self.hud_frame, text="", bg=game.HUD_BACKGROUND)
        spacer.pack(side="right", fill=tk.Y, expand=True)

        end_button = tk.Button(self.hud_frame, text="Stand")
        end_button.pack(side="right", fill=tk.Y, expand=True, ipadx=30)

        spacer = tk.Label(self.hud_frame, text="", bg=game.HUD_BACKGROUND)
        spacer.pack(side="right", fill=tk.X, expand=True)

        hit_button = tk.Button(self.hud_frame, text="Hit")
        hit_button.pack(side="right", fill=tk.Y, expand=True, ipadx=20)

        spacer = tk.Label(self.hud_frame, text="", bg=game.HUD_BACKGROUND)
        spacer.pack(side="right", fill=tk.Y, expand=True)

        deal_button = tk.Button(self.hud_frame, text="Deal")
        deal_button.pack(side="right", fill=tk.Y, expand=True, ipadx=20)

        spacer = tk.Label(self.hud_frame, text="", bg=game.HUD_BACKGROUND)
        spacer.pack(side="right", fill=tk.Y, expand=True)

        return playerCounter, dealerCounter, start_button, quit_button, hit_button, end_button, deal_button, rules_button

    def set_callbacks(self):
        self.start_button['command'] = self.start
        self.quit_button['command'] = self.quit
        self.hit_button['command'] = self.playerHit
        self.end_button['command'] = self.end
        self.deal_button['command'] = self.deal
        self.rules_button['command'] = self.rules

    def start(self):
        self.dealerPoints = 0
        self.playerPoints = 0
        self.roundCount = 0
        if self.start_button['text'] == "Start":
            self.game_is_running = True
            self.Rounds = simpledialog.askinteger(
                "Input",
                "How many rounds would you like to play?",
                parent=self.window)
            self.start_button['text'] = "Stop"
            if self.Rounds == None or self.Rounds == '':
                self.game_is_running = False
                self.start_button['text'] = "Start"
                messagebox.showerror(
                    "Try Again",
                    "Please click start again and type in the number of rounds you want to play."
                )
            else:
                messagebox.showinfo(
                    "***SHUFFLING THE DECK***",
                    "Press the deal button to start the round!")
            print("Start button hit")

            self.playerCounter['text'] = "0"
            self.dealerCounter['text'] = "0"

        else:
            if self.game_is_running == True:
                if messagebox.askyesno(
                        "Stopping the Game",
                        "Are you sure you want to stop the game?") == True:
                    self.game_is_running = False
                    self.start_button['text'] = "Start"

                    for r in range(game.NUM_CARDS_DOWN):
                        for c in range(game.NUM_CARDS_ACROSS):
                            the_label = self.card_labels[r][c]
                            the_label['image'] = self.blank
                    self.hit = 0
                    self.canRun = True
            else:
                self.start_button['text'] = "Start"
                for r in range(game.NUM_CARDS_DOWN):
                    for c in range(game.NUM_CARDS_ACROSS):
                        the_label = self.card_labels[r][c]
                        the_label['image'] = self.blank
                self.hit = 0
                self.canRun = True

    def quit(self):
        print("Quit button hit")
        really_quit = messagebox.askyesno("Quiting?",
                                          "Do you really want to quit?")
        if really_quit:
            self.window.destroy()

    def rules(self):
        messagebox.showinfo(
            "Rules",
            "The standard 52-card pack is used, but in most casinos several decks of cards are shuffled together. In this game we will be using the standard deck. The object of the game is for the participant to attempt to beat the dealer by getting a count as close to 21 as possible, without going over 21. It is up to each individual player if an ace is worth 1 or 11. Face cards are 10 and any other card is its pip value. Before the deal begins, each player places a bet, in chips, in front of him in the designated area. Minimum and maximum limits are established on the betting, and the general limits are from $2 to $500. When all the players have placed their bets, the dealer gives one card face up to each player in rotation clockwise, and then one card face up to himself. Another round of cards is then dealt face up to each player, but the dealer takes his second card face down. Thus, each player except the dealer receives two cards face up, and the dealer receives one card face up and one card face down. If a player's first two cards are an ace and a 'ten-card' (a picture card or 10), giving him a count of 21 in two cards, this is a natural or 'blackjack.'  The player automatically wins.The player to the left goes first and must decide whether to 'stand' (not ask for another card) or 'hit' (ask for another card in an attempt to get closer to a count of 21, or even hit 21 exactly). Thus, a player may stand on the two cards originally dealt him, or he may ask the dealer for additional cards, one at a time, until he either decides to stand on the total (if it is 21 or under), or goes 'bust' (if it is over 21). In the latter case, the player loses. When the dealer has served every player, his face-down card is turned up. If the total is 17 or more, he must stand. If the total is 16 or under, he must take a card. He must continue to take cards until the total is 17 or more, at which point the dealer must stand. If the dealer has an ace, and counting it as 11 would bring his total to 17 or more (but not over 21), he must count the ace as 11 and stand. The dealer's decisions, then, are automatic on all plays, whereas the player always has the option of taking one or more cards. "
        )

    def originalCards(self):
        card_labels = []
        for r in range(game.NUM_CARDS_DOWN):
            row_of_labels = []
            for c in range(game.NUM_CARDS_ACROSS):
                card_label = tk.Label(self.game_frame, image=self.blank)
                card_label.grid(row=r, column=c)

                row_of_labels.append(card_label)
            card_labels.append(row_of_labels)

        return card_labels

    def dealerHit(self):

        card = self.blackjackDeck.deal()
        self.dealerHandValue += card.getValue()
        self.dealerHandCounter['text'] = str(
            int(self.dealerHandCounter['text']) + card.getValue())
        self.dealer.addCard(card)
        the_label = self.card_labels[0][self.hit + 2]
        the_label['image'] = card.image
        self.hit += 1

    def BjGame(self):
        playerName = 'Bill'  # simpledialog.askstring("Input", "What is your name?", parent=self.window)
        #messagebox.showinfo("Welcome","Welcome " + playerName)
        rounds = 1  #simpledialog.askinteger("Input", "How many rounds would you like to play?", parent=self.window)
        #messagebox.showinfo("Shuffling","***Shuffling the deck***")
        blackjackDeck.shuffle()

        for x in range(rounds):
            playerRound = True
            dealerRound = True
            #  messagebox.showinfo("Game Start!","Round: " + str(x+1))
            playerHandValue = 0
            dealerHandValue = 0\

            if playerHandValue == 21 and dealerHandValue != 21:
                messagebox.showinfo(
                    "BLACKJACK", "{} got a blackjack.".format(self.playerName))
                playerRound = False
                dealerRound = False
            if dealerHandValue == 21 and playerHandValue != 21:
                messagebox.showinfo("BLACKJACK", "Dealer got a blackjack.")
                playerRound = False
                dealerRound = False
            if playerHandValue == 21 and dealerHandValue == 21:
                messagebox.showinfo("BLACKJACK",
                                    "Both players got a blackjack.")
                playerRound = False
                dealerRound = False

        #while playerRound:

            sleep(20)

    def deal(self):

        if self.game_is_running == True and self.canRun == True:
            self.playerHandValue = 0
            self.dealerHandValue = 0
            self.playerHandCounter['text'] = '0'
            self.dealerHandCounter['text'] = '???'
            self.canRun = False
            self.blackjackDeck.createDeck()
            self.blackjackDeck.shuffle()
            for time in range(2):
                card = self.blackjackDeck.deal()
                self.playerHandValue += card.getValue()
                self.playerHandCounter['text'] = str(
                    int(self.playerHandCounter['text']) + card.getValue())
                self.player.addCard(card)
                the_label = self.card_labels[1][time]
                the_label['image'] = card.image

            card = self.blackjackDeck.deal()
            self.dealer.addCard(card)
            the_label = self.card_labels[0][0]
            the_label['image'] = card.image
            card2 = self.blackjackDeck.deal()
            self.permanent = card2
            self.dealer.addCard(card2)
            the_label = self.card_labels[0][1]
            the_label['image'] = self.blank

            self.constant1 = card
            self.constant2 = card2

            self.dealerHandValue += card.getValue()
            self.dealerHandValue += card2.getValue()

            for x in range(2):
                for y in range(3):
                    the_label = self.card_labels[x][2 + y]
                    the_label['image'] = self.blank

            self.hit = 0
            self.playerRound = True
            self.roundCount += 1

            if self.playerHandValue == 21 and self.dealerHandValue != 21:
                messagebox.showinfo("BLACKJACK", "You got blackjack!!!")
                playerRound = False
                dealerRound = False
                self.playerPoints += 1
                self.playerCounter['text'] = str(
                    int(self.playerCounter['text']) + 1)
                self.canRun = True
            if self.dealerHandValue == 21 and self.playerHandValue != 21:
                the_label = self.card_labels[0][1]
                the_label['image'] = self.permanent.image
                messagebox.showinfo("BLACKJACK", "Dealer got blackjack!!!")
                playerRound = False
                dealerRound = False
                self.dealerPoints += 1
                self.dealerCounter['text'] = str(
                    int(self.dealerCounter['text']) + 1)
                self.canRun = True
            if self.playerHandValue == 21 and self.dealerHandValue == 21:
                messagebox.showinfo("BLACKJACK",
                                    "Both players got blackjack, its a tie.")
                playerRound = False
                dealerRound = False
                self.canRun = True

        else:
            if self.game_is_running == False:
                messagebox.showerror("Error", "Game has not started yet.")
            elif self.canRun == False:
                messagebox.showerror("Error", "Round is not yet over.")

    def playerHit(self):
        if self.game_is_running == True and self.playerRound == True:
            if self.hit < 3:
                card = self.blackjackDeck.deal()
                self.playerHandValue += card.getValue()
                self.playerHandCounter['text'] = str(
                    int(self.playerHandCounter['text']) + card.getValue())
                self.player.addCard(card)
                the_label = self.card_labels[1][self.hit + 2]
                the_label['image'] = card.image
                self.hit += 1

                if self.playerHandValue > 21:
                    messagebox.showinfo(
                        "Bust", "{} busts with {} points".format(
                            self.playerName, str(self.playerHandValue)))
                    self.dealerRound = False
                    self.playerRound = False
                    self.canRun = True
                    self.dealerPoints += 1
                    self.dealerCounter['text'] = str(
                        int(self.dealerCounter['text']) + 1)

                if self.Rounds == self.roundCount:
                    self.game_is_running = False
                    self.calculateScore()
                    messagebox.showinfo(
                        "Restart the game",
                        'Click the start button to start a new game!')

            else:
                messagebox.showerror("Error", "Maximum Hits Reached")
        else:
            if self.game_is_running == False:
                messagebox.showerror(
                    "Error",
                    "The game has not started yet. Click the start button to start the game."
                )
            elif self.playerRound == False:
                messagebox.showerror("Error", "It is not your turn.")

    def end(self):
        if self.game_is_running == True and self.playerRound == True and self.canRun == False:
            self.hit = 0
            self.playerRound = False
            self.dealerRound = True

            the_label = self.card_labels[0][1]
            the_label['image'] = self.permanent.image
            self.dealerHandCounter['text'] = '0'
            self.dealerHandCounter['text'] = str(
                int(self.dealerHandCounter['text']) +
                self.constant1.getValue())
            self.dealerHandCounter['text'] = str(
                int(self.dealerHandCounter['text']) +
                self.constant2.getValue())

            while self.dealerRound == True:
                if self.dealerHandValue < 17:
                    self.dealerHit()
                else:
                    self.dealerRound = False

            if self.playerHandValue > 21:
                messagebox.showinfo(
                    "Result", "{} Busts, Dealer Wins".format(self.playerName))
                self.dealerPoints += 1
                self.dealerCounter['text'] = str(
                    int(self.dealerCounter['text']) + 1)
            elif self.dealerHandValue > 21:
                messagebox.showinfo("Result", "Dealer Busts, Player Wins")
                self.playerPoints += 1
                self.playerCounter['text'] = str(
                    int(self.playerCounter['text']) + 1)
            elif self.playerHandValue > self.dealerHandValue:
                messagebox.showinfo("Result",
                                    "{} Wins".format(self.playerName))
                self.playerPoints += 1
                self.playerCounter['text'] = str(
                    int(self.playerCounter['text']) + 1)
            elif self.dealerHandValue > self.playerHandValue:
                messagebox.showinfo("Result", "Dealer Wins")
                self.dealerPoints += 1
                self.dealerCounter['text'] = str(
                    int(self.dealerCounter['text']) + 1)
            elif self.dealerHandValue == self.playerHandValue:
                messagebox.showinfo("Result", "It's a tie")
            self.canRun = True

            if self.Rounds == self.roundCount:
                self.game_is_running = False
                self.calculateScore()
        else:
            if self.game_is_running == False:
                messagebox.showerror(
                    "ERROR",
                    "Game has not started yet. Click the start button please.")
            elif self.playerRound == False:
                messagebox.showerror("Error", "It is not your turn yet.")
            elif self.canRun == True:
                messagebox.showerror("Error",
                                     "Round has ended. Please deal again.")

    def calculateScore(self):
        messagebox.showinfo(
            "Final Points", "! Final Score: {} ({}) vs Dealer ({}) !".format(
                self.playerName, str(self.playerPoints),
                str(self.dealerPoints)))
        if self.playerPoints == self.dealerPoints:
            messagebox.showinfo("Ending", 'Its a tie')
        elif self.playerPoints > self.dealerPoints:
            messagebox.showinfo(
                "Ending", "Congrats! {} wins with {} points.".format(
                    self.playerName, str(self.playerPoints)))
        elif self.dealerPoints > self.playerPoints:
            messagebox.showinfo("Ending", "Dealer Wins")


if __name__ == "__main__":
    main()