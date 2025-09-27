import random
import pandas

CARD_DATA_FILE = "./data/card_data.csv"
CARD_DATA_TO_LEARN_FILE = "./data/card_data_to_learn.csv"

class Deck:

    def __init__(self):
        self.m_deck = []
        self.m_current_card = {}
        self.m_header_question = ""
        self.m_header_answer = ""

    def load_cards_via_pandas(self):
        '''load the questions and answer pairs from the card data file using pandas'''
        try:
            retval = pandas.read_csv(CARD_DATA_TO_LEARN_FILE)
        except FileNotFoundError:
            try:
                retval = pandas.read_csv(CARD_DATA_FILE)
            except FileNotFoundError:
                print(f"Unable to load contents from {CARD_DATA_FILE}")

        columns = retval.columns.tolist()
        self.m_header_question = columns[0]
        self.m_header_answer = columns[1]

        self.m_deck = retval.to_dict(orient='records')

    def load_cards_as_file(self):
        '''load the questions and answer pairs from the card data file using a straight file interface'''
        try:
            with open(CARD_DATA_TO_LEARN_FILE, "r") as file_words:
                words = file_words.readlines()
        except FileNotFoundError:
            try:
                with open(CARD_DATA_FILE, "r") as file_words:
                    words = file_words.readlines()
            except FileNotFoundError:
                print(f"Unable to load contents from {CARD_DATA_FILE}")

        header = words.pop(0).strip().split(sep=",")
        self.m_header_question = header[0].strip()
        self.m_header_answer = header[1].strip()

        self.m_deck = []
        for w in words:
            w_array = w.strip().split(sep=",")
            self.m_deck.append({self.m_header_question: w_array[0].strip(), self.m_header_answer: w_array[1].strip()})

    def remove_current_card_from_deck(self):
        if len(self.m_current_card) != 0:
            self.m_deck.remove(self.m_current_card)
            df_remaining_words = pandas.DataFrame.from_dict(data=self.m_deck)
            df_remaining_words.to_csv(CARD_DATA_TO_LEARN_FILE, index=False)
            print(f"removed card from deck: {self.m_header_question} with {self.m_current_card[self.m_header_question]}")

    def get_random_card(self):
        self.m_current_card = random.choice(self.m_deck)
        return self.m_current_card
