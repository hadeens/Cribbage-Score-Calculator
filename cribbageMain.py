from cribbage_utility import *
from cribbage import Card, Hand
from guizero import App, Text, Box, PushButton, Combo, Picture, ListBox

names_values = [("Ace", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7), ("8", 8),
                ("9", 9), ("10", 10), ("Jack", 10), ("Queen", 10), ("King", 10)]
_suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
    
orderedDeck = [Card(name, suit, value) for name, value in names_values for suit in _suits]

def top3(Hand):
    """Compares the top three hands and shows them to the user. Then adds the starter card to the user's
        chosen hand and shows them the total points for the round.
        
        Parameters
        ----------
        Hand : Hand object
            the cards delt to the user to be analyzed
        """
    def final(choice):
        """Displays the user's chosen hand and then gets the starter input. Brings user to the end screen
            where it displays the final total or compares the user's points to the opposition.
            
            Parameters
            ----------
            choice : Hand object
                the user's choice within the top 3 options
            """
        #delete all of the widgets except the title
        for widget in app.children.copy():
            if widget != title:
                widget.destroy()
                
        def showStarter():
            """Shows the starter to the user in the input branch, and displays their final point total.
                """
            #checks the users hand to ensure a duplicate starter is not added
            for c in Hand:
                if _cards.value == c.__repr__():
                    #show duplicate error message
                    error.show()
                    break
            else:
                #hide the starter input widgets
                add_S.hide()
                error.hide()
                _cards.hide()
                pleaseAdd.hide()
                
                #add the starter card from listbox to the user's hand as a card object
                for card in orderedDeck:
                    if _cards.value == card.__repr__():
                        choice.append(card)
                
                #visually show starter card and display final point total
                starter = Text(app, text="Starter:")
                sPic = Picture(app, image=f'card_images/{_cards.value}.png')
                total = calculate_hand(getHand_subgroups(choice, starter = 1), starter = 1)
                points = Text(app, text=f'Points: {total}', color="dark orange")
                
                #check if the user has gotten zero points
                if total == 0:
                    skunk = Text(app, text="You've been skunked!")
                    skunkboy = Picture(app, image=f'card_images/Skunk.png')
        
        #input branch
        if randOrInput.value == "Input Hand":
            
            #represents the user's chosen hand visually
            yourChoice = Text(app, text=f'You chose:')
            boxbox = Box(app,width=300,height=90)   
            for index, (pic, box) in enumerate(pics_boxes2):
                box = Box(boxbox, align="left", width="fill", height=75)
                pic = Picture(box, image=f'card_images/{choice[index].__repr__()}.png')
            
            #widgets for getting starter card input, with error message
            pleaseAdd = Text(app, text="Please select a starter card below:")
            _cards = ListBox(app, scrollbar=True,
                        items=[Card(name, suit, value) for name, value in names_values for suit in _suits])
            add_S = PushButton(app, text="Add Starter", command=showStarter)
            error = Text(app, text="This card is already in your hand, it cannot be the starter")
            error.hide()
        
        #simulation branch
        elif randOrInput.value == "Simulate":
            def representHand(mano, star):
                """Visually represents the user and the opponent's hands and their point values using widgets
                    """
                #widgets for the cards in the hand
                boxbox = Box(app,width=300,height=90)   
                for index, (pic, box) in enumerate(pics_boxes2):
                    box = Box(boxbox, align="left", width="fill", height=75)
                    pic = Picture(box, image=f'card_images/{mano[index].__repr__()}.png')
                
                #adds the starter to the hand, calculates and displays the point total
                mano.append(star[0])
                total = calculate_hand(getHand_subgroups(mano, starter = 1), starter = 1)
                points = Text(app, text=f'Points: {total}', color="dark orange")
                
                return total
            
            #sets player value for the starter function
            if players.value == "2 Players":
                p = 2
            elif players.value == "3 Players":
                p = 3
            
            #gets a random starter and displays the card
            start = getRandom_starter(deck1, p)
            deck2 = start[1]
            starter = Text(app, text="Starter:")
            sPic = Picture(app, image=f'card_images/{start[0].__repr__()}.png')
            
            #visually represent user's hand
            yourChoice = Text(app, text=f'You chose:')
            client = representHand(choice, start)
            
            #run calculation algorithm on opponents hand and display it
            top_3 = compare(getHand_possibilities(oppo1))  
            opponent = Text(app, text=f"Opponent's Hand:")
            one = representHand(top_3[0][0], start)
            
            #repeat calculation algorithm and display if third player is involved
            two = 0
            if players.value == "3 Players":
                top_3_2 = compare(getHand_possibilities(oppo2))
                opponent = Text(app, text=f"Opponent 2's Hand:")
                two = representHand(top_3_2[0][0], start)
            
            #result messages of simulation
            if client == 0:
                skunk = Text(app, text="You've been skunked!", size=14, color="brown")
                skunkboy = Picture(app, image=f'card_images/Skunk.png')
            elif client > one and client > two:
                win = Text(app, text="You win this round!", size=14, color="green")
            elif (client == one and client > two) or (client == two and client > one):
                tie = Text(app, text="You tied this round!", size=14, color="yellow")
            else:
                lose = Text(app, text="You lose this round!", size=14, color="red")
    
    #sets names for the widgets that will show the cards
    yourHand = Text(app, text="Your hand:", size=14)
    if players.value == "2 Players":
        pics_boxes = [('cPic1','box_1'),('cPic2','box_2'),('cPic3','box_3'),('cPic4','box_4'),
                               ('cPic5','box_5'),('cPic6','box_6')]
    if players.value == "3 Players":
        pics_boxes = [('cPic1','box_1'),('cPic2','box_2'),('cPic3','box_3'),('cPic4','box_4'),
                               ('cPic5','box_5')]
    
    #widgets to visually show the user's hand
    boxbox = Box(app,width=300,height=90)   
    for index, (pic, box) in enumerate(pics_boxes):
        box = Box(boxbox, align="left", width="fill", height=75)
        pic = Picture(box, image=f'card_images/{user[index]}.png')
    
    #runs the calculation algorithm
    best3 = Text(app, text="The three best possible hands:", size=16)
    top_3 = compare(getHand_possibilities(Hand))
    
    #sets the names for the widgets in each top 3 hand
    pics_boxes2 = [('cPic_1','box1'),('cPic_2','box2'),('cPic_3','box3'),('cPic_4','box4')]
    
    #displays each hand in the top three, shows the points, and allows the user to select it
    for i in range(3):
        heading = Text(app, text=f'Hand {i+1}', size=14, color="Blue")
        handBox = Box(app, width=300, height=90)
        for ind, (p, b) in enumerate(pics_boxes2):
            b = Box(handBox, align="left", width="fill", height=75)
            p = Picture(b, image=f'card_images/{top_3[i][0][ind].__repr__()}.png')
        
        points = Text(app, text=f'Points: {top_3[i][1]}', color="dark green")
        choose = PushButton(app, text="Select", command=final, args=[top_3[i][0]])
    
def begin(deck):
    """Starts the utility when Start is clicked and allows the user to select either a random or input hand.
        
        Parameters
        ----------
        deck : list of card objects
            standard deck of 52 card
        """
    #reset the screen
    players.hide()
    randOrInput.hide()
    start.hide()
    cribbage.destroy()
    title.value = "Cribbage Utility"
    
    #path for user-input hand
    if randOrInput.value == "Input Hand":
        
        def deleteAll():
            """Clears the current cards selected by the user, triggered by pressing the clear all button
                """
            #resets error messages and deletes all list entries
            full.hide()
            double.hide()
            notfull.hide()
            user.clear()
            
            #resets the text and picture in each card slot to Card 1, Card 2, etc
            for num, item in enumerate(items_boxes):
                globals()[item[0]].value = f'Card {num+1}'
                globals()[item[0]].show()
                for w in globals()[item[1]].children:
                    if isinstance(w, Picture):
                        w.destroy()
                    
        def addcard():
            """Adds the selected card to the user's hand visually and to the list itself. It will first check
                to make sure there are no doubles of the selected card or if every slot is filled.
                Triggered when pressing the Add Card to Hand button.
                """
            #reset the error messages
            double.hide()
            full.hide()
            notfull.hide()
            #check if selected card is already in the user's hand
            if cards.value in user:
                double.show()
            else:
                #check to see if each slot is empty, then add the card to that slot and to the list
                for num, item in enumerate(items_boxes):
                    if globals()[item[0]].value == f'Card {num+1}':
                        globals()[item[0]].value = cards.value
                        globals()[item[0]].hide()
                        globals()[f'cPic{num+1}'] = Picture(globals()[item[1]], image=f'card_images/{cards.value}.png')
                        user.append(cards.value)
                        break
                else:
                    #display the hand is full error message if the for loop reaches the end
                    full.show()
        
        def submit():
            """Checks if the the hand is full, then brings the user to the next screen
                and inputs their hand into the scoring algorithm.
                """
            if len(user) != 6 and players.value == "2 Players":
                #show the error message for submitting an empty hand
                double.hide()
                notfull.show()
            elif len(user) != 5 and players.value == "3 Players":
                #show the error message for submitting an empty hand
                double.hide()
                notfull.show()
            else:
                #hide all of the widgets except the title
                for widget in app.children.copy():
                    if widget != title:
                        widget.destroy()
                    
                #convert each string in the list representing the user's hand into a card object
                for index, entity in enumerate(user):
                    for card in deck:
                        if entity == card.__repr__():
                            user[index] = card
                
                #convert the list of cards into a hand object and run the calculation algorithm
                _user = Hand(user)
                top3(_user)
        
        #create widgets for the title and the list of cards to select from
        t_input = Text(app, text="Input your hand here")
        cardbox = Box(app, width=200, height=200)
        cards = ListBox(cardbox, scrollbar=True,
                        items=[Card(name, suit, value) for name, value in names_values for suit in _suits])
        
        if players.value == "2 Players":
            #sets the card slot names to be used in deleteAll and addcard functions
            items_boxes = [('Card_1','box_1'),('Card_2','box_2'),('Card_3','box_3'),('Card_4','box_4'),
                           ('Card_5','box_5'),('Card_6','box_6')]
            boxbox = Box(app,width=300,height=90)
            #create a box and title for each card slot in the hand
            for i in range(6):
                globals()[f'box_{i+1}'] = Box(boxbox, align="left", width="fill", height=75)
                globals()[f'Card_{i+1}'] = Text(globals()[f'box_{i+1}'], text=f'Card {i+1}', width="fill", height="fill",size=10)
        elif players.value == "3 Players":
            #sets the card slot names to be used in deleteAll and addcard functions
            items_boxes = [('Card_1','box_1'),('Card_2','box_2'),('Card_3','box_3'),('Card_4','box_4'),
                           ('Card_5','box_5')]
            boxbox = Box(app,width=225,height=90)
            #create a box and title for each card slot in the hand
            for i in range(5):
                globals()[f'box_{i+1}'] = Box(boxbox, align="left", width="fill", height=75)
                globals()[f'Card_{i+1}'] = Text(globals()[f'box_{i+1}'], text=f'Card {i+1}', width="fill", height="fill",size=10)
        
        #create the buttons for manipulation, and the error messages
        select = PushButton(cardbox, text="Add Card to Hand", command=addcard)
        csBox = Box(app, width=140, height=50)
        clear = PushButton(csBox, align="left", text="Clear All", command=deleteAll)
        submit = PushButton(csBox,align="right", text="Sumbit", command=submit)
        full = Text(app, text="Hand is full! Please clear or sumbit.")
        notfull = Text(app, text="Hand is not full! Please add more cards.")
        double = Text(app, text="This card is already in your hand!")
        double.hide()
        full.hide()
        notfull.hide()
    
    #path for user generated hand
    elif randOrInput.value == "Simulate":
        
        if players.value == "2 Players":
            #randomly shuffle and deal the deck
            shuffled = getHand_random(deck, 2)
            
            #convert each list into a hand
            for entry in shuffled[0]:
                user.append(entry)
            _user = Hand(user)
            for i in shuffled[1]:
                oppo1.append(i)
            _oppo1 = Hand(oppo1)
            for x in shuffled[2]:
                deck1.append(x)
            
            #delete all of the widgets from the title screen
            for widget in app.children.copy():
                    if widget != title:
                        widget.destroy()
            
            #run calculation algorithm
            top3(_user)
            
        elif players.value == "3 Players":
            #randomly shuffle and deal the deck
            shuffled = getHand_random(deck, 3)
            
            #convert each list into a hand
            for entry in shuffled[0]:
                user.append(entry)
            _user = Hand(user)
            for y in shuffled[1]:
                oppo1.append(y)
            _oppo1 = Hand(oppo1)
            for z in shuffled[2]:
                oppo2.append(z)
            _oppo2 = Hand(oppo2)
            for e in shuffled[3]:
                deck1.append(e)
            kitty.append(shuffled[4])
            _kitty = Hand(kitty)
            
            #delete all of the widgets from the title screen
            for widget in app.children.copy():
                    if widget != title:
                        widget.destroy()
            
            #run calculation algorithm
            top3(_user)
                
app = App()

#create lists that can be changed later on
user = []
oppo1 = []
oppo2 = []
deck1 = []
kitty = []

#create the widgets for the title screen
title = Text(app, text="Welcome to Cribbage Utility", color="purple", size="16")
cribbage = Picture(app, image="Cribbage.png")
settings = Box(app, width=210, height=50)
players = Combo(settings, align="left", options=["2 Players", "3 Players"])
randOrInput = Combo(settings, align="right", width=20, options=["Input Hand", "Simulate"])
start = PushButton(app, text="Start", command=begin, args=[orderedDeck])

app.display()