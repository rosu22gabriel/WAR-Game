import os
import re
from flask import Flask, render_template
from PIL import Image, ImageDraw, ImageFont


app = Flask(__name__)

 
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
        ascii_card = "\n".join(card_template)
        print(f"Generated ASCII art for {self.value} of {self.suit}: \n{ascii_card}", flush=True)
        return ascii_card
    
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename) 


if not os.path.exists('static/cards'):
    os.makedirs('static/cards')


#Function that creates an image of a card and saves it

def generate_card_image(card):
    print(f"Attempting to generate image for {card.value} of {card.suit}", flush=True)
    card_name = sanitize_filename(f"{card.value}_{card.suit}.png")
    filename = f"static/cards/{card_name}"
    if not os.path.exists(filename):
        ascii_card = card.generate_ascii_card()
        print(f"Generated ASCII art for {card.value} of {card.suit}:\n {ascii_card}", flush=True)

        width, height = 400, 200
        image = Image.new('RGB', (width, height), color=(255, 255, 255))

        draw = ImageDraw.Draw(image)

        try: 
            font = ImageFont.truetype("arial.ttf", 18)
            print("Loaded font: arial.ttf", flush=True)
        except IOError:
            try: 
                font = ImageFont.truetype("DejaVuSans.ttf", 18)
                print("Loaded fallback font: DejaVuSans.tff", flush=True)
            except IOError:
                font = ImageFont.load_default()
                print("Loaded default font", flush=True)


        y_offset = 10
        for line in ascii_card.split("\n"):
            draw.text((10, y_offset), line, font=font, fill=(0, 0, 0))
            y_offset += 20

        image.save(filename)

        if os.path.exists(filename):
            print(f"Image successfully created: {filename}", flush=True)
        else: 
            print(f"Failed to create image: {filename}", flush=True)

        return filename


#Defining a deck of cards

deck = [Card(suit, value, suit_symbols[suit]) for suit in suits for value in values]


#Function that creates images for each card in the deck

def generate_all_card_images(deck):
    for card in deck:
        generate_card_image(card)
        print(f"Generating image for {card.value} of {card.suit}", flush=True)



@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    #Generate_all_card_images() function call
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        generate_all_card_images(deck)
    app.run(debug=True)