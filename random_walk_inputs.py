import json
import os
from typing import List


class Inputs:
    """
    this class get the inputs for the random walk simulator.
    the class get a path and checking it, then open the json file
    use some methods in order to read the config file and finally
    check all the parameters in the json file.
    """

    def __init__(self, config_file_path: str) -> None:
        """
         the constructor the class.
         except getting: config_file_path,string representing the file path
        """
        self.config_file_path = config_file_path
        self.config = {}
        self.error_messages = []

    def get_error_messages(self) -> List[str]:
        return self.error_messages

    def parse_config_file(self) -> bool:
        """
        Parse the configuration file and store the content in self.config.
        :return: bool: True if the configuration file is successfully parsed and stored, False otherwise.
        """
        # check if the path is valid:

        if not self.config_file_path:
            self.error_messages.append("File path is empty.")
            return False
        if not os.path.exists(self.config_file_path):
            self.error_messages.append("File path does not exist.")
            return False
        if not os.path.isfile(self.config_file_path):
            self.error_messages.append("Path does not point to a file.")
            return False
        try:
            with open(self.config_file_path, 'r') as f:
                data = json.load(f)
                self.config = data
            return True
        except FileNotFoundError:
            self.error_messages.append(f"Error: File '{self.config_file_path}' not found.")
            return False
        except json.JSONDecodeError:
            self.error_messages.append(f"Error: Invalid JSON format in file '{self.config_file_path}'.")
            return False

    def check_inputs(self) -> bool:
        """
        Check if the required keys are present in the configuration and validate their values.
        :return:bool: True if all required keys are present and their values are valid, False otherwise.
        """

        # check if there is unexpected keys in the json file
        required_keys = {'walker_type', 'num_simulations', 'num_steps', 'save_results', 'plot_statistics', 'gates',
                         'obstacles', 'biased_walker_increasing', 'biased_walker_direction', 'restart_step'}
        json_keys = set(self.config.keys())
        unexpected_keys = json_keys - required_keys
        if unexpected_keys:
            self.error_messages.append(f"you entered unexpected keys: {unexpected_keys}")
            return False

        # checking each key with some methods
        if (self.valid_walker_type() and self.valid_num_simulations() and self.valid_num_steps()
                and self.valid_save_results() and self.valid_plot_statistics() and self.valid_obstacles()
                and self.valid_gates() and self.valid_biased_walker_direction()
                and self.valid_biased_walker_increasing() and self.valid_restart_step()):
            return True
        else:
            return False

    def valid_walker_type(self) -> bool:
        """
        Validate the walker type specified in the configuration.
        :return: bool: True if the walker type is valid, False otherwise.
        """
        if "walker_type" not in self.config:
            self.error_messages.append("You must enter the type of the walker (walker_type), "
                                       "choose the number that corresponds to the description:\n"
                                       "1 - random walker\n"
                                       "2 - random walker in random length 0.5-1.5\n"
                                       "3 - regular random walker (up,down,left,right)\n"
                                       "4 - biased walker")
            return False
        if self.config["walker_type"] in [1, 2, 3, 4]:
            return True
        else:
            self.error_messages.append("You must enter the type of the walker (walker_type), "
                                       "choose the number that corresponds to the description:\n"
                                       "1 - random walker\n"
                                       "2 - random walker in random length 0.5-1.5\n"
                                       "3 - regular random walker (up,down,left,right)\n"
                                       "4 - biased walker")
            return False

    def valid_num_simulations(self) -> bool:
        """
        Validate the number of simulations specified in the configuration.
        :return: bool: True if the number of simulations is valid, False otherwise.
        """
        if "num_simulations" not in self.config:
            self.error_messages.append(
                "You must enter num_simulations, num_simulations must be a positive number smaller than 1000")
            return False
        if type(self.config["num_simulations"]) is int:
            if 1 <= self.config["num_simulations"] <= 10000:
                return True
        self.error_messages.append("num_simulations must be a positive number smaller than 1000")
        return False

    def valid_num_steps(self) -> bool:
        """
        Validate the number of steps specified in the configuration.
        :return: bool: True if the number of steps is valid, False otherwise.
        """
        if "num_steps" not in self.config:
            self.error_messages.append(
                "You must enter num_steps, num_steps must be a positive number smaller than 10000")
            return False
        if type(self.config["num_steps"]) is int:
            if 1 <= self.config["num_steps"] <= 10000:
                return True
        self.error_messages.append("num_steps must be a positive number smaller than 10000")
        return False

    def valid_save_results(self) -> bool:
        """
        Validate the 'save_results' option specified in the configuration.
        :return: bool: True if the 'save_results' option is valid, False otherwise
        """
        if "save_results" not in self.config:
            self.error_messages.append(
                "You must enter save_results, write if you want or not to save the results - Yes / No")
            return False
        if self.config["save_results"] == "Yes" or self.config["save_results"] == "No":
            return True
        else:
            self.error_messages.append("you must enter if you want to save the results - Yes / No")
            return False

    def valid_plot_statistics(self) -> bool:
        """
        Validate the 'plot_statistics' option specified in the configuration.
        :return: bool: True if the 'plot_statistics' option is valid, False otherwise.
        """
        if "plot_statistics" not in self.config:
            self.error_messages.append(
                "You must enter plot_statistics, write if you want or not to save the results - Yes / No")
            return False
        if self.config["plot_statistics"] == "Yes" or self.config["plot_statistics"] == "No":
            return True
        else:
            self.error_messages.append("you must enter if you want to plot the statistics - Yes / No")
            return False

    def valid_obstacles(self) -> bool:
        """
        Validate the obstacles specified in the configuration.
        :return: bool: True if the obstacles are valid, False otherwise.
        """
        if "obstacles" not in self.config:
            self.error_messages.append("if you don't want to enter obstacles, write in the value: "''"")
            return False
        if self.config["obstacles"] == "":
            return True
        if not isinstance(self.config["obstacles"], list):
            self.error_messages.append("Each obstacle has 2 points that will be recorded as follows in list:\n"
                                       "[x1,y1,x2,y2]\n "
                                       "more than one obstacle can be inserted. ")
            return False
        if isinstance(self.config["obstacles"], list):
            if not all(isinstance(item, list) for item in self.config["obstacles"]):
                self.error_messages.append("all the obstacles must be in list inside main list ")
                return False
        for obstacle in self.config["obstacles"]:
            if len(obstacle) != 4:
                self.error_messages.append("Each obstacle has 2 points that will be recorded as follows:\n"
                                           "[x1,y1,x2,y2]\n "
                                           "more than one obstacle can be inserted.")
                return False
            for point in obstacle:
                if not isinstance(point, int):
                    self.error_messages.append("Each point in the obstacle consists only of numbers")
                    return False
        return True

    def valid_gates(self) -> bool:
        """
        Validate the gates specified in the configuration.
        :return: bool: True if the gates are valid, False otherwise.
        """
        if "gates" not in self.config:
            self.error_messages.append("if you don't want to enter gates, write in the value: "''"")
            return False
        if self.config["gates"] == "":
            return True
        if not isinstance(self.config["gates"], list):
            self.error_messages.append(
                "Each gate contains at least 2 points and a goal point that will be recorded as follows in list:\n"
                "[x1,y1,x2,y2,[x3,y3]]\n"
                "You can enter more than one gate.")
            return False
        if isinstance(self.config["gates"], list):
            if not all(isinstance(item, list) for item in self.config["gates"]):
                self.error_messages.append("all the gates must be in list inside main list ")
                return False
        for gate in self.config["gates"]:
            if not isinstance(gate, list) or len(gate) % 2 == 0 or len(gate) < 5:
                self.error_messages.append(
                    "Each gate contains at least 2 points and a goal point that will be recorded as follows in "
                    "list:\n"
                    "[x1,y1,x2,y2,[x3,y3]]\n"
                    "You can enter more than one gate.")
                return False
            if not isinstance(gate[-1], list) or len(gate[-1]) != 2:
                self.error_messages.append("The gate must contain one point")
                return False
            for element in gate[:-1]:
                if not isinstance(element, int):
                    self.error_messages.append("Each point in the gate consists only of numbers")
                    return False
        return True

    def valid_biased_walker_direction(self) -> bool:
        """
        Validate the biased walker direction specified in the configuration.
        :return: bool: True if the biased walker direction is valid, False otherwise.
        """
        if self.config["walker_type"] == 4 and "biased_walker_direction" not in self.config:
            self.error_messages.append("You chose biased walker ,so you must choose which direction you want to "
                                       "increase his chances")
        elif "biased_walker_direction" not in self.config:
            self.error_messages.append("No biased_walker_direction, "
                                       "if you chose another walker, enter in the value: """)
            return False
        if self.config["walker_type"] != 4 and self.config["biased_walker_direction"] == "":
            return True
        if self.config["biased_walker_direction"] in ("up", "down", "left", "right", "beginning of axis"):
            return True
        else:
            self.error_messages.append("biased_walker_direction must one of these directions:\n"
                                       "up\n"
                                       "down\n"
                                       "left\n"
                                       "right\n"
                                       "beginning of axis")
            return False

    def valid_biased_walker_increasing(self) -> bool:
        """
        Validate the biased walker increasing percentage specified in the configuration.
        :return: bool: True if the biased walker increasing percentage is valid, False otherwise.
        """
        if self.config["walker_type"] == 4 and "biased_walker_increasing" not in self.config:
            self.error_messages.append(
                "You chose biased walker ,so you must choose hoe many percentages you want to increase his chances")
        elif "biased_walker_increasing" not in self.config:
            self.error_messages.append(
                "No biased_walker_increasing, if you chose another walker, enter in the value: """)
            return False
        if self.config["walker_type"] != 4 and self.config["biased_walker_increasing"] == "":
            return True
        if type(self.config["biased_walker_increasing"]) is not int:
            self.error_messages.append("biased_walker_increasing must be number between 1 and 100")
            return False
        if 0 <= self.config["biased_walker_increasing"] <= 100:
            return True
        else:
            self.error_messages.append("biased_walker_increasing must be number between 1 and 100")
            return False

    def valid_restart_step(self) -> bool:
        """
        Checks if the 'restart_step' configuration parameter is valid.
        Ensures 'restart_step' is present and either an empty string or a list of positive numbers.
        :return: bool: True if 'restart_step' is valid, False otherwise.
        """
        if "restart_step" not in self.config:
            self.error_messages.append("if you don't want to enter restart step, write in the value: '""' ")
            return False
        if self.config["restart_step"] == "":
            return True
        if not isinstance(self.config["restart_step"], list):
            self.error_messages.append("restart_step must be a list of positive numbers")
            return False
        for element in self.config["restart_step"]:
            if not isinstance(element, (int, float)) or element <= 0:
                self.error_messages.append("restart_step must be a list of positive numbers")
                return False
        return True
