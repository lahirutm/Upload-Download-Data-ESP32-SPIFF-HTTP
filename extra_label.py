from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from custom_functions import resource_path


class ExtraLabel(QtWidgets.QWidget):
    def __init__(self, start_addr=0, label_size=10):
        super(ExtraLabel, self).__init__()
        uic.loadUi(resource_path('extra_label.ui'), self)

        self.start_addr = start_addr
        self.label_size = label_size

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

    def set_data_all(self, data):
        for d in data:
            obj = eval(f'self.{d["name"]}')
            self.set_value(obj, d['value'])

    def read_data_all(self):
        data = []

        addr = self.start_addr

        data.append(self.get_value(addr, self.label_1))
        addr += self.label_size

        data.append(self.get_value(addr, self.label_2))
        addr += self.label_size 

        data.append(self.get_value(addr, self.label_3))
        addr += self.label_size 

        data.append(self.get_value(addr, self.label_4))
        addr += self.label_size 

        return data
