from types import BuiltinMethodType
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from button import Button
from custom_functions import resource_path


class Page(QtWidgets.QWidget):
    def __init__(self, start_addr=0, btns=4, btn_mem=114, label_size=10):
        super(Page, self).__init__()
        uic.loadUi(resource_path('page.ui'), self)
        self.start_addr = start_addr
        # define types
        self.btn_mem = btn_mem
        self.btns_tab: QtWidgets.QTabWidget
        self.write_btn: QtWidgets.QPushButton
        self.update_btn: QtWidgets.QPushButton

        for _ in range(2):
            self.btns_tab.removeTab(0)
        self.btns = []
        for i in range(btns):
            btn = Button(
                start_addr=(i*self.btn_mem) + self.start_addr,
                label_size=label_size
            )
            self.btns_tab.addTab(btn, f'Button {i+1}')
            self.btns.append(btn)

    def get_value(self, addr, obj) -> dict:
        data = {
            'name': obj.objectName(),
            'addr': addr,
            'value': None
        }
        try:
            if isinstance(obj, QtWidgets.QComboBox):
                data['value'] = obj.currentIndex()
            elif isinstance(obj, QtWidgets.QSpinBox):
                data['value'] = obj.value()
            elif isinstance(obj, QtWidgets.QLineEdit):
                data['value'] = obj.text()
        except Exception as e:
            print(e)
        return data

    def set_value(self,  obj, value):
        try:
            if isinstance(obj, QtWidgets.QComboBox):
                obj.setCurrentIndex(value)
            elif isinstance(obj, QtWidgets.QSpinBox):
                obj.setValue(value)
            elif isinstance(obj, QtWidgets.QLineEdit):
                if value == ' ' * self.label_size:
                    obj.setText("*" * self.label_size)
                else:
                    obj.setText(value)
        except Exception as e:
            print(e)

    def set_data(self, data):
        for d in data:
            obj = eval(f'self.{d["name"]}')
            self.set_value(obj, d['value'])

    def read_data(self):
        addr = self.start_addr + (len(self.btns) * self.btn_mem) 

        data = []
        
        data.append(self.get_value(addr + 0, self.onoffVslider))
        data.append(self.get_value(addr + 1, self.spinBox_VSLID_EXPPED_3))
        data.append(self.get_value(addr + 2, self.spinBox_VSLIDSWITCH_3))
        data.append(self.get_value(addr + 3, self.spinBox_VSLIDAUTOON_3))
        data.append(self.get_value(addr + 4, self.spinBox_VSLIDAUTOFF_3))
        data.append(self.get_value(addr + 5, self.spinBox_VSLIDMIDCH_3))

        data.append(self.get_value(addr + 6, self.onoffSlider))
        data.append(self.get_value(addr + 7, self.spinBox_EXPPED))
        data.append(self.get_value(addr + 8, self.spinBox_EXPEDSWITCH))
        data.append(self.get_value(addr + 9, self.spinBox_EXPEDAUTOON))
        data.append(self.get_value(addr + 10, self.spinBox_EXPEDAUTOFF))
        data.append(self.get_value(addr + 11, self.spinBox_EXPEDMIDCH))


        return data

    def read_data_all(self):
        data = []
        for btn in self.btns:
            btn: Button
            data.append(btn.read_data())
        data.append(self.read_data())
        return data

    def set_data_all(self, data):
        for index, d in enumerate(data[:-1]):
            self.btns[index].set_data(d)

        self.set_data(data[-1])
