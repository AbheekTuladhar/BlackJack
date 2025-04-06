'''
Student Name: Abheek Tuladhar
Game title: Blackjack
Period: 4
Features of Game: Black jack game with implemented betting and high scores
'''

import pygame, sys, random, os

pygame.init()

WIDTH=750
HEIGHT=WIDTH

size=(WIDTH,HEIGHT)
surface = pygame.display.set_mode(size)

pygame.display.set_caption("Blackjack")

BG = pygame.image.load('bg.jpg').convert_alpha()
BACKCARD = pygame.image.load('blueback.gif').convert_alpha()

BLACK    = (0, 0, 0)
DW_RED   = (206, 17, 38) #DW = Dark Washed
SAFFRON  = (241, 195, 56)
ORANGE = (227, 106, 52)
EMERALD = (80, 200, 120)
GRAY = (128, 128, 128)

xu = WIDTH/65
yu = HEIGHT/85

#Functions
def createDeck():
    """
    Creates a deck of cards.

    Parameters:
    -----------
    None

    Returns:
    --------
    deck : dict
        A dictionary representing the deck of cards, where keys are card names and values are lists containing the card's value and its image.
    """

    deck = {}
    cardFileName = os.listdir('card_images') #Creates a list of all the cards

    for card in cardFileName:
        cardSplit = card.split('.')
        cardValue = cardSplit[0][1:] #Gets the card value by taking the 1st character to the end before the period, such that K12343212345.gif will give 12343212345

        if cardValue in ['j', 'q', 'k']:
            cardValue = 10 #All face cards are 10

        else:
            cardValue = int(cardValue)

        cardImage = pygame.image.load('card_images/' + card).convert_alpha()
        deck[card] = [cardValue, cardImage]

    return deck


def findHighScore(money):
    """
    Checks if the current money beats the high score and acts accordingly

    Parameters:
    -----------
    money : int
        Amount of money user has

    Returns:
    --------
    high : int
        The high score
    name : str
        The name of high score holder
    bool
        Is it the high score or not
    """

    with open("HighScore.txt", 'r', encoding = "utf-8") as iF:
        high2 = iF.readlines()

        try:
            high = int(high2[0].split(" ")[0])
            name = high2[0].split(" ")[1]

        except IndexError or ValueError: #Should only happen if the file is blank
            with open("HighScore.txt", 'w', encoding = "utf-8") as iF:
                iF.write(str(money) + " Error")

            high = money
            name = "Error"

        if money > high:
            return high, name, True
        else:
            return high, name, False


def drawScreen(playerHand, dealerHand, money, bet, running, done, highmoney, name, show_instructions, show_hit_stand, show_deal_button, high_score_input, user_name):
    """
    Draws the surface

    Parameters:
    -----------
    playerHand : list
        A list of cards that the player owns
    dealerHand : list
        A list of cards that the dealer owns
    money : int
        Users total money
    bet : int
        Users bet
    running : bool
        Game is running or not
    done : bool
        If the current game is done
        Gets put to false if Again button is clicked
    highmoney : int
        The high score
    name : str
        The name of the high score holder
    show_instructions : bool
        Whether to show the instructions or not
    show_hit_stand : bool
        Whether to show the hit and stand buttons
    show_deal_button : bool
        Whether to show the deal button
    high_score_input : bool
        Boolean for whether to show the high score input box
    user_name : str
        The current name the user is typing

    Returns:
    --------
    deal_bounds : Rect
        The bounding box of the deal button
    hit_bounds : Rect
        The bounding box of the hit button
    stand_bounds: Rect
        The bounding box of the stand button
    again_bounds : Rect
        The bounding box of the again button
    no_money_bounds : Rect
        The bounding box of the no money play again button
        (different because resets money, again button doesn't)
    submit_bounds : Rect
        The bounding box of the submit button when you submit your name
    running : bool
        Whether the game is running or not
    money : int
        Users money
    bet : int
        Users bet
    done : bool
        If the current game is done
        Gets put to false if Again button is clicked
    show_instructions : bool
        Whether to show the instructions or not
    """

    surface.blit(BG, (0, 0))

    show_message("Blackjack", "Times New Roman", 100, WIDTH/2, HEIGHT/10, DW_RED)
    show_message("Dealer:", "Times New Roman", 50, 13*xu, 20*yu, SAFFRON)
    show_message("Player:", "Times New Roman", 50, 13*xu, ((20*yu) + HEIGHT)//2, SAFFRON) #((20*yu) + HEIGHT)//2 takes the dealer y value and finds the middle of the screen from the bottom to the dealer, for the midpoint
    show_message(f"Money: {money:,}", "Times New Roman", 30, 30*xu, (HEIGHT-2*xu), SAFFRON)
    show_message(f"Bet: {bet:,}", "Times New Roman", 30, 50*xu, (HEIGHT-2*xu), SAFFRON)
    show_message(f"High Score: ${highmoney:,}", "Times New Roman", 30, 13*xu, ((30*yu)+HEIGHT)//2, EMERALD)
    show_message(f"Holder: {name.strip()}", "Times New Roman", 30, 13*xu, ((60*yu)+HEIGHT)//2, EMERALD)

    #Messages on controls
    if show_instructions:
        show_message("'H' key : Half Money for Bet", "Times New Roman", 20, WIDTH - 17*xu, HEIGHT//2 - 2*yu, SAFFRON, BLACK)
        show_message("'A' key : All In", "Times New Roman", 20, WIDTH - 17*xu, HEIGHT//2 + 0.5*yu, SAFFRON, BLACK)
        show_message("Enter for 'Submit' button (For High Score)", "Times New Roman", 20, WIDTH - 17*xu, HEIGHT//2 + 3*yu, SAFFRON, BLACK)
        show_message("Up Arrow : Increase bet by 1", "Times New Roman", 20, WIDTH - 17*xu, HEIGHT//2 + 5.5*yu, SAFFRON, BLACK)
        show_message("Down Arrow : Decrease bet by 1", "Times New Roman", 20, WIDTH - 17*xu, HEIGHT//2 + 8*yu, SAFFRON, BLACK)
        show_message("Left Arrow : Decrease bet by 10", "Times New Roman", 20, WIDTH - 17*xu, HEIGHT//2 + 10.5*yu, SAFFRON, BLACK)
        show_message("Right Arrow : Increase bet by 10", "Times New Roman", 20, WIDTH - 17*xu, HEIGHT//2 + 13*yu, SAFFRON, BLACK)
        show_message("(Can't change bet after deal)", "Times New Roman", 20, WIDTH - 17*xu, HEIGHT//2 + 15.5*yu, SAFFRON, BLACK)

    if getHandTotal(playerHand)[1] == False or getHandTotal(dealerHand)[1] == False: #If the game is over for either the player or the dealer
        running = False

    #Set them all to None, so that if they aren't updated because they aren't being shown at the moment, it doesn't crash
    deal_bounds = None
    hit_bounds = None
    stand_bounds = None
    again_bounds = None
    no_money_bounds = None
    submit_bounds = None

    if show_deal_button and running:
        deal_bounds = show_message("Deal Hand", "Times New Roman", 30, 13*xu, (HEIGHT - 5*yu), DW_RED, BLACK, True) #Button to deal hand

    if show_hit_stand and running:
        hit_bounds = show_message("Hit", "Times New Roman", 30, 8*xu, (HEIGHT - 5*yu), DW_RED, BLACK, True) #Button to hit
        stand_bounds = show_message("Stand", "Times New Roman", 30, 15*xu, (HEIGHT - 5*yu), DW_RED, BLACK, True) #Button to stand

    if not running and not high_score_input:
        if money != 0:
            again_bounds = show_message("Again?", "Times New Roman", 30, WIDTH/2, (HEIGHT - 10*yu),DW_RED, BLACK, True)
        else:
            no_money_bounds = show_message("You Ran Out Of Money, Restart?", "Times New Roman", 30, WIDTH/2, (HEIGHT-8*yu), DW_RED, BLACK, True)

        message, color, money, bet, done = findWinner(playerHand, dealerHand, money, bet, done)
        show_instructions = False
        show_message(message, "Times New Roman", 80, WIDTH/2, HEIGHT/2, color) #If the game isn't runningn and it isn't the dealers turn, then we will blit out the end game message

    if high_score_input:
        running = False
        input_rect = pygame.Rect(WIDTH//2-150, HEIGHT//2 + 50, 300, 50)
        pygame.draw.rect(surface, EMERALD, input_rect)
        show_message("Enter Name:", "Times New Roman", 80, WIDTH/2, HEIGHT/2, BLACK, EMERALD)
        show_message(user_name, "Times New Roman", 30, WIDTH/2, HEIGHT/2 + 75, BLACK)
        submit_bounds = show_message("Submit", "Times New Roman", 30, WIDTH/2, HEIGHT/2 + 125, BLACK, EMERALD, True)

    x = 5*xu
    player_card_count = 0

    for card in playerHand: #Blits the card with spacing
        if card == None:
            surface.blit(BACKCARD, (x, ((HEIGHT - 25*yu))))
        else:
            surface.blit(card[1], (x, ((HEIGHT - 25*yu))))

        if player_card_count < 3: #Stacking
            x += 10*xu

        else:
            x += xu
        player_card_count += 1

    x = 5*xu
    dealer_card_count = 0

    for card in dealerHand: #Blits cards with spacing
        if card == None:
            surface.blit(BACKCARD, (x, (25*yu)))

        else:
            surface.blit(card[1], (x, (25*yu)))

        if dealer_card_count < 3: #Stacking
            x += 10*xu

        else:
            x += xu
        dealer_card_count += 1

    playertotal = getHandTotal(playerHand)[0]
    dealertotal = getHandTotal(dealerHand)[0]

    show_message(str(playertotal), "Times New Roman", 50, 60*xu, 65*yu, DW_RED)
    show_message(str(dealertotal), "Times New Roman", 50, 60*xu, 30*yu, DW_RED)

    return deal_bounds, hit_bounds, stand_bounds, again_bounds, no_money_bounds, submit_bounds, running, money, bet, done, show_instructions


def show_message(words, font_name, size, x, y, color, bg=None, hover=False):
    """
    Credit to programming mentor, Valerie Klosky

    Parameters:
    -----------
    words : str
        The text to be displayed.
    font_name : str
        The name of the font to use.
    size : int
        The size of the font.
    x : int
        The x-coordinate of the center of the text.
    y : int
        The y-coordinate of the center of the text.
    color : tuple
        The RGB color of the text.
    bg : tuple, optional
        The RGB background color of the text. Defaults to None.
    hover : bool, optional
        Whether to change the text color on hover. Defaults to False.

    Returns:
    --------
    text_bounds : Rect
        The bounding box of the text.
    """

    font = pygame.font.SysFont(font_name, size, True, False)
    text_image = font.render(words, True, color, bg)
    text_bounds = text_image.get_rect()  # bounding box of the text image
    text_bounds.center = (x, y)  # center text within the bounding box

    # find position of mouse pointer
    mouse_pos = pygame.mouse.get_pos()  # returns (x,y) of mouse location

    if text_bounds.collidepoint(mouse_pos) and bg != None and hover:
        # Regenerate the image on hover
        text_image = font.render(words, True, bg, color)  # swap bg and text color

    surface.blit(text_image, text_bounds)    #render on screen
    return text_bounds                      #bounding box returned for collision detection


def getHandTotal(hand):
    """
    Returns the total, incorporating how aces can change

    Parameters:
    -----------
    hand : list
        The current hand of either the player or the dealer

    Returns:
    --------
    total : int
        The total of that hand
    game_in_play : bool
        Whether the game is in play, which is based on the total
    """

    total = 0
    aces = 0
    game_in_play = True

    for card in hand:
        if card != None:
            if card[0] == 1:
                aces += 1
                total += 11
            else:
                total += card[0]

    while total > 21 and aces > 0: #If the total is over 21 and we have some aces, convert them to 1s.
        total -= 10
        aces -= 1

    if total > 21:
        game_in_play = False

    return total, game_in_play


def dealCard(hand, deck):
    """
    Deals the cards in the beginning of a game

    Parameters:
    -----------
    hand : list
        The current hand that gets cards appended to it
    deck : dict
        The current deck

    Returns:
    --------
    deck : dict
        The current deck, with the cards added to the hand removed
    """

    cardNames = list(deck.keys())
    chosencard = deck.pop(random.choice(cardNames)) #Pop a random choice from the deck and save it

    for i in range(len(hand)):
        if hand[i] == None:
            hand[i] = chosencard
            return deck

    hand.append(chosencard)
    return deck


def newHand(deck):
    """
    Gives a new hand to both the dealer and the player

    Parameters:
    -----------
    deck : dict
        The current deck

    Returns:
    --------
    deck : dict
        The current deck
    playerHand : list
        The players hand
    dealerHand : list
        The dealers hand
    """

    #Starts game off with both players having no cards, thus [None, None]
    playerHand = [None, None]
    dealerHand = [None, None]

    #Deal Cards
    deck = dealCard(playerHand, deck)
    deck = dealCard(dealerHand, deck)
    deck = dealCard(playerHand, deck)

    return deck, playerHand, dealerHand


def dealerTurn(dealerHand, mainDeck, playerTotal):
    """
    The function that runs when it is the dealers turn

    Parameters:
    -----------
    dealerHand : list
        The hand of the dealer
    mainDeck : dict
        The deck of cards
    playerTotal : int
        The total of the players cards

    Returns:
    --------
    mainDeck : dict
        The updated deck of cards
    dealerHand : list
        The updated hand of the dealer
    """

    #Reveal the dealers card
    dealerHand[1] = mainDeck.pop(random.choice(list(mainDeck.keys())))
    while getHandTotal(dealerHand)[0] < playerTotal:
        #Keeps hitting till it's over the players hand, whether thats above 21 or not.
        #Once it is, then it stops.
        mainDeck = dealCard(dealerHand, mainDeck)
    return mainDeck, dealerHand


def findWinner(playerHand, dealerHand, money, bet, done):
    """
    Finds what message to display

    Parameters:
    -----------
    playerHand : list
        A list of cards that the player has
    dealerHand : list
        A list of cards that the dealer has
    money : int
        Users current money
    bet : int
        Users current bet
    done : bool
        If the current game is done or not

    Returns:
    --------
    message : str
        The message that will be displayed
    color : tuple
        The color of the message
    money : int
        Users current money
    bet : int
        Users current bet
    done : bool
        If the current game is done or not
    """

    color = SAFFRON
    playerTotal = getHandTotal(playerHand)[0]
    dealerTotal = getHandTotal(dealerHand)[0]
    player_bust = getHandTotal(playerHand)[1]
    dealer_bust = getHandTotal(dealerHand)[1]

    if player_bust == False:
        message = "You Bust"
        color = ORANGE

        if not done:
            money -= bet
            done = True

    elif dealer_bust == False:
        message = "Dealer Busts"
        color = EMERALD

        if not done:
            money += bet
            done = True

    elif playerTotal > dealerTotal:
        message = "You Win"
        color = EMERALD

        if not done:
            money += bet
            done = True

    elif playerTotal < dealerTotal:
        message = "Dealer Wins"
        color = ORANGE

        if not done:
            money -= bet
            done = True

    elif playerTotal == dealerTotal:
        message = "Tie"
        color = GRAY

    return message, color, money, bet, done


def main():
    """
    The main function, where all the action happens

    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """

    mainDeck = createDeck()
    playerHand = [None, None]
    dealerHand = [None, None]

    show_hit_stand_buttons = False # Show hit and stand buttons
    show_deal_button = True

    money = 100
    bet = 1

    dealer_turn = False
    running = True
    done = False
    betdone = False
    no_money = False
    high_score_input = False
    show_instructions = True
    user_name = ""
    highmoney, name = findHighScore(money)[:2]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE): #end game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and high_score_input:
                if event.key == pygame.K_RETURN: #If they hit enter, write to file
                    with open("HighScore.txt", 'w', encoding = "utf-8") as iF:
                        iF.write(str(money) + " " + user_name)
                        highmoney = money
                        name = user_name.split(" ")[0] #Only take the first name, in case they put a last name

                    high_score_input = False

                elif event.key == pygame.K_BACKSPACE: #If they hit backspace, it deletes with slicing
                    user_name = user_name[:-1]

                else:
                    if len(user_name) < 13: #When it starts to go out of the box. So it won't add if it's over
                        user_name += event.unicode

            if bet > money:
                bet = money

            if not no_money and not betdone: #betdone is true if we already dealt the cards, or the bet is done
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if bet < money:
                        bet += 1

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if bet > 1:
                        bet -= 1

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if bet - 10 > 1:
                        bet -= 10

                    else:
                        bet = 1 #If we have, say, $9 and hit left, we don't want -1, so we go to minimum

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if bet + 10 < money:
                        bet += 10

                    else:
                        bet = money #Samem logic as 5 lines up

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and not submit_bounds: #All in. The not submit_bounds because let's say your name has an A and you have $3261 and want to bet 100. That's a lot of hitting.
                    bet = money
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_h and not submit_bounds:
                    bet = money//2

            if event.type == pygame.MOUSEBUTTONDOWN: #A lot of button click if statements will follow
                mouse_pos = pygame.mouse.get_pos()
                deal_bounds, hit_bounds, stand_bounds, again_bounds, no_money_bounds, submit_bounds, running, money, bet, done, show_instructions = drawScreen(playerHand, dealerHand, money, bet, running, done, highmoney, name, show_instructions, show_hit_stand_buttons, show_deal_button, high_score_input, user_name)

                if deal_bounds != None and deal_bounds.collidepoint(mouse_pos) and running: #If deal button is clicked
                    mainDeck, playerHand, dealerHand = newHand(mainDeck)
                    betdone = True #No betting after dealt cards

                    #Show the hit and stand buttons and don't show the deal button
                    show_hit_stand_buttons = True
                    show_deal_button = False

                if show_hit_stand_buttons and running:
                    if hit_bounds != None and hit_bounds.collidepoint(mouse_pos): #If buttons are showing and hit
                        mainDeck = dealCard(playerHand, mainDeck) #If hit button is hit, then deal a card

                    if stand_bounds != None and stand_bounds.collidepoint(mouse_pos): #If buttons are showing and stand
                        #If stand button is pressed, then it is the dealers turn and we shouldn't show the hit and stand buttons
                        dealer_turn = True
                        show_hit_stand_buttons = False

                if (again_bounds != None and again_bounds.collidepoint(mouse_pos) and not running): #If again button clicked
                    #Resets variables
                    mainDeck = createDeck()
                    playerHand = [None, None]
                    dealerHand = [None, None]

                    show_hit_stand_buttons = False # Show hit and stand buttons
                    show_deal_button = True

                    #Don't change money or bet because game still continues

                    dealer_turn = False
                    running = True
                    done = False
                    betdone = False
                    no_money = False
                    high_score_input = False
                    show_instructions = True
                    user_name = ""

                if no_money_bounds != None and no_money_bounds.collidepoint(mouse_pos): #If the 'ran out of money' button is clicked
                    #Resets variables
                    mainDeck = createDeck()
                    playerHand = [None, None]
                    dealerHand = [None, None]

                    show_hit_stand_buttons = False # Show hit and stand buttons
                    show_deal_button = True

                    money = 100
                    bet = 1

                    dealer_turn = False
                    running = True
                    done = False
                    betdone = False
                    no_money = False
                    high_score_input = False
                    show_instructions = True
                    user_name = ""

                if submit_bounds != None and submit_bounds.collidepoint(mouse_pos) and high_score_input: #If submit button is pressed
                    with open("HighScore.txt", 'w', encoding = "utf-8") as iF:
                        iF.write(str(money) + " " + user_name)
                        highmoney = money
                        name = user_name.split(" ")[0] #Only take the first name, in case they put a last name
                    high_score_input = False
                    user_name = ""

        if dealer_turn and running:
            #Run the dealer turn function, and then it isn't the dealers turn anymore, which means the game is over
            mainDeck, dealerHand = dealerTurn(dealerHand, mainDeck, getHandTotal(playerHand)[0])
            dealer_turn = False
            running = False

        if findHighScore(money)[2]:
            high_score_input = True

        surface.fill(BLACK)
        deal_bounds, hit_bounds, stand_bounds, again_bounds, no_money_bounds, submit_bounds, running, money, bet, done, show_instructions = drawScreen(playerHand, dealerHand, money, bet, running, done, highmoney, name, show_instructions, show_hit_stand_buttons, show_deal_button, high_score_input, user_name)

        pygame.display.update()

main()
