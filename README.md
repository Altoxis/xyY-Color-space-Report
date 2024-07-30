![2](https://github.com/user-attachments/assets/3385d2d5-d87f-4076-a0a2-2746d9db8792)
![1](https://github.com/user-attachments/assets/f0478327-47dc-4eab-9626-49a2f310a23d)
Color Report Application
Overview
The Color Report Application is a Python-based tool designed to manage and analyze color data. It provides functionalities to add, plot, and evaluate colors using various color spaces and allows for interactive manipulation of color samples. The application integrates with a spectrometer for real-time color measurements and supports database operations for color data management.

Features
Color Plotting: Visualize color data in the xyY color space and generate plots for color variations and spectrometer data.
Database Management: Add, update, and delete color data entries in an SQLite database.
Real-time Color Measurement: Interface with the YS3010 spectrophotometer from 3nh to capture and plot real-time color data.
Drag and Drop Functionality: Interactive UI components allowing users to drag and drop color samples for plotting and database operations.
Color Comparison: Calculate and display color differences (delta) and pass/fail judgments based on specified criteria.
User Interface: PyQt5-based GUI with various interactive widgets and plotting areas.
Installation
Prerequisites
Python 3.x
PyQt5
pyqtgraph
numpy
pandas
colour
SQLite3
