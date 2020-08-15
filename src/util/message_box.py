from PyQt5.QtWidgets import QMessageBox


class MyMessageBox(QMessageBox):
    def __init__(self, icon:QMessageBox.Icon, title, text):
        super().__init__()
        self.setIcon(icon)
        self.setWindowTitle(title)
        self.setText(text)
