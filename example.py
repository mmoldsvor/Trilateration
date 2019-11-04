from trilateration import Node, ProcessingUnit, Vector2D

node_left = Node('COM2', Vector2D(0, 0))
node_right = Node('COM2', Vector2D(100, 0))
processing_unit = ProcessingUnit([node_left, node_right], (0, 0, 100, 100))

# Get the position
while True:
    position = processing_unit.position
    if position is not None:
        print(position)
