from gui import GUI

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
