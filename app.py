import os
import re
import random 
from flask import Flask, render_template, session, jsonify
from PIL import Image, ImageDraw, ImageFont
from collections import deque
from datetime import timedelta


app = Flask(__name__)
app.secret_key = os.urandom(24) 
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_TYPE'] = 'filesystem'
 
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suit_symbols = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
    '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

#Defining a class for card
class Card:
    def __init__(self, suit, value, symbol):
        self.suit = suit
        self.value = value
        self.symbol = symbol

    def to_dict(self):
        return {
            'suit': self.suit,
            'value': self.value,
            'symbol': self.symbol
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['suit'], data['value'], data['symbol'])


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
        print(f"Generated image for {card.value} of {card.suit}:\n {ascii_card}", flush=True)

        width, height = 150, 200
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        try: 
            value_font = ImageFont.truetype("arial.ttf", 24)
            symbol_font = ImageFont.truetype("arial.ttf", 48)
            print("Loaded font: arial.ttf", flush=True)
        except IOError:
            try: 
                value_font = ImageFont.truetype("DejaVuSans.ttf", 24)
                symbol_font = ImageFont.truetype("DejaVuSans.ttf", 48)
                print("Loaded fallback font: DejaVuSans.ttf", flush=True)
            except IOError:
                value_font = ImageFont.load_default()
                symbol_font = ImageFont.load_default()
                print("Loaded default font", flush=True)

        draw.text((10, 10), str(card.value), font=value_font, fill=(0, 0, 0))

        symbol_bbox = draw.textbbox((0, 0), card.symbol, font=symbol_font)
        symbol_width = symbol_bbox[2] - symbol_bbox[0]
        symbol_height = symbol_bbox[3] - symbol_bbox[1]
        draw.text(((width - symbol_width) // 2, (height - symbol_height) // 2), card.symbol, font=symbol_font, 
                  fill=(255, 0, 0) if card.suit in ["Hearts", "Diamonds"] else (0, 0, 0) )


        #y_offset = 10
        #for line in ascii_card.split("\n"):
            #draw.text((10, y_offset), line, font=font, fill=(0, 0, 0))
            #y_offset += 20

        rotated_value = Image.new('RGBA', (30, 30))
        rotated_draw = ImageDraw.Draw(rotated_value)
        rotated_draw.text((0, 0), str(card.value), font=value_font, fill=(0, 0, 0))
        rotated_value = rotated_value.rotate(180)
        image.paste(rotated_value, (width - 40, height -40), rotated_value)

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


class WarGame:
    def __init__(self):
        self.deck = deck
        random.shuffle(self.deck)
        self.player1 = deque(self.deck[:26])
        self.player2 = deque(self.deck[26:])
        self.pot = []
        self.war_count = 0
        self.game_log = []
        self.battle_cards = []

    def to_dict(self):
        return {
            'player1': [card.to_dict() for card in self.player1],
            'player2': [card.to_dict() for card in self.player2],
            'pot': [card.to_dict() for card in self.pot],
            'war_count': self.war_count,
            'game_log': self.game_log,
            'battle_cards': [card.to_dict() for card in self.battle_cards]
        }
    
    @classmethod
    def from_dict(cls, data):
        game = cls()
        game.player1 = deque([Card.from_dict(c) for c in data.get('player1', [])])
        game.player2 = deque([Card.from_dict(c) for c in data.get('player2', [])])
        game.pot = [Card.from_dict(c) for c in data.get('pot', [])]
        game.war_count = data.get('war_count', 0)
        game.game_log = data.get('game_log', [])
        game.battle_cards = [Card.from_dict(c) for c in data.get('battle_cards', [])]
        return game

    def log(self, message):
        self.game_log.append(message)


    def game_over(self):
        return len(self.player1) == 0 or len(self.player2) == 0

def play_round(self):
    if self.game_over():
        return

    try:
        # Draw initial cards
        p1_card = self.player1.popleft()
        p2_card = self.player2.popleft()
        self.battle_cards = [p1_card, p2_card]
        self.pot.extend(self.battle_cards)
        
        self.log(f"Player 1 plays {p1_card.value} of {p1_card.suit}")
        self.log(f"Player 2 plays {p2_card.value} of {p1_card.suit}")

        # Compare card values
        if CARD_VALUES[p1_card.value] > CARD_VALUES[p2_card.value]:
            self.resolve_round(winner=1)
        elif CARD_VALUES[p2_card.value] > CARD_VALUES[p1_card.value]:
            self.resolve_round(winner=2)
        else:
            # Cards are equal - war begins
            self.start_war(p1_card.value)
            
    except IndexError:
        self.handle_game_over()
    
    # Debug output
    print("Round result:", {
        'p1_count': len(self.player1),
        'p2_count': len(self.player2),
        'battle_cards': [f"{card.value}_{card.suit}.png" for card in self.battle_cards]
    }, flush=True)

def start_war(self, initial_card_value):
    """Handle a war scenario when cards of equal value are drawn."""
    self.log(f"\n⚔️ WAR! Both players drew {initial_card_value}")
    
    # Determine how many cards to draw based on the initial card value
    war_cards_to_draw = 0
    if initial_card_value in ['J', 'Q', 'K', 'A']:
        war_cards_to_draw = {
            'J': 1,
            'Q': 2,
            'K': 3,
            'A': 4
        }[initial_card_value]
    else:
        war_cards_to_draw = 1  # For non-face cards
    
    # Each player adds the required number of face-down cards to the pot
    for _ in range(war_cards_to_draw):
        if len(self.player1) > 0:
            self.pot.append(self.player1.popleft())
        if len(self.player2) > 0:
            self.pot.append(self.player2.popleft())
    
    # Check if players have cards left for the final comparison
    if len(self.player1) == 0 or len(self.player2) == 0:
        self.handle_game_over()
        return
    
    # Draw final comparison cards
    p1_war_card = self.player1.popleft()
    p2_war_card = self.player2.popleft()
    self.battle_cards = [p1_war_card, p2_war_card]
    self.pot.extend(self.battle_cards)
    
    self.log(f"Player 1 reveals: {p1_war_card.value} of {p1_war_card.suit}")
    self.log(f"Player 2 reveals: {p2_war_card.value} of {p2_war_card.suit}")
    
    # Compare the war cards
    if CARD_VALUES[p1_war_card.value] > CARD_VALUES[p2_war_card.value]:
        self.resolve_round(winner=1)
    elif CARD_VALUES[p2_war_card.value] > CARD_VALUES[p1_war_card.value]:
        self.resolve_round(winner=2)
    else:
        # Another war if tied again
        self.start_war(p1_war_card.value)

def resolve_round(self, winner):
    """Award all cards in the pot to the winning player."""
    winner_deck = self.player1 if winner == 1 else self.player2
    random.shuffle(self.pot)  # Shuffle before adding to winner's deck
    winner_deck.extend(self.pot)
    self.log(f"Player {winner} wins the round and {len(self.pot)} cards!")
    self.pot.clear()
    self.battle_cards = []
    self.check_winner()

def handle_game_over(self):
    """Handle game over when a player runs out of cards."""
    if len(self.player1) == 0:
        self.log("\n🎉 Player 2 wins the game!")
    elif len(self.player2) == 0:
        self.log("\n🎉 Player 1 wins the game!")
    self._game_over = True

def check_winner(self):
    """Check if a player has won the game."""
    if len(self.player1) == 0:
        self.log("\n🏆 PLAYER 2 WINS THE GAME!")
    elif len(self.player2) == 0:
        self.log("\n🏆 PLAYER 1 WINS THE GAME!")
    # def play_round(self):
    #     if self.game_over():
    #         return    

    #     try: 
    #         p1_card = self.player1.popleft()
    #         p2_card = self.player2.popleft()
    #         self.battle_cards = [p1_card, p2_card]
    #         self.pot.extend(self.battle_cards)
    #         self.log(f"Player 1 plays {p1_card.value} of {p1_card.suit}")
    #         self.log(f"Player 2 plays {p2_card.value} of {p2_card.suit}")

    #         if CARD_VALUES[p1_card.value] > CARD_VALUES[p2_card.value]:
    #             self.resolve_round(winner = 1)
    #         elif CARD_VALUES[p2_card.value] > CARD_VALUES[p1_card.value]:
    #             self.resolve_round(winner = 2)
    #         else: 
    #             self.start_war(p1_card.value)
    #     except IndexError:
    #         self.handle_game_over()
    #     print("Sent response:", { 
    #         'p1_count': len(self.player1),
    #         'p2_count': len(self.player2),
    #         'battle_cards': [f"{card.value}_{card.suit}.png"
    #                          for card in self.battle_cards]
    #     }, flush=True)
        

    
    # def resolve_round(self, winner):
    #     winner_deck = self.player1 if winner == 1 else self.player2
    #     random.shuffle(self.pot)
    #     winner_deck.extend(self.pot)
    #     self.log(f"\nPlayer {winner} wins the round")
    #     self.pot.clear()
    #     self.battle_cards = []
    #     self.check_winner()


    # def check_winner(self):
    #     if len(self.player1) == 0:
    #         self.log("\n PLAYER 1 WINS THE GAME! ")
    #     elif len(self.player2) == 0:
    #         self.log("\n PLAYER 2 WINS BY DEFAULT ")


    # def log(self, message):
    #     self.game_log.append(message)


    # def game_over(self):
    #     return len(self.player1) == 0 or len(self.player2) == 0


@app.route("/")
def home():
    if 'game' not in session or not session['game']:
        game = WarGame()
        session['game'] = game.to_dict()
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play_round():
    game_data = session.get('game', {})
    if not game_data or not isinstance(game_data, dict) or 'player1' not in game_data:
        game = WarGame()
        print("New game initialized")
    else:
        game = WarGame.from_dict(game_data)
        print("Existing game loaded")

    if not game.game_over():
        print("Playing round...")
        game.play_round()
        print(f"After play_round(): P1 = cards ={len(game.player1)}, P2 card s={len(game.player2)}")
        print(f"Battle cards: {game.battle_cards}")
        print(f"Game log: {game.game_log[-1:]}")
        session['game'] = game.to_dict()
        session.modified = True
        print("Game state saved")

    return jsonify({ 
        'p1_count': len(game.player1), 
        'p2_count': len(game.player2),
        'log': "<br>".join(game.game_log[-5:]),
        'battle_cards': [
            f"{card.value}_{card.suit}.png"
            for card in game.battle_cards
        ]
    })

@app.route("/reset", methods=['POST'])
def reset_game():
    session.clear()
    #return home()
    return jsonify({"status": "Game reset"})

@app.route("/state")
def game_state():
    return jsonify({ 
        'p1_count': len(session.get('game', {}).get('player1', [])),
        'p2_count': len(session.get('game', {}).get('player2', []))
    })

if __name__ == "__main__":    
    if not os.path.exists('static/cards'):
        os.makedirs('static/cards')    
    generate_all_card_images(deck)
    app.run(debug=True)