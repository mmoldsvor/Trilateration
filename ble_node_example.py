from trilateration import Node


class BLENode(Node):
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
            self.distance = self.rssi_to_distance(-50, filtered_data, 2)
        else:
            self.distance = self.default_distance

    @staticmethod
    def rssi_to_distance(measured_power, rssi, constant=3):
        """
        Converts from rssi to distance
        :param measured_power: int, The RSSI measured at 1 meter
        :param rssi: int, current RSSI
        :param constant: int, Environmental factor normally in the range of [2, 4]
        :return: int, distance measured in meters
        """
        return 10 ** ((measured_power - rssi) / (10 * constant))
