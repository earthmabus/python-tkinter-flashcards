import tkinter
from deck import Deck

BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Ariel", 40, "italic")
FONT_WORD = ("Ariel", 60, "bold")
FONT_INSTRUCTIONS = ("Ariel", 24, "bold")
CARD_HEIGHT = 526
CARD_WIDTH = 800
COUNTDOWN_TIMER_IN_SEC = 3

# ----------------------------- WORDS --------------------------------- #

# load a deck of cards
deck = Deck()
deck.load_cards_via_pandas()

# ---------------------------- UI SETUP ------------------------------- #

def flip_card_to_question(current_card):
    value = current_card[deck.m_header_question]
    canvas_card.itemconfig(canvas_image, image=image_card_back)
    canvas_card.itemconfig(label_title, text=deck.m_header_question)
    canvas_card.itemconfig(label_word, text=value, font=FONT_WORD)

def flip_card_to_answer(current_card):
    value = current_card[deck.m_header_answer]
    canvas_card.itemconfig(canvas_image, image=image_card_front)
    canvas_card.itemconfig(label_title, text=deck.m_header_answer)
    canvas_card.itemconfig(label_word, text=value, font=FONT_WORD)

# create a window
window = tkinter.Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# create the canvas for the card
image_card_front = tkinter.PhotoImage(file="./images/card_front.png")
image_card_back = tkinter.PhotoImage(file="./images/card_back.png")
canvas_card = tkinter.Canvas(width=CARD_WIDTH, height=CARD_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas_card.create_image(int(CARD_WIDTH/2), int(CARD_HEIGHT/2), image=image_card_front)
canvas_card.grid(row=0, column=0, rowspan=2, columnspan=2)
label_title = canvas_card.create_text(int(CARD_WIDTH/2), 150, text="", font=FONT_TITLE)
label_word = canvas_card.create_text(int(CARD_WIDTH/2), int(CARD_HEIGHT/2), text="Click green button to start", font=FONT_INSTRUCTIONS)

# create the right button
def right_button_clicked():
    # remove the current card from the deck (if one is displayed) and display a new card
    deck.remove_current_card_from_deck()
    display_random_card()
image_right = tkinter.PhotoImage(file="./images/right.png")
button_right = tkinter.Button(image=image_right, bg=BACKGROUND_COLOR, highlightthickness=0, command=right_button_clicked)
button_right.grid(row=2, column=0)

# create the wrong button
def wrong_button_clicked():
    if len(deck.m_current_card) > 0:
        print(f"kept current card in deck: {deck.m_header_question} with {deck.m_current_card[deck.m_header_question]}")
        display_random_card()
image_wrong = tkinter.PhotoImage(file="./images/wrong.png")
button_wrong = tkinter.Button(image=image_wrong, highlightthickness=0, command=wrong_button_clicked)
button_wrong.grid(row=2, column=1)

# create a timer label
label_countdown_clock = tkinter.Label(text="[COUNTDOWN_TIMER]", bg=BACKGROUND_COLOR)
label_countdown_clock.grid(row=3, column=0, columnspan=2)

# create a countdown clock that will go from COUNTDOWN_TIMER_IN_SEC to 0
# while it's greater than 0, the program will display number of seconds remaining
# when it reaches 0, the program will flip the card to the answer side
countdown_clock = None

def countdown(countdown_in_seconds):
    '''updates the timer, updating a countdown clock, and flips card when it hits 0 seconds remaining'''

    # update the countdown clock...
    global countdown_clock
    label_countdown_clock.config(text=f"Time Remaining: {countdown_in_seconds} sec")

    # if the countdown clock isn't at 0, keep counting, otherwise flip the card and stop counting
    if countdown_in_seconds > 0:
        # the timer is not at 0, countdown one more second
        countdown_clock = window.after(1000, countdown, countdown_in_seconds - 1)
    else:
        # the timer hit 0, flip the card to the answer and cancel the timer
        flip_card_to_answer(deck.m_current_card)
        window.after_cancel(countdown_clock)

# select a random card
def display_random_card():
    global countdown_clock
    if countdown_clock != None:
        window.after_cancel(countdown_clock)
    deck.get_random_card()
    flip_card_to_question(deck.m_current_card)
    countdown(COUNTDOWN_TIMER_IN_SEC)

#######################
# loop for user input #
#######################
window.mainloop()
