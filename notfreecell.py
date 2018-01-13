import random

# The help text introduces the rules to play this game
help_text = "This is the game Free Cell!\n" \
            "You have 52 cards with 4 suits: ♠, ♡, ♣, ♢. " \
            "Each suit contains 13 cards from A to K.\n" \
            "You can press n to start a new game，press h to check the help text.\n" \
            "During a game, you can input order to move only one card at the same time.\n" \
            "If you want to move a card to Main board, the color of that card should be\n" \
            "different from where you move it to and rank of that card should equals that\n" \
            "of where you move it to minus 1.\n" \
            "And only the card in Free cells, Foundations, and the last card in each \n" \
            "column of Main board." \
            "The structure of your order should perform like following:\n" \
            "\t\t[number(place)] [space] [number(place)]\n" \
            "The first 'number(place)' means which card you will move, and the second one \n" \
            "means where this card will be moved to. 'number' mean the column of the situation.\n" \
            "And 'place' only have 3 part: Free cells for c, Foundations for f, Main board for\n" \
            "no character. For example, if you want to move the card from column 1 to column 2,\n" \
            "the order should print as:\n" \
            "\t\t1 2\n" \
            "or from column 1 to 1-st Free cell:\n" \
            "\t\t1 1c\n" \
            "Each Free cell can only be put one card at the same time，and each Foundation can \n" \
            "only add card with same suit by order. When you moved all cards to Foundations, you\n" \
            "are win, and you can press Enter to start a new game."


# Build class Card. Each card has its own face (rank) and suit.
class Card:
    def __init__(self, face, suit):
        self.face = face
        self.suit = suit
        # let suit ordering like: 0=black spades, 1=red heart, 2=black clubs, 3=red diamonds
        self.colour = self.suit % 2

    # get_face function is used to get the face of a card.
    def get_face(self):
        return self.face

    # get_color function is used to get the color of a card.
    def get_colour(self):
        return self.colour

    # get_suit function is used to get the suit of a card.
    def get_suit(self):
        return self.suit

    # output a card as string
    def __str__(self):
        self.suit_name = ['♠', '♡', '♣', '♢'][self.suit]
        if self.face == 0:
            self.face_name = 'A'
        elif self.face >= 10:
            self.face_name = ['J', 'Q', 'K'][self.face - 10]
        else:
            self.face_name = str(self.face + 1)
        return self.suit_name + " " + self.face_name + " "


# transform a string to a card
def return_card(string):
    suit_name = string[0]
    face_name = string[2:]
    dict_s = {'♠': 0, '♡': 1, '♣': 2, '♢': 3}
    suit = dict_s[suit_name]
    if face_name == "A ":
        face = 0
    elif face_name == "10 " or face_name == "J " or face_name == "Q " or face_name == "K ":
        d = {"10 ": 9, "J ": 10, "Q ": 11, "K ": 12}
        face = d[face_name]
    else:
        face = int(face_name[0]) - 1
    # Return the string into class Card.
    return Card(face, suit)


# Build class Deck.
class Deck:
    # When a Deck is built, the value_start and value_end decide the domain of cards' rank.
    # number_of_suits decides how many kinds of suit will put into the deck.
    def __init__(self, value_start, value_end, number_of_suits):
        self.start = value_start
        self.end = value_end
        self.no_suits = number_of_suits
        # Build a list to save all cards in this deck.
        self.cards = []
        for face in range(self.start - 1, self.end):
            for suit in range(self.no_suits):
                self.cards.append(str(Card(face, suit)))

    # Shuffle the order of cards in list in random.
    def shuffle(self):
        random.shuffle(self.cards)

    # Add a card as string in card list.
    def add_card(self, face, suit):
        self.cards.append(str(Card(face, suit)))

    # Draw a card in deck.
    def draw_card(self, card):
        card = self.cards[card - 1]
        return print(card)


# build class NotFreecell to set the rules of this game.
class NotFreecell:
    def __init__(self, deck):
        self.deck = deck.cards
        # in each free cell can only put one card, so we set four string used to be replaced in a list
        self.free_cells = ['None', 'None', 'None', 'None']
        # foundations is set as four lists to save cards with four different suits.
        self.foundations = [['None'], ['None'], ['None'], ['None']]
        # base is the actual management of cards on board.
        self.base = []
        # for the original interface of game, the first 4 columns has 7 rows
        # the last 4 columns has 6 rows.
        for j in range(0, 4):
            self.base.append(self.deck[(7 * j): ((7 * j) + 7)])
        for j in range(4, 8):
            self.base.append(self.deck[(28 + 6 * (j - 4)): (34 + 6 * (j - 4))])

    # This is the function to move card from board to board.
    def move_b_b(self, order):
        # The first part in order means the cards will be moved from which column.
        # The third part in order means the cards will be moved to which column.
        if order[0].isdigit() and 1 <= int(order[0]) <= 8 \
                and order[1].isspace() \
                and order[2].isdigit() and 1 <= int(order[2]) <= 8:
            start = int(order[0]) - 1
            end = int(order[2]) - 1
            if len(self.base[start]) > 0 \
                and (len(self.base[end]) == 0
                     or (len(self.base[end]) > 0
                     and return_card(self.base[start][len(self.base[start]) - 1]).get_face() ==
                     return_card(self.base[end][len(self.base[end]) - 1]).get_face() - 1
                     and return_card(self.base[start][len(self.base[start]) - 1]).get_colour() !=
                     return_card(self.base[end][len(self.base[end]) - 1]).get_colour())):
                self.base[end].extend(self.base[start][(len(self.base[start]) - 1):])
                self.base[start] = self.base[start][0: (len(self.base[start]) - 1)]
                return NotFreecell
            else:
                print("Your order makes no sense, please enter again.")
                return NotFreecell
        else:
            print("Your order makes no sense, please enter again.")
            return NotFreecell

    # The function to move card across from board foundations and free cells.
    def move_bfc(self, order):
        # move card from board to free cells or foundations
        if order[0].isdigit() and 1 <= int(order[0]) <= 8 \
                and order[1].isspace \
                and order[2].isdigit() and 1 <= int(order[2]) <= 4 \
                and (order[3] == 'c' or order[3] == 'f'):
            start = int(order[0]) - 1
            end = int(order[2]) - 1
            place = order[3]
            # when a card is moved to foundations, the list of that will add the card
            if place == "f" and len(self.base[start]) > 0 \
                    and ((self.foundations[end][len(self.foundations[end]) - 1] != 'None'
                          and return_card(self.base[start][len(self.base[start]) - 1]).get_face() ==
                          return_card(str(self.foundations[end][len(self.foundations[end]) - 1])).get_face() + 1
                          and return_card(self.base[start][len(self.base[start]) - 1]).get_suit() ==
                          return_card(str(self.foundations[end][len(self.foundations[end]) - 1])).get_suit())
                         or (return_card(self.base[start][len(self.base[start]) - 1]).get_face() == 0
                             and self.foundations[end][len(self.foundations[end]) - 1] == 'None')):
                self.foundations[end].append(str(return_card(self.base[start][len(self.base[start]) - 1])))
                self.base[start] = self.base[start][0: (len(self.base[start]) - 1)]
                return NotFreecell
            # when a card is moved to free cell, the string None will be replaced by the string of that card.
            elif place == "c" and len(self.base[start]) > 0 and self.free_cells[end] == 'None':
                self.free_cells[end] = self.base[start][len(self.base[start]) - 1]
                self.base[start] = self.base[start][0: (len(self.base[start]) - 1)]
                return NotFreecell
            else:
                print("Your order make no sense, please enter again")
                return NotFreecell
        # Move card from free cell or foundations to board.
        elif order[0].isdigit() and 1 <= int(order[0]) <= 4 \
                and (order[1] == 'c' or order[1] == 'f') \
                and order[2].isspace() \
                and order[3].isdigit() and 1 <= int(order[3]) <= 8:
            start = int(order[0]) - 1
            place = order[1]
            end = int(order[3]) - 1
            if place == 'c' and self.free_cells[start] != 'None' \
                    and (len(self.base[end]) == 0
                         or (len(self.base[end]) > 0
                         and return_card(self.free_cells[start]).get_colour()
                         != return_card(self.base[end][len(self.base[end]) - 1]).get_colour()
                         and return_card(self.free_cells[start]).get_face()
                         == return_card(self.base[end][len(self.base[end]) - 1]).get_face() - 1)):
                self.base[end].append(str(self.free_cells[start]))
                self.free_cells[start] = 'None'
                return NotFreecell
            elif place == 'f' and self.foundations[start][len(self.foundations[start]) - 1] != 'None' \
                    and (len(self.base[end]) == 0
                         or (len(self.base[end]) > 0
                         and return_card(self.foundations[start][len(self.foundations[start]) - 1]).get_colour()
                         != return_card(self.base[end][len(self.base[end]) - 1]).get_colour()
                         and return_card(self.foundations[start][len(self.foundations[start]) - 1]).get_face()
                         == return_card(self.base[end][len(self.base[end]) - 1]).get_face() - 1)):
                self.base[end].append(self.foundations[start][len(self.foundations[start]) - 1])
                self.foundations[start] = self.foundations[start][0: len(self.foundations[start]) - 1]
                return NotFreecell
            else:
                print("Your order makes no sense, please enter again.")
                return NotFreecell
        else:
            print("Your order makes no sense, please enter again.")
            return NotFreecell

    def move_fc(self, order):
        # Move card from free cells to foundations.
        if order[0].isdigit() and 1 <= int(order[0]) <= 4 \
                and order[1] == 'c' \
                and order[2].isspace() \
                and order[3].isdigit() and 1 <= int(order[3]) <= 4 \
                and order[4] == 'f':
            start = int(order[0]) - 1
            end = int(order[3]) - 1
            if self.free_cells[start] != 'None' \
                    and ((len(self.foundations[end]) > 1
                          and return_card(str(self.free_cells[start])).get_suit()
                          == return_card(self.foundations[end][len(self.foundations[end]) - 1]).get_suit()
                          and return_card(str(self.free_cells[start])).get_face()
                          == return_card(self.foundations[end][len(self.foundations[end]) - 1]).get_face() + 1)
                         or (return_card(self.free_cells[start]).get_face() == 0
                             and len(self.foundations[end]) == 1)):
                self.foundations[end].append(str(self.free_cells[start]))
                self.free_cells[start] = 'None'
                return NotFreecell
            else:
                print("Your order makes no sense, please enter again.")
                return NotFreecell
        # Move card from foundations to free cells.
        elif order[0].isdigit() and 1 <= int(order[0]) <= 4 \
                and order[1] == 'f' \
                and order[2].isspace() \
                and order[3].isdigit() and 1 <= int(order[3]) <= 4 \
                and order[4] == 'c':
            start = int(order[0]) - 1
            end = int(order[3]) - 1
            if len(self.foundations[start]) > 1 \
                    and self.free_cells[end] == 'None':
                self.free_cells[end] = self.foundations[start][len(self.foundations[start]) - 1]
                self.foundations[start] = self.foundations[start][0: (len(self.foundations[start]) - 1)]
                return NotFreecell
            else:
                print("Your order makes no sense, please enter again.")
                return NotFreecell
        else:
            print("Your order makes no sense, please enter again.")
            return NotFreecell

    # the interface in document of this game.
    def __str__(self):
        free_cells = ""
        foundations = ""
        main_board = ""
        notation = "Press h to view rules for game and order.\n" \
                   "Press n to start a new game."
        len_deck = []
        for i in range(0, len(self.base)):
            len_deck.append(int(len(self.base[i])))
        max_len = max(len_deck)
        for i in range(0, 4):
            free_cells += str(self.free_cells[i]) + "\t"
            foundations += str(self.foundations[i][len(self.foundations[i]) - 1]) + "\t"
        for i in range(0, max_len):
            for j in range(0, len(self.base)):
                if len(self.base[j]) > i:
                    main_board += self.base[j][i] + "\t\t"
                else:
                    main_board += "\t\t\t"
            main_board += "\n"
        return "Free cells:\t" + free_cells + "Foundations:\t" + \
               foundations + "\n" + main_board + notation


def main():
    # build a while loop with true condition to make sure the system can run in these codes forever.
    while True:
        # add a deck with 52 cards suit the rules of freecell.
        deck = Deck(1, 13, 4)
        # when a game is started, the deck must be shuffled before.
        deck.shuffle()
        # set board as class NotFreecell with a shuffled deck in it.
        board = NotFreecell(deck)
        print(board)
        while True:
            order = str(input("Please input your order:"))
            if order == 'h':
                print(help_text)
                print(board)
            # When the length of order is 3, it may move a card from board to board.
            elif len(order) == 3:
                board.move_b_b(order)
                print(board)
            # Victory may happen when a card is moved to Foundations.
            # Thus, we only need to judge if player wins when order is related to Foundations.
            elif len(order) == 4:
                board.move_bfc(order)
                result = 0
                # There are 4 list in foundations.
                # When each list is filled with 14 elements (None + A-K), players wins.
                for i in range(0, 4):
                    if len(board.foundations[i]) == 14:
                        result += 1
                if result == 4:
                    while True:
                        any_str = input("Victory! Press Enter to start a new Free Cell.")
                        if any_str == "":
                            break
                        else:
                            pass
                    break
                else:
                    print(board)
            # when the length of order is 5, it might move card between foundations and free cells.
            elif len(order) == 5:
                board.move_fc(order)
                result = 0
                for i in range(0, 4):
                    if len(board.foundations[i]) == 14:
                        result += 1
                if result == 4:
                    while True:
                        any_str = input("Victory! Press Enter to start a new Free Cell.")
                        if any_str == "":
                            break
                        else:
                            pass
                    break
                else:
                    print(board)
            # If order is n, break this loop to start a new game.
            elif order == 'n':
                break
            # When order doesn't suit the rules, let play input again.
            else:
                print("Your order makes no sense, please input your order again")
                print(board)


# run the main function.
if __name__ == "__main__":
    main()
