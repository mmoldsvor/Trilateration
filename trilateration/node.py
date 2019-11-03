from .vector2D import Vector2D

import math
import serial
import threading
import collections


class Node:
    DEFAULT_DISTANCE = 300

    def __init__(self, position, serial_port, filter_sample=1):
        """
        A Node network element
        :param position: Vector2D - The position of the Node in relation to the top left corner in centimeters
        :param serial_port: str - Serial port to read data from
        :param filter_sample: int - The amount of data points to sample when filtering distance
        """
        self.position = position
        self.distance = 0

        self.filter_sample = filter_sample
        self.data_points = collections.deque([], filter_sample)

        self.serial_port = serial_port

        try:
            # Starts a serial thread if the serial port is available
            self.serial = serial.Serial(serial_port, baudrate=115200)
            threading.Thread(target=self.serial_thread).start()
        except serial.serialutil.SerialException as ex:
            self.serial = None
            print(ex)

    def serial_thread(self):
        """
        A Thread that reads data from Serial Port and appends it to a data_point collections.deque
        with a fixed length equal to the filter_sample variable
        """
        while True:
            try:
                self.data_points.appendleft(int(self.serial.readline()))
            except ValueError:
                print('INITIALIZING')

    def filter_data(self):
        """
        Filters data points into a single useable value
        :return: int, distance if data points are present, None otherwise
        """
        if len(self.data_points) > 0:
            return sum(self.data_points) / len(self.data_points)
        return None

    def update_distance(self):
        """
        Updates distance and performs filtering in MainThread to avoid unnecessary workload on SerialThread
        """
        if self.serial is not None:
            self.distance = self.filter_data()
        else:
            self.distance = Node.DEFAULT_DISTANCE

    @staticmethod
    def intersection(node1, node2):
        """
        Calculates the intersection between two nodes and their distances.
        :param node1: Node
        :param node2: Node
        :return: Vector2D - intersection point if exists
        """
        distance = abs(node1.position - node2.position)
        intersections = []

        # Checks if the circles intersects
        if node1.distance + node2.distance > distance > abs(node1.distance - node2.distance):
            a = (node1.distance ** 2 - node2.distance ** 2 + distance ** 2) / (2 * distance)
            h = math.sqrt(node1.distance * node1.distance - a * a)
            midpoint = node1.position + ((node2.position - node1.position) * (a / distance))

            for sign in (-1, 1):
                x = midpoint.x + sign * h * (node2.position.y - node1.position.y) / distance
                y = midpoint.y - sign * h * (node2.position.x - node1.position.x) / distance
                intersections.append(Vector2D(x, y))

        return intersections
