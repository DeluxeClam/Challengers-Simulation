import random
from typing import List


class Card:
    def __init__(self, name: str, power: int) -> None:
        self.name = name
        self.power = power

def sum_card_power(cards: List[Card]):
    total = 0
    for card in cards:
        total += card.power
    return total



class Deck:
    def __init__(self, card_list: dict) -> None:
        self.card_list = card_list
        self.cards = []
        self.bench = []
        self.draw_index = 0

        for card_count in self.card_list.keys():
            for card in self.card_list[card_count]:
                for i in range(int(card_count)):
                    self.add_card(card)
        
        self.shuffle_deck()

    def add_card(self, card: Card):
        self.cards.append(card)

    def shuffle_deck(self):
        random.shuffle(self.cards)
        self.draw_index = 0
        self.bench = []

    def draw_card(self):
        card = self.cards[self.draw_index]
        self.draw_index += 1
        return card


class Game:
    def __init__(self, deck1: Deck, deck2: Deck, verbose: bool = True) -> None:
        self.deck1 = deck1
        self.deck2 = deck2

        self.verbose = verbose

        self.first_player = 1
        self.active_player = self.first_player

        self.defend_power = 0

        self.defender_cards = []

        self.game_on = True

        self.turns_taken = 0

    def randomise_first(self):
        self.first_player = random.randint(1, 2)
        self.active_player = self.first_player
        if self.verbose:
            print(f'Player {self.first_player} will go first.')

    def play_turn(self, attack_deck):
        self.turns_taken += 1
        drawn_cards = []
        attack_power = 0
        attack_loss = False

        if self.verbose:
            print(f'Defend power: {self.defend_power}')
            print(f'Player {self.active_player} cards remaining: {len(attack_deck.cards) - attack_deck.draw_index}')

        while attack_power < self.defend_power or attack_power == 0:

            if attack_deck.draw_index < len(attack_deck.cards):
                drawn_cards.append(attack_deck.draw_card())
                attack_power = sum_card_power(drawn_cards)

            else:
                attack_loss = True
                break

        if self.verbose:
            print('Drawn cards:')
            for card in drawn_cards:
                print(f'{card.name}: {card.power}')
            print(f'Attack power: {attack_power}')

        if attack_loss:
            self.attack_loss()
        else:
            if self.verbose:
                print(f'Power {attack_power} is enough to capture the flag.')
                print(f'Player {self.active_player} will now become the defender.')
            self.become_defender(drawn_cards)

    def become_defender(self, cards: List[Card]):
        
        self.defend_power = cards[-1].power
        
        if self.active_player == 1:
            for card in self.defender_cards:
                if len(set(self.deck2.bench)) < 6:
                    self.deck2.bench.append(card.name)
                else:
                    self.defend_loss()
            self.active_player = 2

        else:
            for card in self.defender_cards:
                if len(set(self.deck1.bench)) < 6:
                    self.deck1.bench.append(card.name)
                else:
                    self.defend_loss()
            self.active_player = 1

        self.defender_cards = cards

    def attack_loss(self):
        self.loser = self.active_player
        if self.active_player == 1:
            self.winner = 2
        else:
            self.winner = 1
        self.game_on = False

        if self.verbose:
            print(f'Player {self.loser} did not have enough cards left to capture the flag from Player {self.winner}.')


    def defend_loss(self):
        if self.active_player == 1:
            self.loser = 2
        else:
            self.loser = 1
        self.winner = self.active_player
        self.game_on = False

        if self.verbose:
            if self.verbose:
                print(f'Player {self.loser} did not have enough slots left on the bench.')

    def play_game(self):
        self.deck1.shuffle_deck()
        self.deck2.shuffle_deck()

        self.defend_power = 0
        self.defender_cards = []
        self.game_on = True
        self.turns_taken = 0

        if self.verbose:
            print(f'Player {self.first_player} will start.')
        while self.game_on:

            if self.active_player == 1:
                attack_deck = self.deck1
            else:
                attack_deck = self.deck2

            self.play_turn(attack_deck)
        
        if self.verbose:
            print(f'Player {self.winner} wins after {self.turns_taken} turns.') 
