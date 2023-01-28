import os
import sys
import requests

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox


# Local functions and classes
from page import Page
from extra_label import ExtraLabel
from custom_functions import (
    dump_json,
    load_json,
    resource_path
)

##############################
##############################
# for the debug go to parallel_threads.py and set debug=True to shod the address numeber then go to get data.py and set DEBUG = True


NUMBER_OF_PAGES = 4
NUMBER_OF_BUTTONS = 4
BTN_LABEL_SIZE = 10
URL = 'http://192.168.4.1/data'

# Number of memory addresses for each page
BTN_MEMORY = 114
PAGE_FOOTER_MEM = 12
PAGE_MEMORY = (BTN_MEMORY * NUMBER_OF_BUTTONS) + PAGE_FOOTER_MEM


class LoadingGif(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.movie = QtGui.QMovie(resource_path("loading.gif"))
        self.setMovie(self.movie)
        self.movie.start()
        self.hide()

    def hide(self) -> None:
        self.movie.stop()
        return super().hide()

    def show(self) -> None:
        self.movie.start()
        return super().show()


class MainWidget(QtWidgets.QWidget):

    def __init__(self, host: QtWidgets.QMainWindow, parent=None):
        super().__init__(parent)
        self.host = host

        self.frame = QtWidgets.QFrame()
        layout = QtWidgets.QVBoxLayout()

        self.tabs = QtWidgets.QTabWidget(
            tabPosition=QtWidgets.QTabWidget.North)
        self.add_pages()
        layout.addWidget(self.tabs)

        btns_layout = QtWidgets.QHBoxLayout()
        self.write_btn = QtWidgets.QPushButton('Write All', self)
        self.write_btn.clicked.connect(self.write_all)

        self.read_btn = QtWidgets.QPushButton('Update All', self)
        self.read_btn.clicked.connect(self.read_all)

        btns_layout.addWidget(self.write_btn)
        btns_layout.addWidget(self.read_btn)

        self.save_btn = QtWidgets.QPushButton('Save all preset to file', self)
        self.save_btn.clicked.connect(self.save_click)

        self.load_btn = QtWidgets.QPushButton('Load presets from file', self)
        self.load_btn.clicked.connect(self.load_click)

        btns_layout.addWidget(self.load_btn)
        btns_layout.addWidget(self.save_btn)

        layout.addLayout(btns_layout)

        self.frame.setLayout(layout)

        parent_layout = QtWidgets.QVBoxLayout()
        parent_layout.addWidget(self.frame)

        self.loading_frame = LoadingGif()
        self.loading_frame.hide()

        parent_layout.addWidget(self.loading_frame)

        self.setLayout(parent_layout)

    def delete_obj(self, obj):
        try:
            del obj
        except Exception as e:
            print(e)

    def refresh_tabs(self):
        for _ in range(len(self.pages)):
            self.tabs.removeTab(0)
        del self.pages
        self.add_pages()

    def add_pages(self):
        """ Function to add Pages and create there tabs """
        self.pages = []
        for i in range(NUMBER_OF_PAGES):
            self.pages.append(
                Page(
                    start_addr=(i*PAGE_MEMORY),
                    btns=NUMBER_OF_BUTTONS,
                    btn_mem=BTN_MEMORY,
                    label_size=BTN_LABEL_SIZE
                )
            )
            self.tabs.addTab(self.pages[i], f'Page {i+1}')
        self.pages.append(ExtraLabel(
            start_addr=(NUMBER_OF_PAGES*PAGE_MEMORY)+1,
            label_size=BTN_LABEL_SIZE
        ))
        self.tabs.addTab(self.pages[NUMBER_OF_PAGES], f'Extra Labels')

    def read_data(self):
        data = []
        for page in self.pages:
            page: Page
            data.append(page.read_data_all())
        return data

    def set_data(self, data):
        for index, d in enumerate(data):
            self.pages[index].set_data_all(d)

    def write_all(self):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Are you sure, You want to upload configurations now ?")
        msg.setWindowTitle("Upload")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No );
        result = msg.exec_()

        if (result == QMessageBox.Yes):
            try:
                response = requests.post(URL, json = self.read_data())

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"Configurations successfully uploaded.")
                msg.setWindowTitle("Upload Success")
                msg.setStandardButtons(QMessageBox.Ok);
                msg.exec_()

            except Exception as err:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"{err=}")
                msg.setWindowTitle("Upload Failed")
                msg.setStandardButtons(QMessageBox.Ok);
                msg.exec_()

                #print(f"Unexpected error while posting data to {URL=}:: {err=}, {type(err)=}")
        else:
            print(f"No button clicked !");

        self.write_btn.clearFocus()

    def read_all(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Are you sure, You want to download data ?")
        msg.setWindowTitle("Download")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No );
        result = msg.exec_()

        if (result == QMessageBox.Yes):
            try:
                response = requests.get(URL)
                self.set_data(response.json())

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"Configurations successfully downloaded.")
                msg.setWindowTitle("Download Success")
                msg.setStandardButtons(QMessageBox.Ok);
                msg.exec_()

            except Exception as err:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(f"{err=}")
                    msg.setWindowTitle("Download Failed")
                    msg.setStandardButtons(QMessageBox.Ok);
                    msg.exec_()

                    #print(f"Unexpected error while posting data to {URL=}:: {err=}, {type(err)=}")
        else:
            print(f"No button clicked !");

        self.write_btn.clearFocus()


    def saveFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Configurations", "config.json",
                                                             "JSON Files (*.json)", options=options)
        if file_name:
            return file_name

    def loadFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Configurations", "config.json",
                                                             "JSON Files (*.json)", options=options)
        if file_name:
            return file_name

    def save_click(self):
        filename = self.saveFileDialog()
        if filename:
            data = self.read_data()
            dump_json(filename, data)

    def load_click(self):
        filename = self.loadFileDialog()
        if filename:
            data = load_json(filename)
            self.set_data(data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    window = QtWidgets.QMainWindow()

    # window.setWindowState(QtCore.Qt.WindowMaximized)
    window.setMinimumSize(1150, 640)
    qtRectangle = window.frameGeometry()
    centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())
    window.setWindowIcon(QtGui.QIcon(resource_path('logo.jpg')))
    widget = MainWidget(host=window)
    window.setWindowTitle("THE BUTTON EDITOR")
    window.setCentralWidget(widget)
    window.show()
    ret = app.exec_()
    widget.disconnect()
    sys.exit(ret)
