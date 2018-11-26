from engine import Board, BoardMovements

b = Board(4, 2)
b.insert_random(5)
print(b)

print()
x = b.move_all(BoardMovements.RIGHT)
print(b)
print(x)
