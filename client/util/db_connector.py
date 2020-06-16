import MySQLdb as mdb
from PyQt5.QtWidgets import QMessageBox


def connector(host, username, password, db_name):
    db = None
    try:
        db = mdb.connect(host, username, password, db_name)
    except mdb.Error:
        pass
    return db

# def check_login(username, password):
#     con = connector('localhost', 'henrydb', 'root', 'face_recognitions')
#     if con == None:
#         return QMessageBox(QMessageBox.Icon, "Wrong db or authentication")
#     cusor = con.cursor()
#     cusor.execute("select * from user where username='{}' and password='{}'".format(username, password.hexdigest()))
#     print(cusor._last_executed)
#     session = None
#     for i in range(cusor.rowcount):
#         result = cusor.fetchall()
#         if len(result) == 1:
#             session = username
#         else:
#             break
#     return session