from trilateration import *


class BLENode(Node):
    def serial_thread(self):
        while True:
            try:
                # Reads RSSI from serial
                self.data_points.appendleft(int(self.serial.readline()))
            except ValueError:
                print('INITIALIZING')

    def rssi_to_distance(self, measured_power, rssi, N):
        """
        Converts from rssi to distance
        :param measured_power: int, The RSSI measured at 1 meter
        :param rssi: int, current RSSI
        :param N: int, Environmental factor normally in the range of [2, 4]
        :return: int, distance measured in meters
        """
        return 10^((measured_power - rssi)/(10*N))


    def filter_data(self):
        """
        Filters data points into a single useable value
        :return: int, rssi if data points are present, None otherwise
        """
        # Add kalman or other filter here
        # Currently using average filter
        if len(self.data_points) > 0:
            return sum(self.data_points) / len(self.data_points)
        return None


    def update_distance(self):
        """
        Updates distance and performs filtering in MainThread to avoid unnecessary workload on SerialThread
        """
        if self.serial is not None:
            filtered_data = self.filter_data()
            self.distance = self.rssi_to_distance(-50, filtered_data, 2)
        else:
            self.distance = Node.DEFAULT_DISTANCE
