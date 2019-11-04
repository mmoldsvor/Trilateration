from trilateration import Node


class BLENode(Node):
    def __init__(self, position, connection, measured_power=-50, default_distance=100):
        """
        A Node which supports BLE and rssi to distance conversion
        :param measured_power: The RSSI measured at 1 meter
        """
        super().__init__(position, connection, default_distance)
        self.measured_power = measured_power

    def filter_data(self):
        """
        Filters data points into a single usable value
        :return: int, rssi if data points are present, None otherwise
        """
        # Add kalman or other filter here
        # Currently using average filter
        if len(self.connection.data_points) > 0:
            return sum(self.connection.data_points) / len(self.connection.data_points)
        return 0

    def update_distance(self):
        """
        Updates distance and performs filtering in MainThread to avoid unnecessary workload on SerialThread
        """
        if self.connection.connected:
            filtered_data = self.filter_data()
            self.distance = self.rssi_to_distance(filtered_data, 2)
        else:
            self.distance = self.default_distance

    def rssi_to_distance(self, rssi, constant=3):
        """
        Converts from rssi to distance
        :param rssi: int, current RSSI
        :param constant: int, Environmental factor normally in the range of [2, 4]
        :return: int, distance measured in meters
        """
        return 10 ** ((self.measured_power - rssi) / (10 * constant))
