from p5 import *
import random
from tkinter import *

def play():
    window = Tk()

    # creates the possible suits and values of each card
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    # creates the dictionary for the current deck
    allcards = {}

    # creates the dictionaries for the probability of drawing each card value
    probabilities = {}

    # creates your current hand and the dealer's current hand
    you = {}
    dealer = {}

    # creates the deck from the card suits and values --> turns the value of jacks, queens, kings to 10
    for suit in suits:
        for value in values:
            if 2 <= value <= 10:
                allcards[str(value) + " of " + suit] = value
            if value == 1:
                allcards["Ace" + " of " + suit] = 11
            if value == 11:
                allcards["Jack" + " of " + suit] = 10
            if value == 12:
                allcards["Queen" + " of " + suit] = 10
            if value == 13:
                allcards["King" + " of " + suit] = 10


    def initialcards():
        # deals two cards to you and two cards to the dealer
        for initialcard in range(2):
            initialcard = random.choice(list(allcards.keys()))
            you[initialcard] = allcards[initialcard]
        for initialcard in you:
            for card in list(allcards.keys()):
                if card == initialcard:
                    del allcards[card]
        for initialcard in range(2):
            initialcard = random.choice(list(allcards.keys()))
            dealer[initialcard] = allcards[initialcard]
        for initialcard in dealer:
            for card in list(allcards.keys()):
                if card == initialcard:
                    del allcards[card]

    # creates the initial labels
    updatebartext = "Your turn:"
    updatebar = Label(window, text = updatebartext, font = ('Helvetica', 14, 'bold'))
    updatebar.place(x = 580, y = 100)
    yourcards = Label(window, text = "Your cards:", font = ('Helvetica', 14, 'bold'))
    yourcards.place(x = 100, y = 100)
    dealercards = Label(window, text = "Dealers' cards:", font = ('Helvetica', 14, 'bold'))
    dealercards.place(x = 300, y = 100)

    def displaycards(hiddencardvar):
        # displays only your cards (not their values)
        yourcards = list(you.keys())
        for card in range(len(you)):
            yourcard = Label(window, text = yourcards[card])
            yourcard.place(x = 100, y = 20*card + 120)

        # displays only the dealer's cards (not their values)
        # if hiddencardvar is 1, the first card will be hidden; if hiddencardvar is 0, the first card will be shown
        dealercards = list(dealer.keys())
        if hiddencardvar == 1:
            hiddencard = Label(window, text = "--Hidden--")
            hiddencard.place(x = 300, y = 120)

        for card in range(hiddencardvar, len(dealer)):
            dealercard = Label(window, text = dealercards[card])
            dealercard.place(x = 300, y = 20*card + 120)

    def displaytotals():
        # calculates your total and displays it
        yourvalues = list(you.values())
        yourtotal = 0
        for value in yourvalues:
            yourtotal += value
            totallabel = Label(window, text = "Your total: " + str(yourtotal))
            totallabel.place(x = 100, y = 250)

    def status():
        # figures out your total and displays a status label based on if you won or busted (or if the dealer won or busted)
        yourvalues = list(you.values())
        yourtotal = 0
        for value in yourvalues:
            yourtotal += value
        if yourtotal == 21:
            statuslabel = Label(window, text = "You got 21--you won!", font = ('Helvetica', 20, 'bold'))
            statuslabel.place(x = 100, y = 50)
            statuslabel.config(fg = "green")
        elif yourtotal > 21:
            statuslabel = Label(window, text = "You busted--you lose!", font = ('Helvetica', 20, 'bold'))
            statuslabel.place(x = 100, y = 50)
            statuslabel.config(fg = "red")


        dealervalues = list(dealer.values())
        dealertotal = 0
        for value in dealervalues:
            dealertotal += value
        if dealertotal == 21:
            statuslabel = Label(window, text = "Dealer got 21--you lose!", font = ('Helvetica', 20, 'bold'))
            statuslabel.place(x = 100, y = 50)
            statuslabel.config(fg = "red")
            displaycards(0)
        elif dealertotal > 21:
            statuslabel = Label(window, text = "Dealer busted--you win!", font = ('Helvetica', 20, 'bold'))
            statuslabel.place(x = 100, y = 50)
            statuslabel.config(fg = "green")
            dealertotallabel = Label(window, text = "Dealer total: " + str(dealertotal))
            dealertotallabel.place(x = 300, y = 250)

    def probabilityentry():
        # calculates the probability of drawing a certain value
        cardtotals = {}
        userentry = valueentry.get()
        currentdeck = list(allcards.values())

        for value in currentdeck:
            cardtotals[value] = 0

        for value1 in cardtotals:
            for value2 in currentdeck:
                if value1 == value2:
                    cardtotals[value2] += 1

        totaloptions = 0
        for value in cardtotals:
            totaloptions += cardtotals[value]

        # calculates the probability
        for value in cardtotals:
            probabilities[value] = value/totaloptions*100

        cardtotals[1] = cardtotals[11]

        # rounds the probability to 2 decimals
        probabilityvalue = round(probabilities[int(userentry)], 2)

        # prints the probability
        outputprobabilitylabel = Label(window, text = "The probability of drawing a " + str(userentry) + " is " + str(probabilityvalue) + "%.")
        outputprobabilitylabel.place(x = 100, y = 510)

    def probwinlose():
        # calculates the probabilities if you hit
        cardtotals = {}
        yourvalues = list(you.values())
        yourtotal = 0
        for value in yourvalues:
            yourtotal += value

        currentdeck = list(allcards.values())

        for value in currentdeck:
            cardtotals[value] = 0

        for value1 in cardtotals:
            for value2 in currentdeck:
                if value1 == value2:
                    cardtotals[value2] += 1
        cardtotals[1] = cardtotals[11]


        unsuccessfuloutcomes = 0
        fineoutcomes = 0
        successfuloutcomes = 0

        # calculates # of cards that will give you more than, less than, or equal to 21
        for card in cardtotals:
            if yourtotal + card > 21:
                unsuccessfuloutcomes += cardtotals[card]
            elif yourtotal + card < 21:
                fineoutcomes += cardtotals[card]
            elif yourtotal + card == 21:
                successfuloutcomes += cardtotals[card]

        totaloutcomes = 0
        for card in cardtotals:
            totaloutcomes += cardtotals[card]

        # calculates the probabilities based on outcomes
        unprob = round(unsuccessfuloutcomes/totaloutcomes*100, 2)
        fineprob = round(fineoutcomes/totaloutcomes*100, 2)
        sucprob = round(successfuloutcomes/totaloutcomes*100, 2)
        unsuccessfullabel = Label(window, text = "The probability of busting if you hit is " + str(unprob) + "%.")
        unsuccessfullabel.place(x = 100, y = 340)
        finelabel = Label(window, text = "The probability of having less than 21 if you hit is " + str(fineprob) + "%.")
        finelabel.place(x = 100, y = 360)
        successfullabel = Label(window, text = "The probability of having 21 if you hit is " + str(sucprob) + "%.")
        successfullabel.place(x = 100, y = 380)

    def hityou():
        # deals you a new card
        yourvalues = list(you.values())
        yourtotal = 0
        for value in yourvalues:
            yourtotal += value

        if yourtotal < 21:
            newcard = random.choice(list(allcards.keys()))
            you[newcard] = allcards[newcard]
            # changes ace value from 11 to 1
            if yourtotal > 10:
                if you[newcard] == 11:
                    you[newcard] = 1
        if yourtotal > 21:
            for card in you:
                if you[card] == 11:
                    you[card] = 1

            # deletes the card from the main deck
            for newcard in you:
                for card in list(allcards.keys()):
                    if card == newcard:
                        del allcards[card]
        displaycards(1)
        displaytotals()
        status()

    def finddealertotal():
        # finds the dealer total
        dealervalues = list(dealer.values())
        dealertotal = 0
        for value in dealervalues:
            dealertotal += value
        return dealertotal

    def hitdealer():
        # deals a new card to the dealer
        newcard = random.choice(list(allcards.keys()))
        dealer[newcard] = allcards[newcard]
        if finddealertotal() > 10:
            if dealer[newcard] == 11:
                dealer[newcard] = 1

        for newcard in dealer:
            for card in list(allcards.keys()):
                if card == newcard:
                    del allcards[card]
        displaycards(0)

    def stand():
        dealervalues = list(dealer.values())
        updatebartext = "Dealer's turn"
        dealertotal = 0
        for value in dealervalues:
            dealertotal += value
        # deals a new card to the dealer while their total is <= 16
        while dealertotal <= 16:
            hitdealer()
            dealertotal = 0
            dealervalues = list(dealer.values())
            for value in dealervalues:
                dealertotal += value
            status()

        yourvalues = list(you.values())
        yourtotal = 0
        for value in yourvalues:
            yourtotal += value

        status()
        displaycards(0)

        # if neither player has more than or equal to 21, checks who won
        if yourtotal < 21 and dealertotal < 21:
            if yourtotal > dealertotal:
                statuslabel = Label(window, text = "You won!", font = ('Helvetica', 20, 'bold'))
                statuslabel.place(x = 100, y = 50)
                statuslabel.config(fg = "green")
            elif yourtotal < dealertotal:
                statuslabel = Label(window, text = "You lose!", font = ('Helvetica', 20, 'bold'))
                statuslabel.place(x = 100, y = 50)
                statuslabel.config(fg = "red")
            elif yourtotal == dealertotal:
                statuslabel = Label(window, text = "It's a tie!", font = ('Helvetica', 20, 'bold'))
                statuslabel.place(x = 100, y = 50)
            dealertotallabel = Label(window, text = "Dealer total: " + str(dealertotal))
            dealertotallabel.place(x = 300, y = 250)

    # creates hit and stand buttons
    class hitstandbuttons:
        def __init__(self, hitx, hity, standx, standy):
            self.hitx = hitx
            self.hity = hity
            self.standx = standx
            self.standy = standy

        def makebuttons(self):
            hitbutton = Button(window, text = "Hit", command = hityou)
            hitbutton.place(x = self.hitx, y = self.hity)

            standbutton = Button(window, text = "Stand", command = stand)
            standbutton.place(x = self.standx, y = self.standy)


    buttons = hitstandbuttons(580, 120, 640, 120)
    buttons.makebuttons()

    # creates all other labels, entry, and buttons
    entrylabel = Label(window, text = "Type in a card value to see your probability of drawing it:")
    entrylabel.place(x = 100, y = 430)

    valueentry = Entry(window, bd = 5)
    valueentry.place(x = 100, y = 450)

    entrybutton = Button(window, text = "Enter", command = probabilityentry)
    entrybutton.place(x = 100, y = 485)

    probwinlosebutton = Button(window, text = "Press to see your probabilities if you hit", command = probwinlose)
    probwinlosebutton.place(x = 100, y = 310)

    maintitle = Label(window, text = "Blackjack", font = ('Helvetica', 20, 'bold'))
    maintitle.place(x = 580, y = 50)


    playbutton = Button(window, text = "Play again", command = play, font = ('Helvetica', 14, 'bold'))
    playbutton.place(x = 680, y = 550)

    initialcards()
    displaycards(1)
    displaytotals()
    status()

    window.title("Blackjack")
    window.geometry("800x600")
    window.mainloop()

# runs the program
play()
