import tkinter
from tkinter import messagebox, PhotoImage
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Ariel", 40, "italic")
FONT_WORD = ("Ariel", 60, "bold")
FONT_INSTRUCTIONS = ("Ariel", 24, "bold")
CARD_HEIGHT = 526
CARD_WIDTH = 800
CARD_DATA_FILE = "./data/card_data.csv"
COUNTDOWN_TIMER_IN_SEC = 3

# ----------------------------- WORDS --------------------------------- #

HEADER_QUESTION = ""
HEADER_ANSWER = ""

def load_cards_via_pandas():
    '''load the questions and answer pairs from the card data file using pandas'''
    retval = pandas.read_csv(CARD_DATA_FILE)

    columns = retval.columns.tolist()
    global HEADER_QUESTION
    global HEADER_ANSWER
    HEADER_QUESTION = columns[0]
    HEADER_ANSWER = columns[1]

    return retval.to_dict(orient='records')

def load_cards_as_file():
    '''load the questions and answer pairs from the card data file using a straight file interface'''
    with open(CARD_DATA_FILE, "r") as file_words:
        words = file_words.readlines()

    header = words.pop(0).strip().split(sep=",")
    global HEADER_QUESTION
    global HEADER_ANSWER
    HEADER_QUESTION = header[0].strip()
    HEADER_ANSWER = header[1].strip()
    retval = []
    for w in words:
        w_array = w.strip().split(sep=",")
        retval.append( { HEADER_QUESTION: w_array[0].strip(), HEADER_ANSWER: w_array[1].strip()} )
    return retval

# ---------------------------- UI SETUP ------------------------------- #

countdown_clock = None

current_card = {}

def flip_card_to_question():
    question = HEADER_QUESTION
    value = current_card[HEADER_QUESTION]
    canvas_card.itemconfig(canvas_image, image=image_card_back)
    canvas_card.itemconfig(label_title, text=question)
    canvas_card.itemconfig(label_word, text=value, font=FONT_WORD)

def flip_card_to_answer():
    answer = HEADER_ANSWER
    value = current_card[HEADER_ANSWER]
    canvas_card.itemconfig(canvas_image, image=image_card_front)
    canvas_card.itemconfig(label_title, text=answer)
    canvas_card.itemconfig(label_word, text=value, font=FONT_WORD)



# load all the flashcard bank
flashcard_bank = load_cards_via_pandas()

# create a window
window = tkinter.Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# create the canvas for the card
image_card_front = PhotoImage(file="./images/card_front.png")
image_card_back = PhotoImage(file="./images/card_back.png")
canvas_card = tkinter.Canvas(width=CARD_WIDTH, height=CARD_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas_card.create_image(int(CARD_WIDTH/2), int(CARD_HEIGHT/2), image=image_card_front)
canvas_card.grid(row=0, column=0, rowspan=2, columnspan=2)
label_title = canvas_card.create_text(int(CARD_WIDTH/2), 150, text="", font=FONT_TITLE)
label_word = canvas_card.create_text(int(CARD_WIDTH/2), int(CARD_HEIGHT/2), text="Click green button to start", font=FONT_INSTRUCTIONS)

# create the right button
def right_button_clicked():
    display_random_card()
image_right = PhotoImage(file="./images/right.png")
button_right = tkinter.Button(image=image_right, bg=BACKGROUND_COLOR, highlightthickness=0, command=right_button_clicked)
button_right.grid(row=2, column=0)

# create the wrong button
def wrong_button_clicked():
    pass
image_wrong = PhotoImage(file="./images/wrong.png")
button_wrong = tkinter.Button(image=image_wrong, highlightthickness=0, command=wrong_button_clicked)
button_wrong.grid(row=2, column=1)

# create a timer label
label_countdown_clock = tkinter.Label(text="[COUNTDOWN_TIMER]")
label_countdown_clock.grid(row=3, column=0, columnspan=2)




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
        flip_card_to_answer()
        window.after_cancel(countdown_clock)


# select a random card
def display_random_card():
    global current_card
    global countdown_clock
    if countdown_clock != None:
        window.after_cancel(countdown_clock)
    current_card = random.choice(flashcard_bank)
    flip_card_to_question()
    countdown(COUNTDOWN_TIMER_IN_SEC)


# we wait until the user clicks the button...



# loop for user input
window.mainloop()
