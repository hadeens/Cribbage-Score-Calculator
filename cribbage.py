class Card:
    """Represents a typical playing card in a 52 card deck, specifically for the game of cribbage.

        Attributes:
        ----------
        name : str
            the name of the card, either a number 2-10 or Ace, Jack, Queen, or King
        suit : str
            the suit of the card, either Club, Diamond, Spade, or Heart
        value : int
            what the card is worth when adding for cribbage scoring, a number 1-10 (face cards are worth 10)
        """
    
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value
        
    def __repr__(self):
        return self.name + " of " + self.suit
    
class Hand:
    """Represents a players hand in the game of cribbage, can be any length of card objects. Used for calculating
        point totals for each player during a round. This class essentially emulates a list, it uses the
        container-like class special methods from https://www.pythonlikeyoumeanit.com/Module4_OOP/Special_Methods.html

        Attributes:
        ----------
        contents : list of card objects
            the cards that make up the player's hand. Can either be in a list or on their own. No minimum or maximum.
        points : int
            the cribbage point value associated with the hand.
        """
    def __init__(self, *args):
        #check if list
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            self.contents = list(args[0])
        else:
            #not a list
            self.contents = list(args)
        
        self.points = 0
    
    #the following are all self-explanitory list special methods
    def __getitem__(self, index):
        element = self.contents[index]
        
        return Hand(element) if isinstance(index, slice) else element
    
    def __setitem__(self, key, value):
        self.contents[key] = value
        
    def __len__(self):
        return len(self.contents)
    
    def __contains__(self, item):
        return item in self.contents
    
    def append(self, item):
        self.contents.append(item)
        
    def remove(self, item):
        self.contents.remove(item)
        
    def __repr__(self):
        return "|" + self.contents.__repr__()[1:-1] + "|"
    
    def addto15(self):
        """Checks the cribbage scoring condition of if the cards add to 15.
            """
        total = 0
        #add the card value of each card to the total
        for __card in self.contents:
            total += __card.value
        return True if total == 15 else False
        
    def ofakind(self):
        """Checks the cribbage scoring condition of if the cards are a 4 of a kind, 3 of a kind, or a pair
            """
        #a hand of 5 cards cannot be a 4 of a kind
        if len(self.contents) > 4:
            raise Exception("This hand is greater than 4 cards and cannot be sorted into pairs.")
        #check to see if all of the card names match
        names = []
        for __card in self.contents:
            names.append(__card.name)
        return names.count(names[0]) == len(names)
             
    def run(self):
        """Checks the cribbage scoring condition of if the cards are in sequential order, or a "run"
            """
        #convert the facecard names to their number variants
        names = []
        for __card in self.contents:
            names.append(__card.name)
        for index in range(len(names)):
            if names[index] == "Ace":
                names[index] = "1"
            elif names[index] == "Jack":
                names[index] = "11"
            elif names[index] == "Queen":
                names[index] = "12"
            elif names[index] == "King":
                names[index] = "13"
            names[index] = int(names[index])
        
        #sort the cards by integer, the compare it to a sequential copy of the list
        names.sort()
        return names == list(range(min(names), max(names)+1))
                
    def flush(self):
        """Checks the cribbage scoring condition of if the cards are all of the same suit, or a "flush"
            """
        if len(self.contents) < 4:
            raise Exception("This hand is less than 4 cards and cannot be found as a flush.")
        #check if all of the suits are the same
        suits = []
        for __card in self.contents:
            suits.append(__card.suit)
        return suits.count(suits[0]) == len(suits)
    
    def nobs(self):
        """Checks the cribbage scoring condition of if the players hand has a Jack of the same suit as the starter
            """
        #track all of the suits and names
        name_suit = []
        for __card in self.contents:
            name_suit.append((__card.name,__card.suit))
        #access starter card
        starter = name_suit.pop()
        #check if any of the rest are jacks, then compare it's suit to the starter
        for name,suit in name_suit:
            if name == "Jack":
                if suit == starter[1]:
                    return True
        else:
            return False
                
if __name__ == "__main__":
    
    names_values = [("Ace", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7), ("8", 8),
                ("9", 9), ("10", 10), ("Jack", 10), ("Queen", 10), ("King", 10)]
    _suits = ["Spades", "Clubs", "Hearts", "Diamonds"]

    deck = [Card(name, suit, value) for name, value in names_values for suit in _suits]
    
    handA = Hand(deck[3], deck[7], deck[32], deck[48], deck[50], deck[18])
    
    
