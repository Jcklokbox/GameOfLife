# HashLife in Python

This repository contains an implementation of the HashLife algorithm in Python,
which is a highly efficient algorithm for simulating the Game of Life, a
cellular automaton devised by John Conway.

## Description

The Game of Life is a zero-player game that simulates the evolution of cells on
a two-dimensional grid based on a set of rules. The HashLife algorithm
optimizes the simulation process by identifying and storing patterns that
repeat themselves, resulting in a significant performance improvement compared
to the naive implementation.

## Installation

Follow these steps to set up and run the HashLife simulation:

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/hashlife-python.git
   cd hashlife-python
   ```

2. **Create and activate a virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the main script**

   ```bash
   python main.py
   ```

## Configuration

You can modify the width and height of the game window, as well as enable GUI
mode or specify the number of iterations for the non-GUI mode in the `main.py`
file. Here's an example:

```python
if __name__ == '__main__':
    # Example usage
    width = 2 ** 8
    height = 2 ** 8

    # GUI mode
    # game_gui = GUI(width, height, cell_size=3)
    # game_gui.run()

    # Non-GUI mode
    game_no_gui = GUI(width, height, gui=False)
    # Specify the number of iterations for non-GUI mode
    game_no_gui.run(num_iterations=1000)
```

## Dependencies

The following dependencies are required to run the HashLife simulation:

- pygame ~= 2.5.2
- numpy ~= 1.26.4
- scipy ~= 1.13.0
- numba ~= 0.59.1

These dependencies are listed in the requirements.txt file and can be installed
using the command mentioned in the Installation section.

Feel free to explore and modify the code to suit your needs. Contributions and
improvements are always welcome!