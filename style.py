import os

# Define styles, colors, and image paths

# Colors
DARK_GREY = '#1F1F1F'  # Dark grey color for backgrounds
LIGHTER_GREY = '#363636'  # Lighter grey color for buttons
LIGHTER_DARK_GREY = '#2B2B2B'  # Slightly lighter dark grey for drop areas
WHITE = '#FFFFFF'  # White color for text fields and button text
FONT_COLOR = '#A8A8A8'  # Font color
ICON_COLOR = 'lightgrey'  # Initial color for icon
ICON_HOVER_COLOR = 'white'  # Hover color for icon
ICON_PRESSED_COLOR = 'grey'  # Pressed color for icon
LIGHT_BORDER_COLOR = '#CCCCCC'  # Light border color for editable textboxes
LIGHT_RED = "#ff0000"
LIGHTER_RED = "rgba(255, 204, 204, 0.2)"  # Semi-transparent red for hover

# Font settings
BASE_FONT = "Arial"
BASE_FONT_SIZE = "14px"
BASE_FONT_COLOR = FONT_COLOR

# Styles
MAIN_WINDOW_STYLE = """
    QFrame#MainBackground {
        background-color: %s;
        border-radius: 5px;
    }
""" % DARK_GREY

DRAGGABLE_WIDGET_STYLE = """
    QWidget {
        background-color: %s;
        border-radius: 10px;
        border: 1px solid #CCCCCC;
        margin-bottom: 1px;
    }
""" % LIGHTER_DARK_GREY

MAIN_BACKGROUND_STYLE = """
    QFrame#MainBackground {
        background-color: %s;
        border-radius: 5px;
    }
""" % DARK_GREY

CONTENT_BOX_STYLE = """
    background-color: %s;
    border-radius: 10px;
    padding: 5px;
""" % LIGHTER_DARK_GREY

ICON_STYLE = """
    QPushButton {
        background-color: transparent;
        border: none;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 50);
    }
    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 100);
    }
"""

BUTTON_STYLE = """
    QPushButton {
        background-color: %s;
        color: %s;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-family: %s;
        font-size: %s;
    }
    QPushButton:hover {
        background-color: #444444;
    }
""" % (LIGHTER_GREY, WHITE, BASE_FONT, BASE_FONT_SIZE)

LINE_EDIT_STYLE = """
    QLineEdit {
        background-color: %s;
        border: none;
        border-radius: 5px;
        padding: 5px;
        color: %s;
        font-family: %s;
        font-size: %s;
    }
""" % (LIGHTER_GREY, FONT_COLOR, BASE_FONT, BASE_FONT_SIZE)

LINE_EDIT_STYLE_EDITABLE = """
    QLineEdit {
        background-color: %s;
        border: 1px solid %s;
        border-radius: 5px;
        padding: 5px;
        color: %s;
        font-family: %s;
        font-size: %s;
    }
""" % (LIGHTER_GREY, LIGHT_BORDER_COLOR, FONT_COLOR, BASE_FONT, BASE_FONT_SIZE)

# style.py
SEARCH_BAR_STYLE = """
QLineEdit {
    height: 30px;
    border: 1px solid #2E2E2E;
    border-radius: 5px;
    padding: 5px;
    background-color: #2E2E2E;
    color: #FFFFFF;
}
"""
LABEL_STYLE = """
    QLabel {
        color: lightgrey;
        font-family: Calibri;
        font-size: 10pt;
        padding: 5px;
    }
"""

SCROLL_AREA_STYLE = """
QScrollArea {
    border: none;
}

QScrollBar:vertical {
    border: none;
    background: LIGHTER_GREY;
    width: 10px;
    margin: 0px 0px 0px 0px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: LIGHTER_GREY;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:vertical {
    border: none;
    background: #2B2B2B;
    height: 10px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    border: none;
    background: #2B2B2B;
    height: 10px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""
DELETE_DROP_AREA_STYLE = """
    QWidget {
        background-color: %s;

        border-radius: 10px;
        padding: 5px;
    }
""" % LIGHT_RED

DELETE_DROP_AREA_HOVER_STYLE = """
    QWidget {
        background-color: %s;

        border-radius: 10px;
        padding: 5px;
    }
""" % LIGHTER_RED
# Paths to images
MINIMIZE_ICON_PATH = os.path.join(os.path.dirname(__file__), 'resources/icons/minimize.svg')
MAXIMIZE_ICON_PATH = os.path.join(os.path.dirname(__file__), 'resources/icons/maximize.svg')
CLOSE_ICON_PATH = os.path.join(os.path.dirname(__file__), 'resources/icons/close.svg')
