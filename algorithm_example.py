from trilateration import Node, ProcessingUnit, Vector2D, SerialConnection


def pick_first(processing_unit):
    """
    DO NOT USE FOR POSITIONING
    Just a basic algorithm that picks the first intersection it can find
    :return: Vector()
    """
    intersections = processing_unit.calculate_intersections()
    return intersections[0]


node_left = Node(Vector2D(0, 0), SerialConnection('COM9', 38400, 20))
node_right = Node(Vector2D(100, 0), SerialConnection('COM13', 38400, 20))
processing_unit = ProcessingUnit([node_left, node_right], (0, 0, 100, 100), algorithm_function=pick_first)

while True:
    position = processing_unit.position
    print(node_left.distance, node_right.distance)
    if position is not None:
        print(position)
