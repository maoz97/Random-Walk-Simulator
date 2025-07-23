import tkinter as tk
from tkinter import messagebox
from random_walk_inputs import Inputs
from simulator import Simulator
import os


class RandomWalkSimulatorGUI:
    """
       Graphical user interface for the Random Walk Simulator.
    """
    welcome_message = (
        "Welcome to the Random Walker Simulator!\n\n"
        "To start the simulation, please enter the path to the configuration file.\n"
        "If you need help, press help'.\n"
        "If you want to exit, press 'exit'.\n\n"
        "Ensure your configuration file is correctly formatted with the required parameters (for explain press help.\n"
    )

    def __init__(self, master) -> None:
        """
       Initialize the GUI.
       :param master: The Tkinter root window.
       """
        self.help_text = None
        self.exit_button = None
        self.help_button = None
        self.run_button = None
        self.config_file_entry = None
        self.config_file_label = None
        self.welcome_label = None
        self.master = master
        self.master.title("Random Walk Simulator")

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create all the widgets for the GUI.
        """

        # Welcome message
        self.welcome_label = tk.Label(self.master, text=self.welcome_message, justify="left", wraplength=400)
        self.welcome_label.pack(pady=20)

        self.config_file_label = tk.Label(self.master, text="Enter the path to the configuration file:")
        self.config_file_label.pack()

        self.config_file_entry = tk.Entry(self.master, width=30)
        self.config_file_entry.pack()

        self.run_button = tk.Button(self.master, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack()

        # Buttons for additional functionalities
        self.help_button = tk.Button(self.master, text="Help", command=self.show_help)
        self.help_button.pack()

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit)
        self.exit_button.pack()

    def show_help(self) -> None:
        """
        Display the help window with instructions.
        """
        help_window = tk.Toplevel(self.master)
        help_window.title("Help")

        self.help_text = tk.Text(help_window)
        self.help_text.insert(tk.END, get_helper(0))
        self.help_text.pack()

        # Create buttons in a row
        button_frame = tk.Frame(help_window)
        button_frame.pack()

        for i in range(1, 11):
            button = tk.Button(button_frame, text=str(i), command=lambda num=i: self.show_helper_text(num))
            button.pack(side="left")

        back_button = tk.Button(help_window, text="Back", command=help_window.destroy)
        back_button.pack()

    def show_helper_text(self, num: int) -> None:
        """
        Display the help text corresponding to the selected parameter number.
        :param num: The parameter number.
        """
        self.help_text.delete("1.0", tk.END)
        self.help_text.insert(tk.END, get_helper(num))

    def run_simulation(self) -> None:
        """
        Run the simulation based on the provided configuration file.
        """
        config_file_path = self.config_file_entry.get()

        if config_file_path.strip() == "":
            messagebox.showerror("Error", "Please enter the path to the configuration file.")
            return

        # Parse configuration file
        inputs = Inputs(config_file_path)
        if not inputs.parse_config_file():
            # Get error messages from Inputs class
            error_messages = inputs.get_error_messages()
            messagebox.showerror("Error", "\n".join(error_messages))
            return

        # Check inputs
        if not inputs.check_inputs():
            # Get error messages from Inputs class
            error_messages = inputs.get_error_messages()
            messagebox.showerror("Error", "\n".join(error_messages))
            return

        simulator = Simulator(inputs.config["walker_type"], inputs.config["num_simulations"],
                              inputs.config["num_steps"], inputs.config["obstacles"], inputs.config["gates"],
                              inputs.config["biased_walker_direction"], inputs.config["biased_walker_increasing"],
                              inputs.config["restart_step"])
        simulator.run()

        if inputs.config["save_results"] == "Yes":
            simulator.save_results()

        if inputs.config["plot_statistics"] == "Yes":
            simulator.plot_all_results()

        directory_path = os.getcwd()
        simulator.plot_crystal_graph(directory_path)  # Plot the crystal graph

        messagebox.showinfo("Success", "Simulation finished!")

        self.show_crystal_graph_window(directory_path)

    def show_crystal_graph_window(self, directory_path: str) -> None:
        """
        Display the crystal graph window with the saved image.
        :param directory_path: The directory path where the crystal graph image is saved.
        """
        # Create a new window to display the crystal graph
        graph_window = tk.Toplevel(self.master)
        graph_window.title("Crystal Graph")

        # Load the saved image and display it in the window
        img = tk.PhotoImage(file=directory_path + "/crystal_graph.png")
        label = tk.Label(graph_window, image=img)
        label.image = img  # Keep a reference to the image to prevent garbage collection
        label.pack()


def get_helper(num: int):
    """
    Get the helper text corresponding to the provided parameter number.
    :param num: The parameter number.
    :return: The helper text.
    """
    helpers = {
        0: ("Hello! welcome to the helper!\n\n"
            "you need to create Json file with the following parameters:\n\n"
            "1. walker_type\n2. num_simulations\n3. num_steps\n4. save_results\n5. plot_statistics\n6. obstacles\n"
            "7. gates\n8. biased_walker_increasing 9.\nbiased_walker_direction\n10. restart_step\n\n"
            "you can look in the example JSON file or choose the number of parameter below for more details: "),
        1: ("walker_type:\n\n"
            "write in file the number of the walker you want to simulate:\n"
            "1 - random walker\n"
            "2 - random walker in random length 0.5-1.5\n"
            "3 - regular random walker (up,down,left,right)\n"
            "4 - biased walker\n"),
        2: "num_simulations:\n\n"
           "num_simulations must be a positive number smaller than 1000\n",
        3: "num_steps:\n\n"
           "num_steps must be a positive number smaller than 10000\n",
        4: "save_results:\n\n"
           "If you want or to save results write: Yes. if not, write: No\n",
        5: "plot_statistics:\n\n"
           "If you want or to plot statistics write: Yes. if not, write: No\n",
        6: ("obstacle:\n\n"
            "Each obstacle has 2 points that will be recorded as follows in list:\n"
            "[x1,y1,x2,y2]\n "
            "Each coordinate in point must be a number. more than one obstacle can be inserted.\n"),
        7: ("gate:\n\n"
            "Each gate contains at least 2 points and a goal point that will be recorded as follows in list:\n"
            "[x1,y1,x2,y2,[x3,y3]]\n"
            "Each coordinate in point must be a number.\n You can enter more than one gate.\n"),
        8: "biased_walker_increasing:\n\n"
           "biased_walker_increasing must be number between 1 and 100.\n",
        9: ("biased_walker_direction:\n\n"
            "For biased_walker_direction write one of these directions:\n"
            "up\n"
            "down\n"
            "left\n"
            "right\n"
            "beginning of axis\n"),
        10: "restart_step:\n\n"
            "restart_step must be a list of positive numbers\n"
    }
    return helpers.get(num, "Invalid input")


