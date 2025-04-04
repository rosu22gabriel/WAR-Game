## War Card Game

A web-based implementation of the classic War card game built with Python (Flask) and JavaScript.

![Game Screenshot](/static/screenshots/gameplay.png)

## Features

- Full deck simulation with 52 cards
- Battle system with War mechanics (ties trigger additional card draws)
- Real-time card count tracking
- Game log showing all moves
- Reset game functionality
- Responsive design for different screen sizes

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python 3, Flask
- **Dependencies**: Pillow (Python Imaging Library)

2. **Setup**:
   ```bash
   # Clone the repository
   git clone https://github.com/rosu22gabriel/WAR-Game.git
   cd war-card-game

    # Create virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate


## WAR-Game – Rules

## 1. Game Setup:
    - A standard 52-card deck (without Jokers) is used.
    The deck is split into two equal halves, with 26 cards for each player.
    - Players cannot see their cards and must always draw the top card from their deck.

## 2. Gameplay:
    - In each round, both players draw one card and compare them:
    - The player with the higher-value card wins the round and takes both cards, placing them at the bottom of their deck.
    - If both cards have the same value, a War begins.

## 3. War Rules:
    - When two cards have the same value, players must draw additional cards:
    - If the initial cards are not J, Q, K, or A, each player draws one extra card, and the winner of that comparison takes all the cards.
    - If the initial cards are J, Q, K, or A, players must draw additional cards based on the rank of the card:
    J (Jack) → 1 extra card
    Q (Queen) → 2 extra cards
    K (King) → 3 extra cards
    A (Ace) → 4 extra cards
    - The last drawn card is compared to determine the winner, who takes all the cards from that round.
    - If this comparison also results in a tie, the process repeats.

4. Special Cases for War:
    - If a player does not have enough cards to continue a War, the game stops:
    - Their last available card is compared with the opponent's.
    - If this card is lower than the opponent's, they lose the game.
    - If this card is equal to the opponent's, the game ends immediately, and the opponent wins.

5. Game Ending Conditions:
    - A player loses when they run out of cards.
    - The opponent is declared the winner of the game.
    
6. Card Value Hierarchy (from lowest to highest):
2, 3, 4, 5, 6, 7, 8, 9, 10, J (Jack), Q (Queen), K (King), 
A (Ace)
