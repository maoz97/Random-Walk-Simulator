from random_walk_gui import RandomWalkSimulatorGUI
import tkinter as tk
import sys


def main() -> None:
    """
    A command-line interface for running the Random Walk Simulator or launching its graphical user interface.
    :return: None
    """

    if "--help" in sys.argv or "-h" in sys.argv:
        print("Welcome to the Random Walker Simulator!\n\n"
              "To start the simulation, run the command: python main.py\n"
              "You can press the help button to see how to implement the json file.\n"
              "If you want to exit, press the exit button.\n\n"
              "After you create the config file, save its path in order to start the simulation.\n")
        return


    root = tk.Tk()
    app = RandomWalkSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
