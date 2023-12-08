from collections import Counter


class Card:
    symbols = "23456789TJQKA"

    def __init__(self, symbol):
        self._symbol = symbol
        self._ordinality = Card.symbols.index(symbol)

    def __str__(self):
        return self._symbol

    def __lt__(self, other):
        return self._ordinality < other._ordinality


class Hand:
    types = {
        (1, 1, 1, 1, 1): 0,  # High card
        (1, 1, 1, 2): 1,  # One pair
        (1, 2, 2): 2,  # Two pair
        (1, 1, 3): 3,  # Three of a kind
        (2, 3): 4,  # Full house
        (1, 4): 5,  # Four of a kind
        (5,): 6,  # Five of a kind
    }

    def __init__(self, symbols, bid):
        if not len(symbols) == 5:
            raise ValueError("Hand must contain five cards")
        self.bid = bid
        self._cards = [Card(s) for s in symbols]
        self._type_id = tuple(sorted(Counter(list(symbols)).values()))
        self._value = Hand.types[self._type_id]

    def __lt__(self, other):
        if self._value < other._value:
            return True
        if self._value == other._value:
            for c in zip(self._cards, other._cards):
                if c[0] < c[1]:
                    return True
                if c[1] < c[0]:
                    break
        return False


if __name__ == "__main__":
    with open("Advent of Code/Day_7/input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    hands = sorted([Hand(s.split()[0], int(s.split()[1])) for s in lines])
    print(sum((i + 1) * h.bid for i, h in enumerate(hands)))