import MySQLdb as mdb
from PyQt5.QtWidgets import QMessageBox


def connector(host, username, password, db_name):
    db = None
    try:
        db = mdb.connect(host, username, password, db_name)
    except mdb.Error:
        pass
    return db

