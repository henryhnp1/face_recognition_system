from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import MySQLdb as db
from hashlib import md5
import pandas as pd

import os
import sys

# import util.ui_loader as ui_loader
from util import *
from models import *
# from util import ui_loader, db_connector, message_box, standardized, common
# from client.controllers.building_controller import *
# from client.util import ui_loader, db_connector, message_box, standardized, common
# import client.util.ui_loader as ui_loader
# from models import my_model
# from client.util import ui_loader

ui = ui_loader.load_ui('../resources/login.ui')

class MainApp(QMainWindow, ui):
    