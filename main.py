'''
Chcę

'''

from models.card import Card
from models.deck import Deck
from models.player import Player

def main():
    example_deck = Deck()
    example_deck.shuffle()

    player1 = Player("Alice")
    player2 = Player("Bob")
    players = [player1, player2]
    example_deck.deal(players, 5)

    for player in players:
        print(player.show_hand())

    example_deck.draw_for_player(player1)
    print(player1.show_hand())


if __name__ == "__main__":
    main()
