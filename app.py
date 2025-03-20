import os
from flask import Flask, render_template
from PIL import Image, ImageDraw, ImageFont


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

    
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suit_symbols = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}


#Defining a class for card
class Card:
    def __init__(self, suit, value, symbol):
        self.suit = suit
        self.value = value
        self.symbol = symbol


#Function for generating a ASCII art face for a card

    def generate_ascii_card(self):
        card_template = [
            "┌─────────┐",
            "│{:<2}       │".format(self.value),
            "│         │",
            "│    {}    │".format(self.symbol),
            "│         │",
            "│       {:>2}│".format(self.value),
            "└─────────┘"
        ]
        return "\n".join(card_template)


#Function that creates an image of a card and saves it

if not os.path.exists('static/cards'):
    os.makedirs('static/cards')


def generate_card_image(card):
    filename = f"static/cards/{card.value}_{card.suit}.png"
    if not os.path.exists(filename):
        ascii_card = card.generate_ascii_card()

        width, height = 400, 200
        image = Image.new('RGB', (width, height), color=(255, 255, 255))

        draw = ImageDraw.Draw(image)

        try: 
            font = ImageFont.truetype("arial.ttf", 18)
        except IOError:
            font = ImageFont.load_default()

        draw.text((10, 10), ascii_card, font=font, fill=(0, 0, 0))

        card_name = f"{card.value}_{card.suit}.png"

        image_path = os.path.join("static/cards", card_name)
        image.save(image_path)

        return image_path


#Defining a deck of cards

deck = [Card(suit, value, suit_symbols[suit]) for suit in suits for value in values]


#Function that creates images for each card in the deck

def generate_all_card_images(deck):
    for card in deck:
        card.generate_card_image()


#Generate_all_card_images() function call
    generate_all_card_images(deck)
