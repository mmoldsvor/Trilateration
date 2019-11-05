from trilateration import *
from visualizer import AnalysisTool

node_left = Node(Vector2D(100, 100), SerialConnection('COM9', 38400, 20))
node_right = Node(Vector2D(400, 100), SerialConnection('COM13', 38400, 20))
node_bottom = Node(Vector2D(250, 400), SerialConnection('COM15', 38400, 20))
processing_unit = ProcessingUnit([node_left, node_right, node_bottom], (100, 100, 400, 400))

while True:
    analysis = AnalysisTool()

    position = processing_unit.position
    analysis.update_display(processing_unit.tracking_area, processing_unit.nodes)

    if position is not None:
        analysis.draw_point(position)

    analysis.update()
