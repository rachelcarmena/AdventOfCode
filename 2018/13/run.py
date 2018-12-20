#!/usr/bin/python
from enum import Enum

INTERSECTION = '+'
CURVE_NW_SE = '/'
CURVE_NE_SW = '\\'

class Decision(Enum):

    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

    def next(self):
        return Decision((self.value + 1) % 3)

class CartSymbol(Enum):

    UP = '^'
    DOWN = 'v'
    RIGHT = '>'
    LEFT = '<'

    def next_from(self, found_symbol, decision):
        if found_symbol == INTERSECTION:
            if decision == Decision.LEFT: return self.__left()
            if decision == Decision.STRAIGHT: return self
            if decision == Decision.RIGHT: return self.__right()
        if found_symbol == CURVE_NW_SE:
            if self == self.LEFT: return self.DOWN
            if self == self.RIGHT: return self.UP
            if self == self.UP: return self.RIGHT
            if self == self.DOWN: return self.LEFT
        if found_symbol == CURVE_NE_SW:
            if self == self.LEFT: return self.UP
            if self == self.RIGHT: return self.DOWN
            if self == self.UP: return self.LEFT
            if self == self.DOWN: return self.RIGHT
        return self

    def __left(self):
        if self == self.RIGHT: return self.UP
        if self == self.UP: return self.LEFT
        if self == self.LEFT: return self.DOWN
        if self == self.DOWN: return self.RIGHT

    def __right(self):
        if self == self.RIGHT: return self.DOWN
        if self == self.DOWN: return self.LEFT
        if self == self.LEFT: return self.UP
        if self == self.UP: return self.RIGHT

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def beforeThat(self, another_point):
        if (self.y == another_point.y):
            return self.x - another_point.x
        return self.y - another_point.y

    def left(self):
        self.x = self.x - 1

    def right(self):
        self.x = self.x + 1

    def up(self):
        self.y = self.y - 1

    def down(self):
        self.y = self.y + 1

    def __eq__(self, another_element):
        return self.x == another_element.x and self.y == another_element.y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

class Mine:

    def __init__(self, filename):
        self.data = []
        for row in open('input.txt'):
            self.data.append(row)

    def get_symbol_from(self, position):
        return self.data[position.y][position.x]

    def get_carts(self):
        carts = []
        for y in range(len(self.data)):
            for x, symbol in enumerate(self.data[y]):
                if symbol in [cart_symbol.value for cart_symbol in CartSymbol]:
                    carts.append(Cart(Point(x, y), CartSymbol(symbol), Decision.RIGHT))
        return Carts(carts)

class Cart:

    def __init__(self, point, symbol, last_decision):
        self.position = point
        self.symbol = symbol
        self.last_decision = last_decision
        self.alive = True
    
    def update_position(self):
        if self.symbol == CartSymbol.LEFT: self.position.left()
        if self.symbol == CartSymbol.RIGHT: self.position.right()
        if self.symbol == CartSymbol.UP: self.position.up()
        if self.symbol == CartSymbol.DOWN: self.position.down()

    def update_decision_and_symbol(self, found_symbol):
        if found_symbol == INTERSECTION:
            self.last_decision = self.last_decision.next()
        if found_symbol in [INTERSECTION, CURVE_NW_SE, CURVE_NE_SW]:
            self.symbol = self.symbol.next_from(found_symbol, self.last_decision)

    def crash(self):
        self.alive = False
        return self

    def __repr__(self):
        return "[CART: {0}, {1}, {2}]".format(self.position, self.symbol, self.last_decision)
        
class Carts:    

    def __init__(self, carts):
        self.data = carts

    def __order_for_the_tick(self):
        self.data = sorted(self.data, lambda a,b: a.position.beforeThat(b.position))
    
    def __exist_position(self, position):
        found_carts = filter(lambda cart: cart.alive and (cart.position == position), self.data)    
        return len(found_carts) > 1
                
    def __crash_carts_with_position(self, position):
        self.data = map(lambda cart: cart.crash() if (cart.position == position) else cart, self.data)

    def tick_in(self, mine):
        self.__order_for_the_tick()
        for cart in carts.data:
            if not cart.alive: continue
            cart.update_position()
            
            if self.__exist_position(cart.position):
                print "Crash! Position: " + str(cart.position)
                self.__crash_carts_with_position(cart.position)
                continue
        
            found_symbol = mine.get_symbol_from(cart.position)
            cart.update_decision_and_symbol(found_symbol)
        return self 

    def get_survivors(self):
        return Carts(filter(lambda cart: cart.alive, self.data))
    
    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data)


if __name__ == "__main__":
    
    mine = Mine('input.txt')
    carts = mine.get_carts()
    survivors = carts
    while len(survivors) > 1:
        carts = carts.tick_in(mine)
        survivors = carts.get_survivors()
    print "Last survivor: " + str(survivors)
