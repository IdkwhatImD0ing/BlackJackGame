'''
Created on 6 February 2019; Last edited on 15 February 2019

@author: Bill Zhang
'''
from card import Card
from cards import Cards
from player import Player
from gui import Blackjack
import random
import tkinter as tk


# make a BlackjackCard Class inherit from Card
class BlackjackCard(Card):
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


def BlackjackGame():

    # Player and Dealer objects are created
    dealer = BlackjackPlayer("Dealer", 1)
    player = BlackjackPlayer("Player", 1)
    playerScore = 0
    dealerScore = 0
    deck = Cards()  # Empty deck of cards is created
    # add the 52-cards and shuffle

    # Beginning of the Game
    print("Welcome to the BackJack!")
    playerName = input("What's your name, gamer?")
    print("Hello, ", playerName + "!")
    rounds = input("How many rounds would you like to play?")
    if rounds not in "1234567890":
        Round = False
        rounds = input("Please give a positive integer number.")
    while Round == False:
        if rounds not in "1234567890" or rounds == '':
            rounds = input("Please give a positive integer number.")
        else:
            Round = True
    print("*****Shuffling Deck*****")
    blackjackDeck = BlackjackHand(
    )  # Make a deck and add all the cards into it. Idk if its already done or not
    blackjackDeck.createDeck()
    blackjackDeck.shuffle()  # Same I dont know if this will work for the deck
    playerHand = BlackjackHand()
    dealerhand = BlackjackHand()

    # Game proceeds with "rounds" amount of rounds
    for x in range(int(rounds)):
        playerRound = True
        dealerRound = True
        playerHandValue = 0
        dealerHandValue = 0
        print("Starting the Game now...")
        print("[  Round   ", x + 1, " ]", "Score: Dealer ", dealerScore,
              " Vs ", playerName, " ", playerScore)
        dealer.introduce()
        for x in range(2):
            card = blackjackDeck.deal()
            player.addCard(card)
            playerHandValue += card.getValue()
        card = blackjackDeck.deal()
        card2 = blackjackDeck.deal()
        dealer.addCard(card)
        dealer.addCard(card2)
        dealerHandValue += card.getValue()
        print(playerName + "'s hand ", player.hand, "Value =", playerHandValue)
        print("Dealer's hand ", card, "???")

        # Blackjack Scenario (If either player gets a Blackjack)
        if playerHandValue == 21 and dealerHandValue != 21:
            print("YOU GOT A BLACKJACK!")
            playerRound = False
            dealerRound = False
        if dealerHandValue == 21 and playerHandValue != 21:
            print("The Dealer got a Blackjack!")
            playerRound = False
            dealerRound = False
        if playerHandValue == 21 and dealerHandValue == 21:
            print("Both players got a Blackjack! It's a Tie!!!")
            playerRound = False
            dealerRound = False

        # Normal Scenario, Turn: Player (no natural Blackjack)
        while playerRound == True:
            playerhit = input("Would you like to hit? ( y/n )")
            if playerhit == "y":
                print("Player Hit!")
                card = blackjackDeck.deal()
                player.addCard(card)
                playerHandValue += card.getValue()
                print(playerName + "'s hand ", player.hand, "Value = ",
                      playerHandValue)
            elif playerhit == "n":
                playerRound = False
            if playerHandValue > 21:
                playerRound = False
                dealerRound = False

        # Normal Scenario, Turn: Dealer (after Player either Stands or Busts)
        while dealerRound == True:
            print("Dealer Hand ", dealer.hand)
            if dealerHandValue < 17:
                print("Dealer Hit")
                card = blackjackDeck.deal()
                dealer.addCard(card)
                dealerHandValue += card.getValue()
                print("Dealer's hand ", dealer.hand, "Value = ",
                      dealerHandValue)
            elif dealerHandValue > 21:
                dealerRound = False
            else:
                dealerRound = False

        # Ending message when determining the winner of the current round
        if playerHandValue > 21:
            print(playerName + " busts! They lose!")
            print("Dealer Wins!")
            dealerScore += 1
        elif dealerHandValue > 21:
            print("Dealer busts! They lose!")
            print(playerName + " Wins!")
            playerScore += 1
        elif playerHandValue > dealerHandValue:
            print(playerName + " Wins!")
            print("Dealer Loses!")
            playerScore += 1
        elif dealerHandValue > playerHandValue:
            print("Dealer Wins!")
            print(playerName + " Loses!")
            dealerScore += 1
        elif dealerHandValue == playerHandValue:
            print("It's a Tie!!!")

        # Hands are reset
        player.tossHand()
        dealer.tossHand()

    # Total number of wins for each player are tallied after all rounds are over
    print("-----------------------------------")
    print("! Final Score: {} ({}) vs Dealer ({}) !".format(
        playerName, str(playerScore), str(dealerScore)))
    #print("! Final Score", playerName, playerScore, "vs Dealer", dealerScore, " !")
    print("-----------------------------------")
    if playerScore == dealerScore:
        print("It's a Tie!")
    elif playerScore > dealerScore:
        print("Congrats! " + playerName + " Wins.")
    elif dealerScore > playerScore:
        print("Dealer Wins.")


BlackjackGame()