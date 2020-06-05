from os.path import dirname, join
from PyQt5.uic import loadUiType


def load_ui(filename):
    current_dir = dirname(__file__)
    file_path = join(current_dir, filename)
    ui, _ = loadUiType(file_path)
    return ui
