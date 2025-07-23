# Random Walker Simulator

This project is a configurable simulator for 2D random walks, enhanced with visualizations and GUI interaction. It supports various walker types, obstacles, gates, restarts, and detailed statistical analysis.

##  Features

- Multiple walker types (uniform, random-length, biased, grid-based).
- Support for custom obstacles and gates via configuration.
- Restart points that probabilistically return the walker to the origin.
- Detailed statistics: distances from origin/axes, steps to exit radius, and more.
- Graphical plots and a visual "crystal graph" of walker movements.
- User-friendly Tkinter-based GUI with integrated helper and JSON validator.

##  GUI Overview

- Enter a path to a JSON config file.
- Click `Run Simulation` to execute and visualize.
- Use the `Help` button for parameter descriptions.
- Crystal graph will be shown at the end.

##  Output

results.txt: raw simulation statistics.

graph_*.png: charts of walk metrics.

crystal_graph.png: 2D path of the walker.

##  Dependencies

Python 3.x

tkinter

matplotlib

numpy

##  Configuration File (JSON)

Here’s an example structure for `config.json`:

```json
{
    "walker_type": 3,
    "num_simulations": 2,
    "num_steps": 200,
    "save_results": "Yes",
    "plot_statistics": "Yes",
    "obstacles": [[400, 2, 3, 500]],
    "gates": [
        [12, 14, 10, 10, [100, 100]],
        [23, 23, 45, 23, [200, 200]]
    ],
    "biased_walker_increasing": "",
    "biased_walker_direction": "",
    "restart_step": ""
}
Refer to the in-app Help button for full descriptions of each field.


