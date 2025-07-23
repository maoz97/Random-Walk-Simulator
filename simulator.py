import numpy as np
from walker import *
import matplotlib.pyplot as plt
import os


class Simulator:

    def __init__(self, walker_type, num_simulations, num_steps, obstacles, gates, direction, percents,
                 restart_step, ) -> None:
        """
                Initializes a Simulator object with the provided parameters.

        :param walker_type: The type of walker to simulate.
        :param num_simulations: The number of simulations to run.
        :param num_steps: The number of steps to simulate in each simulation.
        :param obstacles: The obstacles present in the simulation area.
        :param gates: The gates present in the simulation area.
        :param direction: The direction biasing configuration for the walker (if the walker is biased walker).
        :param percents:  The percentage biasing configuration for the walker (if the walker is biased walker).
        :param restart_step: The configuration for restarting steps during simulation.
        """
        self.__walker_type = walker_type
        self.__num_simulations = num_simulations
        self.__num_steps = num_steps
        self.__obstacles = obstacles
        self.__gates = gates
        self.__direction = direction
        self.__percents = percents
        self.restart_step = restart_step
        self.__statistics = {
            "average_distance_from_origin": {},
            "average_time_to_leave_radius_10": {},
            "average_distance_from_y_axis": {},
            "average_distance_from_x_axis": {},
            "crossed_y_axis": {},
            "locations_list": [(0, 0)]
        }

    def run(self) -> None:
        """
        Runs the simulation based on the specified parameters and updates the statistics.

        This method executes the simulation for the specified number of simulations and steps.
        It tracks the walker's movements, checking for obstacles, gates, and restarting steps as necessary.
        During the simulation, it calculates various statistics including average distances from origin,
        average distances from the y-axis and x-axis, crossings of the y-axis, and time taken to leave
        a radius of 10 units from the origin. Finally, it computes averages and updates the statistics.
        :return: None
        """
        # Initialize statistics dictionaries
        self.create_statistics_dict("average_distance_from_origin")
        self.create_statistics_dict("average_distance_from_y_axis")
        self.create_statistics_dict("average_distance_from_x_axis")
        self.create_statistics_dict("crossed_y_axis")
        last_distances_list = []
        time_to_leave_radius_10_list = []

        # Loop through simulations
        for num_simulate in range(self.__num_simulations):
            # Initialize walker and variables for statistics calculation
            walker = Walker()
            time_to_leave_radius_10 = 0
            num_crossed_y_axis = 0
            keep_calculate = True
            last_distance = 0

            # Loop through steps
            for step in range(1, self.__num_steps + 1):
                # Execute walker's move and then check if there is in the new position any special area
                # (like obstacle, gates etc.)
                new_position = self.execute_move(walker)
                new_position = self.check_obstacles(walker, new_position)
                if new_position != walker.get_position():
                    new_position = self.check_gates(walker, new_position)
                new_position = self.check_restart_step(new_position, step)

                old_position = walker.get_position()
                walker.set_position(new_position)
                position = walker.get_position()
                self.__statistics["locations_list"].append(position)
                distance_from_origin = np.linalg.norm(position)

                # Calculate time to leave radius 10 and update last distance
                if distance_from_origin < 10 and keep_calculate:
                    time_to_leave_radius_10 += 1
                    last_distance = distance_from_origin
                    if step in self.__statistics["average_time_to_leave_radius_10"]:
                        self.__statistics["average_time_to_leave_radius_10"][step].append(last_distance)
                    else:
                        self.__statistics["average_time_to_leave_radius_10"][step] = [last_distance]
                elif distance_from_origin > 10:
                    keep_calculate = False

                # Check if y-axis is crossed
                if (old_position[1] > 0 > new_position[1] or old_position[1] < 0 < new_position[1]) and step > 0:
                    num_crossed_y_axis += 1

                # calculate distance from each axis
                if step in self.__statistics["average_distance_from_origin"] and step > 0:
                    distance_from_y_axis = abs(position[0])
                    distance_from_x_axis = abs(position[1])

                    # Update statistics dictionaries
                    self.__statistics["average_distance_from_origin"][step].append(distance_from_origin)
                    self.__statistics["average_distance_from_y_axis"][step].append(distance_from_y_axis)
                    self.__statistics["average_distance_from_x_axis"][step].append(distance_from_x_axis)
                    self.__statistics['crossed_y_axis'][step].append(num_crossed_y_axis)
            last_distances_list.append(last_distance)
            time_to_leave_radius_10_list.append(time_to_leave_radius_10)

        # Compute averages and update statistics
        self.set_statistics_to_average("average_distance_from_origin")
        self.set_statistics_to_average("average_distance_from_y_axis")
        self.set_statistics_to_average("average_distance_from_x_axis")
        self.set_statistics_to_average("crossed_y_axis")
        self.set_statistics_to_average("average_time_to_leave_radius_10")
        self.update_dict_time_to_leave(last_distances_list, time_to_leave_radius_10_list)

    def check_restart_step(self, new_position: tuple[float, float], step: int) -> tuple[float, float]:
        """
         Checks if the current step matches any of the specified restart steps.
        :param new_position: (tuple[float, float]): The current position coordinates.
        :param step: The current step count.
        :return: tuple[float, float]: If the current step matches any restart steps, returns (0, 0)
                            to indicate a restart; otherwise, returns the current position.
        """
        if self.restart_step != "":
            for num in self.restart_step:
                if step == num:
                    result = random.choice([True, False])
                    if result:
                        return 0, 0
            return new_position
        return new_position

    def update_dict_time_to_leave(self, last_distance_list: list, time_to_leave_list: list) -> None:
        """
        This method updates a dictionary with average time-to-leave values as keys and corresponding average distances
        as values, based on provided lists of last distances and time-to-leave values.
        :param last_distance_list: list of all the last locations
        :param time_to_leave_list: list of all the times to leave radius 10
        :return: None
        """
        average_distance = sum(last_distance_list) / len(last_distance_list)
        average_time_to_leave = sum(time_to_leave_list) / len(time_to_leave_list)
        self.__statistics["average_time_to_leave_radius_10"][average_time_to_leave] = average_distance

    def set_statistics_to_average(self, statistic_name: str) -> None:
        """
         Computes the average for each list of numbers in the specified data dictionary and updates it with
         the computed averages.
        :param statistic_name: The key for accessing the data in the statistics dictionary.
        :return: None
        """
        for key in self.__statistics[statistic_name].keys():
            # Get the list of numbers for the current key
            numbers = self.__statistics[statistic_name][key]

            # Compute the average of the numbers
            if numbers:  # Check if the list is not empty to avoid division by zero
                average = sum(numbers) / len(numbers)
                self.__statistics[statistic_name][key] = average
            else:
                # If the list is empty, set the average to 0
                self.__statistics[statistic_name][key] = 0

    def create_statistics_dict(self, statistic_name: str) -> None:
        """
        Creates a dictionary to store statistics with intervals of 5 steps.
        :param statistic_name: The name of the statistics to be stored in the dictionary.
        :return: None
        """
        # Create a dictionary with keys representing intervals of 5 steps
        self.__statistics[statistic_name] = {num: [] for num in range(0, self.__num_steps + 1, 5)}

        # If the total number of steps is not divisible by 5, add the last step as a key
        if self.__num_steps % 5 != 0:
            self.__statistics[statistic_name][self.__num_steps] = self.__num_steps
            # Reinitialize the dictionary with only the new keys added
            self.__statistics[statistic_name] = {key: [] for key in self.__statistics[statistic_name].keys()}

        # Initialize the first key with a list containing 0 to represent the starting step
        self.__statistics[statistic_name][0] = [0]

    def execute_move(self, walker: Walker) -> tuple[float, float]:
        """
        Executes a move for the given walker based on the walker type.
        :param walker: An instance of the walker class.
        :return: tuple[float, float]: The new position after the move.
        """
        # Executes a biased step based on provided direction and percentages
        if self.__walker_type == 4:
            new_position = walker.biased_step(self.__direction, self.__percents)

        # Executes a step with four possible directions
        elif self.__walker_type == 3:
            new_position = walker.four_options_step()

        # Executes a step with random length
        elif self.__walker_type == 2:
            new_position = walker.random_step_length()

        # Executes a step with random direction and length
        else:
            new_position = walker.random_step()
        return new_position

    def check_gates(self, walker: Walker, new_position: tuple[float, float]) -> tuple[float, float]:
        """
        Checks if the walker intersects with any gates and adjusts the position accordingly.
        :param walker: An instance of the walker class.
        :param new_position: (tuple[float, float]): The new position after the move.
        :return: tuple[float, float]: The adjusted new position if intersection with a gate occurs; otherwise,
        the original new position.
        """
        if self.__gates is None:
            return new_position
        else:
            # Iterate through each gate to check for intersection
            for gate in self.__gates:
                gate_area = gate[:-1]

                num_pairs = len(gate_area) // 2
                for i in range(num_pairs - 1):
                    coordinate1 = (gate_area[i * 2], gate_area[i * 2 + 1])
                    coordinate2 = (gate_area[(i + 1) * 2], gate_area[(i + 1) * 2 + 1])
                    if self.are_lines_intersecting(walker.get_position(), new_position, coordinate1, coordinate2):
                        # If intersection occurs, adjust the position to the end of the gate
                        new_position = gate[-1]
                        return new_position
            return new_position

    def check_obstacles(self, walker: Walker, new_position: tuple[float, float]) -> tuple[float, float]:
        """
        Checks if the walker intersects with any obstacles and adjusts the position accordingly.
        :param walker: An instance of the walker class.
        :param new_position: (tuple[float, float]): The new position after the move.
        :return: tuple[float, float]: The adjusted new position if intersection with an obstacle occurs; otherwise,
        the original new position.
        """
        if self.__obstacles is None:
            return new_position
        else:
            x, y = walker.get_position()
            # Iterate through each obstacle to check for intersection
            for obstacle in self.__obstacles:
                coordinate1 = obstacle[:2]
                coordinate2 = obstacle[2:4]
                if self.are_lines_intersecting(walker.get_position(), new_position, coordinate1, coordinate2):
                    # If intersection occurs, keep the walker's position unchanged
                    return x, y
            return new_position

    def are_lines_intersecting(self, line1_point1: tuple[float, float], line1_point2:  tuple[float, float],
                               line2_point1:  tuple[float, float], line2_point2:  tuple[float, float]) -> bool:
        """
           Check if two line segments defined by their endpoints intersect.
           :param line1_point1: Tuple (x, y) representing the first endpoint of the first line segment.
           :param line1_point2: Tuple (x, y) representing the second endpoint of the first line segment.
           :param line2_point1: Tuple (x, y) representing the first endpoint of the second line segment.
           :param line2_point2: Tuple (x, y) representing the second endpoint of the second line segment.
           :return: True if the line segments intersect, False otherwise.
           """
        # Find orientations for each pair of points
        o1 = self.orientation(line1_point1, line1_point2, line2_point1)
        o2 = self.orientation(line1_point1, line1_point2, line2_point2)
        o3 = self.orientation(line2_point1, line2_point2, line1_point1)
        o4 = self.orientation(line2_point1, line2_point2, line1_point2)

        # General case: if orientations are different, then the lines intersect
        if o1 != o2 and o3 != o4:
            return True

        # Special cases for collinear points
        if o1 == 0 and self.is_on_segment(line1_point1, line2_point1, line1_point2):
            return True
        if o2 == 0 and self.is_on_segment(line1_point1, line2_point2, line1_point2):
            return True
        if o3 == 0 and self.is_on_segment(line2_point1, line1_point1, line2_point2):
            return True
        if o4 == 0 and self.is_on_segment(line2_point1, line1_point2, line2_point2):
            return True

        return False

    def orientation(self, p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> int:
        """
            Determine the orientation of three points: clockwise, counterclockwise, or collinear.
            :param p: Tuple (x, y) representing the first point.
            :param q: Tuple (x, y) representing the second point.
            :param r: Tuple (x, y) representing the third point.
            :return: 0 if the points are collinear, 1 if clockwise, and 2 if counterclockwise.
            """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # collinear
        return 1 if val > 0 else 2  # clockwise or counterclockwise

    def is_on_segment(self, p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> bool:
        """
        Check if point 'p' lies on the line segment defined by points 'q' and 'r'.
        :param p: Tuple (x, y) representing the point to check.
        :param q: Tuple (x, y) representing one endpoint of the line segment.
        :param r: Tuple (x, y) representing the other endpoint of the line segment.
        :return: True if point 'p' lies on the line segment, False otherwise.
        """
        return min(q[0], r[0]) <= p[0] <= max(q[0], r[0]) and min(q[1], r[1]) <= p[1] <= max(q[1], r[1])

    def save_results(self) -> None:
        """
        Saves the statistics to a text file named 'results.txt' in the current directory.
        :return: None
        """
        # Generate file name
        file_name = 'results.txt'

        # Get current directory
        current_directory = os.getcwd()

        # Construct full file path
        file_path = os.path.join(current_directory, file_name)

        # Write statistics to the file
        with open(file_path, 'w') as file:
            for key, value in self.__statistics.items():
                file.write(f"{key}:\n")
                # Check if the value is a list or a single value
                if isinstance(value, list):
                    for item in value:
                        file.write(f"{item}\n")
                else:
                    file.write(f"{value}\n")
                file.write("\n")

    def plot_all_results(self) -> None:
        """
        Plots all the results and saves the plots in the current directory.
        :return: None
        """
        # Get the current directory
        directory_path = os.getcwd()

        # Plot graphs for all results
        self.plot_graph_1(self.__num_steps, directory_path)
        self.plot_graph_2(directory_path)
        self.plot_graph_3(self.__num_steps, directory_path)
        self.plot_graph_4(self.__num_steps, directory_path)
        self.plot_graph_5(self.__num_steps, directory_path)

    def plot_graph_1(self, num_steps: int, directory_path: str) -> None:
        """
        Plots the graph of average distance from the origin at each step and saves it as 'graph_1.png'.
        :param num_steps: (int): The total number of steps.
        :param directory_path: (str): The path to the directory where the plot will be saved
        :return: None
        """
        # Extract data for plotting
        list_steps = list(self.__statistics['average_distance_from_origin'].keys())
        list_average_distance = [self.__statistics['average_distance_from_origin'][key] for key in
                                 self.__statistics['average_distance_from_origin']]

        # Plot the graph
        plt.plot(list_steps, list_average_distance, marker='o', color='blue')
        plt.title('Average Distance at {} Steps'.format(num_steps))
        plt.xlabel('Number of Steps')
        plt.ylabel('Average Distance from origin')
        plt.grid(True)

        # Save the plot
        file_path = os.path.join(directory_path, 'graph_1.png')
        plt.savefig(file_path)
        plt.close()

    def plot_graph_2(self, directory_path: str) -> None:
        """
        Plots the graph of time to leave radius 10 as a function of average distance from the beginning of the axis
        and saves it as 'graph_2.png'.
        :param directory_path: (str): The path to the directory where the plot will be saved
        :return:
        """
        list_time_to_leave = list(self.__statistics['average_time_to_leave_radius_10'].keys())
        list_average_distance = [self.__statistics['average_time_to_leave_radius_10'][key] for key in
                                 self.__statistics['average_time_to_leave_radius_10']]
        plt.plot(list_time_to_leave, list_average_distance, marker='o', color='blue')
        plt.title('average distance from beginning of axis smaller than 10 VS average time ')
        plt.xlabel(f'Average time to leave radius 10: {list_time_to_leave[-1]}')
        plt.ylabel('Average distance from beginning of axis')
        plt.grid(True)
        file_path = os.path.join(directory_path, 'graph_2.png')
        plt.savefig(file_path)
        plt.close()

    def plot_graph_3(self, num_steps: int, directory_path: str) -> None:
        """
        Plots the graph of average distance from the y axis at each step and saves it as 'graph_3.png'.
        :param num_steps: (int): The total number of steps.
        :param directory_path: (str): The path to the directory where the plot will be saved
        :return: None
        """
        # Extract data for plotting
        list_steps = list(self.__statistics['average_distance_from_y_axis'].keys())
        list_average_distance = [self.__statistics['average_distance_from_y_axis'][key] for key in
                                 self.__statistics['average_distance_from_y_axis']]

        # Plot the graph
        plt.plot(list_steps, list_average_distance, marker='o', color='blue')
        plt.title('Average Distance from y axis at {} Steps'.format(num_steps))
        plt.xlabel('Number of Steps')
        plt.ylabel('Average_distance_from_y_axis')
        plt.grid(True)

        # Save the plot
        file_path = os.path.join(directory_path, 'graph_3.png')
        plt.savefig(file_path)
        plt.close()

    def plot_graph_4(self, num_steps: int, directory_path: str) -> None:
        """
        Plots the graph of average distance from the x axis at each step and saves it as 'graph_4.png'.
        :param num_steps: (int): The total number of steps.
        :param directory_path: (str): The path to the directory where the plot will be saved
        :return: None
        """
        # Extract data for plotting
        list_steps = list(self.__statistics['average_distance_from_x_axis'].keys())
        list_average_distance = [self.__statistics['average_distance_from_x_axis'][key] for key in
                                 self.__statistics['average_distance_from_x_axis']]

        # Plot the graph
        plt.plot(list_steps, list_average_distance, marker='o', color='blue')
        plt.title('Average_distance_from_x_axis at {} Steps'.format(num_steps))
        plt.xlabel('Number of Steps')
        plt.ylabel('Average_distance_from_x_axis')
        plt.grid(True)

        # Save the plot
        file_path = os.path.join(directory_path, 'graph_4.png')
        plt.savefig(file_path)
        plt.close()

    def plot_graph_5(self, num_steps: int, directory_path: str) -> None:
        """
        Plots the graph of average number of times Y axis crossed at each step and saves it as 'graph_5.png'.
        :param num_steps: (int): The total number of steps.
        :param directory_path: (str): The path to the directory where the plot will be saved
        :return: None
        """
        # Extract data for plotting
        list_steps = list(self.__statistics['crossed_y_axis'].keys())
        list_average_distance = [self.__statistics['crossed_y_axis'][key] for key in
                                 self.__statistics['crossed_y_axis']]

        # Plot the graph
        plt.plot(list_steps, list_average_distance, marker='o', color='blue')
        plt.title('crossed_y_axis at {} Steps'.format(num_steps))
        plt.xlabel('Number of Steps')
        plt.ylabel('Average number of times Y axis crossed')
        plt.grid(True)

        # Save the plot
        file_path = os.path.join(directory_path, 'graph_5.png')
        plt.savefig(file_path)
        plt.close()

    def plot_crystal_graph(self, directory_path: str) -> None:

        all_locations = []
        for cur_list in self.__statistics["locations_list"]:
            all_locations.append(cur_list)

        # Extract x and y
        all_x, all_y = zip(*all_locations)

        # Plot crystal graph
        plt.scatter(all_x, all_y, c=range(len(all_x)), cmap='coolwarm', s=50)
        plt.annotate('Start', (all_x[0], all_y[0]))
        plt.axis('equal')
        plt.grid()
        plt.title('Crystal Random Walk Graph')

        # Save the plot
        file_path = os.path.join(directory_path, 'crystal_graph.png')
        plt.savefig(file_path)
        plt.close()
