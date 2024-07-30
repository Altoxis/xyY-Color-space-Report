import config

def reload_config_data(xy_plotter, color_variations_plotter):
    # Read values from config.py
    try:
        x_center, y_center, Y = config.xyY_values
    except ValueError:
        xy_plotter.label.setText("Invalid values in config.py. Please provide three valid numbers.")
        color_variations_plotter.label.setText("Invalid values in config.py. Please provide three valid numbers.")
        return

    if not (0 <= x_center <= 1) or not (0 <= y_center <= 1) or not (0 <= Y <= 1):
        xy_plotter.label.setText("Values in config.py must be between 0 and 1.")
        color_variations_plotter.label.setText("Values in config.py must be between 0 and 1.")
        return

    # Update the plotters with new values
    xy_plotter.start_calculation()
    color_variations_plotter.start_calculation()
