import random
import math


class Walker:
    """
    The Walker class represents an entity capable of taking steps in a two-dimensional space.
    It encapsulates methods to perform different types of movements,
    such as random steps and biased steps,
    as well as functionality to keep track of its position in the space.
    """

    def __init__(self) -> None:
        """
        this method initializes an instance of the Walker class with the position set to (0, 0).
        :return: None
        """
        self.__position = (0, 0)

    def random_step(self) -> tuple[float, float]:
        """
        calculates a random direction in degrees, converts it to radians, computes the corresponding x and y
        components of the step using trigonometric functions,
        and updates the position of the walker accordingly.
        :return: tuple[float, float]: The new position after the biased movement.
        """
        direction_degrees = random.randint(0, 360)
        direction_radians = math.radians(direction_degrees)
        x = math.cos(direction_radians)
        y = math.sin(direction_radians)
        return self.__position[0] + x, self.__position[1] + y

    def random_step_length(self) -> tuple[float, float]:
        """
         generates a random direction in degrees, converts it to radians,
         generates a random step length between 0.5 and 1.5 units,
         calculates the x and y components of the step using trigonometric functions,
         and updates the position of the walker accordingly.
         :return: tuple[float, float]: The new position after the biased movement.
        """
        direction_degrees = random.uniform(0, 360)
        direction_radians = math.radians(direction_degrees)
        length = random.uniform(0.5, 1.5)
        x = length * math.cos(direction_radians)
        y = length * math.sin(direction_radians)
        return self.__position[0] + x, self.__position[1] + y

    def four_options_step(self) -> tuple[float, float]:
        """
        randomly selects one of four possible directions: up, down, left, or right,
        and updates the position of the walker accordingly.
        :return: tuple[float, float]: The new position after the biased movement.

        """
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        return self.__position[0] + direction[0], self.__position[1] + direction[1]

    def biased_step(self, increased_direction: str, increase_percentage: int) -> tuple[float, float]:
        """
        biases the movement probability towards a specified direction by a given percentage,
        then updates the walker's position accordingly.
        :param increased_direction: the movement that his probability is biased towards
        :param increase_percentage: the percentage of biasing the movement
        :return: tuple[float, float]: The new position after the biased movement.
        """
        if increased_direction == "up":
            index = 0
        elif increased_direction == "down":
            index = 1
        elif increased_direction == "left":
            index = 2
        elif increased_direction == "right":
            index = 3
        else:
            index = 4
        probabilities = [1, 1, 1, 1, 1]

        probabilities[index] += (increase_percentage / 100)
        total_prob = sum(probabilities)
        probabilities = [prob / total_prob for prob in probabilities]
        all_directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        direction = random.choices(all_directions, probabilities)
        if direction == (0, 0):
            return self.step_towards_beginning()
        else:
            x, y = direction[0]
            return self.__position[0] + x, self.__position[1] + y

    def step_towards_beginning(self) -> tuple[int, int]:
        """
        calculates a step towards the beginning of the axes
        by decrementing or incrementing the x and y coordinates of the walker's position based on their signs,
        :return: the updated position as a tuple of integers
        """
        x, y = self.__position
        if x > 0:
            x -= 1
        elif x < 0:
            x += 1
        if y > 0:
            y -= 1
        elif y < 0:
            y += 1
        return x, y

    def get_position(self) -> tuple[int, int]:
        """
        :return: the current position of the walker as a tuple of integers representing the x and y coordinates.
        """
        return self.__position

    def set_position(self, position: tuple[int, int]) -> None:
        """
        Set the position of the object.
        :param position: tuple([int, int]): A tuple representing the new position as (x, y) coordinates.
        :return: None
        """
        self.__position = position
