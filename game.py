'''
Created on 6 February 2019; Last edited on 4 March 2019

@author: Bill Zhang
'''
from card import Card
from cards import Cards
from player import Player
import card


# make a BlackjackCard Class inherit from Card
class BlackjackCard(Card):
    SUIT = ['H', 'D', 'S', 'C']
    RANK = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

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
        aces = 0
        for card in self.cards:
            total += card.getValue()
            if (card.getValue() == 11):
                aces += 1
            if (total > 21 and aces > 0):
                total -= 10
                aces -= 1
        return total

    def bust(self):  # Command called to see if Player/Dealer busts
        if (self.hand.getTotalWithAce() > 21):
            return True
        return False


class BlackjackPlayer(Player):
    def __init__(self, name, amount):
        self.name = name
        self.money = amount
        self.hand = BlackjackHand()

    def getMoney(self):
        return self.money

    def tossHand(self):
        self.hand = BlackjackHand()

    def askHit(self):  # Asks if the player wants to hit
        playerhit = input("Would you like to hit? (y/n)")
        if playerhit in "yY":
            return True
        elif playerhit in "nN":
            return False
        else:
            print("I didn't quite catch that. Please reply with 'y' or 'n'.")
            return (self.askHit())

    def changeMoney(self, num):
        self.money += num


class BlackjackDealer(BlackjackPlayer):
    def askHit(self):  # Dealer automatically hits if its total is less than 17
        if (self.hand.getTotalWithAce() < 17):
            return True
        else:
            return False


def BlackjackGame():
    # Player and Dealer objects are created
    print("Welcome to the BackJack!")
    playerName = input("What's your name, gamer?")
    print("Hello, ", playerName + "!")
    dealer = BlackjackDealer("Dealer", 1)
    player = BlackjackPlayer(playerName, 100)
    playerScore = 0
    dealerScore = 0

    # Beginning of the Game
    rounds = input("How many rounds would you like to play?"
                   )  # This segmen9t determines how many rounds are played
    if rounds not in "1234567890":
        Round = False
        rounds = input("Please give a positive integer number.")
    else:
        Round = True
    while Round == False:
        if rounds not in "1234567890" or rounds == '':
            rounds = input("Please give a positive integer number.")
        else:
            Round = True

    Round = False
    bettingGame = input(
        "Do you want to bet virtual money during this game? You will start with 100G. (Type 'y' or 'n')"
    )  # This segment asks the player if they want to bet money
    if bettingGame == 'y':
        hasBet = True
        canBet = True
        Round = True
    elif bettingGame == 'n':
        hasBet = False
        canBet = False
        Round = True
    else:
        Round = False
        bettingGame = input("Please type 'y' or 'n'.")
    while Round == False:
        if bettingGame == 'y':
            hasBet = True
            canBet = True
            Round = True
        elif bettingGame == 'n':
            hasBet = False
            canBet = False
            Round = True
        else:
            Round = False

    print("*****Shuffling Deck*****")
    blackjackDeck = BlackjackHand()  # Make a deck...
    blackjackDeck.createDeck()  # ...add all the cards into it...
    blackjackDeck.shuffle()  # ...and randomly shuffle it.

    # Game proceeds with "rounds" amount of rounds
    for x in range(int(rounds)):
        playerRound = True
        dealerRound = True
        print("Starting the Game now...")
        print("[Round {}]".format(str(x + 1)), "Score: Dealer", dealerScore,
              "Vs", playerName, playerScore)

        if (
                hasBet
        ):  # If Player is betting/has bet, their current balance is displayed
            print("{}'s balance: {}".format(playerName,
                                            str(player.getMoney())))
        if (canBet):  # If Player is betting, they are asked to place their bet
            betAmt = int(
                input(
                    "List the amount of G you want to bet. (Bet has to be at least than 10G, but cannot be more than your current balance)"
                ))
            while (betAmt < 10 or betAmt > player.getMoney()):
                if (betAmt < 10):
                    betAmt = int(
                        input(
                            "Your bet cannot be that low! (Bet has to be at least than 10G, but cannot be more than your current balance))"
                        ))
                else:
                    betAmt = int(
                        input(
                            "You don't have enough money to bet that much! (Bet has to be at least than 10G, but cannot be more than your current balance))"
                        ))

        for x in range(2):  # Hands are given to both players
            card = blackjackDeck.deal()
            player.addCard(card)
        card = blackjackDeck.deal()
        card2 = blackjackDeck.deal()
        dealer.addCard(card)
        dealer.addCard(card2)
        print(playerName + "'s hand", player.hand, "Value =",
              player.hand.getTotalWithAce())
        print("Dealer's hand [{} ???]".format(str(card)))

        # Blackjack Scenario (If either player gets a Blackjack)
        if player.hand.getTotalWithAce(
        ) == 21 and dealer.hand.getTotalWithAce() != 21:
            print("You got a Blackjack!")
            if (canBet):
                player.changeMoney((betAmt * 1.5) // 1)
            playerRound = False
            dealerRound = False
        elif player.hand.getTotalWithAce(
        ) != 21 and dealer.hand.getTotalWithAce() == 21:
            print("The Dealer got a Blackjack!")
            playerRound = False
            dealerRound = False
        elif player.hand.getTotalWithAce(
        ) == 21 and dealer.hand.getTotalWithAce() == 21:
            print("Both players got a Blackjack! It's a Tie!")
            playerRound = False
            dealerRound = False

        # Normal Scenario, Turn: Player (no natural Blackjack)
        while playerRound:
            playerhit = player.askHit()
            if (playerhit):
                print("Player Hit!")
                card = blackjackDeck.deal()
                player.addCard(card)
                print(playerName + "'s hand", player.hand, "Value =",
                      player.hand.getTotalWithAce())
            elif (playerhit != True):
                playerRound = False
            if player.hand.getTotalWithAce() > 21:
                playerRound = False
                dealerRound = False

        # Normal Scenario, Turn: Dealer (after Player either Stands or Busts)
        while dealerRound:
            print("Dealer Hand ", dealer.hand)
            dealerhit = dealer.askHit()
            while (dealerhit):
                print("Dealer Hit!")
                card = blackjackDeck.deal()
                dealer.addCard(card)
                print("Dealer's hand", dealer.hand, "Value =",
                      dealer.hand.getTotalWithAce())
                dealerhit = dealer.askHit()
            dealerRound = False

        # Ending message when determining the winner of the current round
        if player.hand.getTotalWithAce() > 21:
            print(playerName + " busts! They lose! The Dealer Wins!")
            if (canBet):
                player.changeMoney(-1 * betAmt)
            dealerScore += 1
        elif dealer.hand.getTotalWithAce() > 21:
            print("Dealer busts! They lose! {} Wins!".format(playerName))
            if (canBet):
                player.changeMoney(betAmt)
            playerScore += 1
        elif player.hand.getTotalWithAce() > dealer.hand.getTotalWithAce():
            print(playerName + " Wins! The Dealer Loses!")
            if (canBet):
                player.changeMoney(betAmt)
            playerScore += 1
        elif dealer.hand.getTotalWithAce() > player.hand.getTotalWithAce():
            print("The Dealer Wins! {} loses!".format(playerName))
            if (canBet):
                player.changeMoney(-1 * betAmt)
            dealerScore += 1
        elif dealer.hand.getTotalWithAce() == player.hand.getTotalWithAce():
            print("It's a Tie!!!")

        # Hands are reset; if the player has less than 10G in their balance they cannot bet anymore
        player.tossHand()
        dealer.tossHand()
        if (player.getMoney() < 10):
            canBet = False
            print(
                "Your balance is less than 10G, so you are now unable to bet. Sorry!"
            )

    # Total number of wins for each player are tallied after all rounds are over
    print("-----------------------------------")
    print("Final Score: {} ({}) vs Dealer ({})".format(playerName,
                                                       str(playerScore),
                                                       str(dealerScore)))
    #print("! Final Score", playerName, playerScore, "vs Dealer", dealerScore, " !")
    print("-----------------------------------")
    if playerScore == dealerScore:
        print("It's a Tie!")
    elif playerScore > dealerScore:
        print("Congratulations! " + playerName + " Wins.")
    elif dealerScore > playerScore:
        print("Dealer Wins.")
    if (hasBet):  # Prints out the Player's balance if they decided to bet
        print("{} ended with {}G.".format(playerName, str(player.getMoney())))


BlackjackGame()
'''
Created on 6 February 2019; Last edited on 4 March 2019

@author: Bill Zhang, Alec Chen
'''
from card import Card
from cards import Cards
from player import Player
import card


# make a BlackjackCard Class inherit from Card
class BlackjackCard(Card):
    SUIT = ['H', 'D', 'S', 'C']
    RANK = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

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
        aces = 0
        for card in self.cards:
            total += card.getValue()
            if (card.getValue() == 11):
                aces += 1
            if (total > 21 and aces > 0):
                total -= 10
                aces -= 1
        return total

    def bust(self):  # Command called to see if Player/Dealer busts
        if (self.hand.getTotalWithAce() > 21):
            return True
        return False


class BlackjackPlayer(Player):
    def __init__(self, name, amount):
        self.name = name
        self.money = amount
        self.hand = BlackjackHand()

    def getMoney(self):
        return self.money

    def tossHand(self):
        self.hand = BlackjackHand()

    def askHit(self):  # Asks if the player wants to hit
        playerhit = input("Would you like to hit? (y/n)")
        if playerhit in "yY":
            return True
        elif playerhit in "nN":
            return False
        else:
            print("I didn't quite catch that. Please reply with 'y' or 'n'.")
            return (self.askHit())

    def changeMoney(self, num):
        self.money += num


class BlackjackDealer(BlackjackPlayer):
    def askHit(self):  # Dealer automatically hits if its total is less than 17
        if (self.hand.getTotalWithAce() < 17):
            return True
        else:
            return False


def BlackjackGame():
    # Player and Dealer objects are created
    print("Welcome to the BackJack!")
    playerName = input("What's your name, gamer?")
    print("Hello, ", playerName + "!")
    dealer = BlackjackDealer("Dealer", 1)
    player = BlackjackPlayer(playerName, 100)
    playerScore = 0
    dealerScore = 0

    # Beginning of the Game
    rounds = input("How many rounds would you like to play?"
                   )  # This segmen9t determines how many rounds are played
    if rounds not in "1234567890":
        Round = False
        rounds = input("Please give a positive integer number.")
    else:
        Round = True
    while Round == False:
        if rounds not in "1234567890" or rounds == '':
            rounds = input("Please give a positive integer number.")
        else:
            Round = True

    Round = False
    bettingGame = input(
        "Do you want to bet virtual money during this game? You will start with 100G. (Type 'y' or 'n')"
    )  # This segment asks the player if they want to bet money
    if bettingGame == 'y':
        hasBet = True
        canBet = True
        Round = True
    elif bettingGame == 'n':
        hasBet = False
        canBet = False
        Round = True
    else:
        Round = False
        bettingGame = input("Please type 'y' or 'n'.")
    while Round == False:
        if bettingGame == 'y':
            hasBet = True
            canBet = True
            Round = True
        elif bettingGame == 'n':
            hasBet = False
            canBet = False
            Round = True
        else:
            Round = False

    print("*****Shuffling Deck*****")
    blackjackDeck = BlackjackHand()  # Make a deck...
    blackjackDeck.createDeck()  # ...add all the cards into it...
    blackjackDeck.shuffle()  # ...and randomly shuffle it.

    # Game proceeds with "rounds" amount of rounds
    for x in range(int(rounds)):
        playerRound = True
        dealerRound = True
        print("Starting the Game now...")
        print("[Round {}]".format(str(x + 1)), "Score: Dealer", dealerScore,
              "Vs", playerName, playerScore)

        if (
                hasBet
        ):  # If Player is betting/has bet, their current balance is displayed
            print("{}'s balance: {}".format(playerName,
                                            str(player.getMoney())))
        if (canBet):  # If Player is betting, they are asked to place their bet
            betAmt = int(
                input(
                    "List the amount of G you want to bet. (Bet has to be at least than 10G, but cannot be more than your current balance)"
                ))
            while (betAmt < 10 or betAmt > player.getMoney()):
                if (betAmt < 10):
                    betAmt = int(
                        input(
                            "Your bet cannot be that low! (Bet has to be at least than 10G, but cannot be more than your current balance))"
                        ))
                else:
                    betAmt = int(
                        input(
                            "You don't have enough money to bet that much! (Bet has to be at least than 10G, but cannot be more than your current balance))"
                        ))

        for x in range(2):  # Hands are given to both players
            card = blackjackDeck.deal()
            player.addCard(card)
        card = blackjackDeck.deal()
        card2 = blackjackDeck.deal()
        dealer.addCard(card)
        dealer.addCard(card2)
        print(playerName + "'s hand", player.hand, "Value =",
              player.hand.getTotalWithAce())
        print("Dealer's hand [{} ???]".format(str(card)))

        # Blackjack Scenario (If either player gets a Blackjack)
        if player.hand.getTotalWithAce(
        ) == 21 and dealer.hand.getTotalWithAce() != 21:
            print("You got a Blackjack!")
            if (canBet):
                player.changeMoney((betAmt * 1.5) // 1)
            playerRound = False
            dealerRound = False
        elif player.hand.getTotalWithAce(
        ) != 21 and dealer.hand.getTotalWithAce() == 21:
            print("The Dealer got a Blackjack!")
            playerRound = False
            dealerRound = False
        elif player.hand.getTotalWithAce(
        ) == 21 and dealer.hand.getTotalWithAce() == 21:
            print("Both players got a Blackjack! It's a Tie!")
            playerRound = False
            dealerRound = False

        # Normal Scenario, Turn: Player (no natural Blackjack)
        while playerRound:
            playerhit = player.askHit()
            if (playerhit):
                print("Player Hit!")
                card = blackjackDeck.deal()
                player.addCard(card)
                print(playerName + "'s hand", player.hand, "Value =",
                      player.hand.getTotalWithAce())
            elif (playerhit != True):
                playerRound = False
            if player.hand.getTotalWithAce() > 21:
                playerRound = False
                dealerRound = False

        # Normal Scenario, Turn: Dealer (after Player either Stands or Busts)
        while dealerRound:
            print("Dealer Hand ", dealer.hand)
            dealerhit = dealer.askHit()
            while (dealerhit):
                print("Dealer Hit!")
                card = blackjackDeck.deal()
                dealer.addCard(card)
                print("Dealer's hand", dealer.hand, "Value =",
                      dealer.hand.getTotalWithAce())
                dealerhit = dealer.askHit()
            dealerRound = False

        # Ending message when determining the winner of the current round
        if player.hand.getTotalWithAce() > 21:
            print(playerName + " busts! They lose! The Dealer Wins!")
            if (canBet):
                player.changeMoney(-1 * betAmt)
            dealerScore += 1
        elif dealer.hand.getTotalWithAce() > 21:
            print("Dealer busts! They lose! {} Wins!".format(playerName))
            if (canBet):
                player.changeMoney(betAmt)
            playerScore += 1
        elif player.hand.getTotalWithAce() > dealer.hand.getTotalWithAce():
            print(playerName + " Wins! The Dealer Loses!")
            if (canBet):
                player.changeMoney(betAmt)
            playerScore += 1
        elif dealer.hand.getTotalWithAce() > player.hand.getTotalWithAce():
            print("The Dealer Wins! {} loses!".format(playerName))
            if (canBet):
                player.changeMoney(-1 * betAmt)
            dealerScore += 1
        elif dealer.hand.getTotalWithAce() == player.hand.getTotalWithAce():
            print("It's a Tie!!!")

        # Hands are reset; if the player has less than 10G in their balance they cannot bet anymore
        player.tossHand()
        dealer.tossHand()
        if (player.getMoney() < 10):
            canBet = False
            print(
                "Your balance is less than 10G, so you are now unable to bet. Sorry!"
            )

    # Total number of wins for each player are tallied after all rounds are over
    print("-----------------------------------")
    print("Final Score: {} ({}) vs Dealer ({})".format(playerName,
                                                       str(playerScore),
                                                       str(dealerScore)))
    #print("! Final Score", playerName, playerScore, "vs Dealer", dealerScore, " !")
    print("-----------------------------------")
    if playerScore == dealerScore:
        print("It's a Tie!")
    elif playerScore > dealerScore:
        print("Congratulations! " + playerName + " Wins.")
    elif dealerScore > playerScore:
        print("Dealer Wins.")
    if (hasBet):  # Prints out the Player's balance if they decided to bet
        print("{} ended with {}G.".format(playerName, str(player.getMoney())))


BlackjackGame()