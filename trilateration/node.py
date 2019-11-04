from trilateration.vector2D import Vector2D

import math
import serial
import threading
import collections


class ConnectionHandler:
    def __init__(self, filter_sample):
        self.filter_sample = filter_sample
        self.data_points = collections.deque([], filter_sample)
        self.connected = False


class SerialConnection(ConnectionHandler):
    def __init__(self, serial_port, baud_rate, filter_sample=1):
        super().__init__(filter_sample)

        try:
            # Starts a serial thread if the serial port is available
            self.serial = serial.Serial(serial_port, baudrate=baud_rate)
            threading.Thread(target=self.serial_thread).start()
            self.connected = True
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
                self.data_points.appendleft(float(self.serial.readline()))
            except ValueError:
                print('INITIALIZING')


class Node:
    def __init__(self, position, connection, default_distance=100):
        """
        A Node network element
        :param position: Vector2D - The position of the Node in relation to the top left corner in centimeters
        :param connection: ConnectionHandler - The type of connection to read data from
        """
        self.position = position
        self.connection = connection
        self.default_distance = default_distance

        self.distance = 0

    def filter_data(self):
        """
        Filters data points into a single useable value
        :return: int, distance if data points are present, None otherwise
        """
        if len(self.connection.data_points) > 0:
            return sum(self.connection.data_points) / len(self.connection.data_points)
        return 0

    def update_distance(self):
        """
        Updates distance and performs filtering in MainThread to avoid unnecessary workload on SerialThread
        """
        if self.connection.connected:
            self.distance = self.filter_data()
        else:
            self.distance = self.default_distance

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
