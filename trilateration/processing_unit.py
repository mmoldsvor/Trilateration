from .node import Node
from .vector2D import Vector2D


class ProcessingUnit:
    def __init__(self, nodes, tracking_area):
        """
        Handles all incoming data
        :param nodes: List[Node, Node, ...] -
        :param tracking_area: tuple(x1, y1, x2, y2) - The area where positions can appear
        """
        self.nodes = nodes
        self.tracking_area = tracking_area
        self.position_generator = self.calculate_position()

    @property
    def position(self):
        """
        Creates a position property that updates the position
        :return: Vector2D if successful, None otherwise
        """
        for node in self.nodes:
            node.update_distance()

        next_position = next(self.position_generator)
        if next_position is not None:
            return next_position
        return None

    def calculate_position(self):
        """
        Calculates the average position of the intersections in the tracked area
        :yield: Vector2D(x, y) - yields the position whenever it is available
        """
        while True:
            intersections = self.calculate_intersections()
            points_of_interest = self.compare_points(intersections)
            if not points_of_interest == []:
                point = Vector2D.average_vector(points_of_interest)
                yield point
            else:
                yield None

    def calculate_intersections(self):
        """
        Calculates the intersections and filters out those outside the tracked area
        :return:
        """
        # Loops through the nodes so every node is calculated against each other
        intersections = [Node.intersection(node1, node2) for index, node1 in enumerate(self.nodes)
                         for node2 in self.nodes[index + 1:]]
        return self.track_area_filter(intersections)

    def track_area_filter(self, points):
        """
        Filters out values outside the tracking area
        :param points: List[Vector2D, Vector2D, ...]
        :return:
        """
        result = []
        x1, y1, x2, y2 = self.tracking_area
        for pair in points:
            result.append([Vector2D(x, y) for (x, y) in pair if x1 <= x <= x2 and y1 <= y <= y2])

        return result

    @staticmethod
    def compare_points(points):
        """
        Finds the unique points of interest if more than one intersection point inside tracking area, the single intersection point otherwise
        :param points: List[Vector2D, Vector2D, ...]
        :return: Set(Vector2D, Vector2D, ...) if more than one intersection point inside tracking area, List[Vector2D] otherwise.
        """
        # Checks if comparision is needed
        points_flattened = [point for pairs in points for point in pairs if point is not None]
        if len(points_flattened) <= 1:
            return points_flattened

        result = []
        for index, point1 in enumerate(points):
            for point2 in points[index+1:]:
                for point in ProcessingUnit.closest_points(point1, point2):
                    result.append(point)
        return set(tuple(result))

    @staticmethod
    def closest_points(points1, points2):
        """
        Finds the two closest points from two different lists of Vectors
        :param points1: Vector2D
        :param points2: Vector2D
        :return: List[Vector2D, Vector2D]
        """
        min_dist = None
        points = []
        for point1 in points1:
            for point2 in points2:
                dist = abs(point1-point2)
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    points = [point1, point2]
        return points
