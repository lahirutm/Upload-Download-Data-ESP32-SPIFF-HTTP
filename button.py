from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from custom_functions import resource_path


class Button(QtWidgets.QWidget):
    def __init__(self, start_addr=0, label_size=10):
        super(Button, self).__init__()
        uic.loadUi(resource_path('button.ui'), self)

        self.start_addr = start_addr
        self.label_size = label_size

        self.tempo_state = False
        self.tempo_btn: QtWidgets.QPushButton

        # setting checkable to true
        self.tempo_btn.setCheckable(True)

        # setting calling method by button
        self.tempo_btn.clicked.connect(self.tempo_toggle)

        self.check_func()
        self.check_action()
        for i in range(1, 7):
            obj = eval(f'self.btn_func_{i}')
            obj: QtWidgets.QComboBox
            obj.currentIndexChanged.connect(self.check_func)

    def tempo_label(self):
        if self.tempo_state:
            self.disable_actions()
            self.tempo_btn.setText("Enabled")
        else:
            self.enable_actions()
            self.tempo_btn.setText("Disabled")

    def tempo_toggle(self):
        self.tempo_state = (not self.tempo_state)
        self.tempo_label()

    def check_action(self):
        self.tempo_state = False
        for i in range(1, 7):
            obj = eval(f'self.btn_action_{i}')
            obj: QtWidgets.QComboBox
            index = obj.currentIndex()
            if index > 5:
                self.tempo_state = True
                break
        self.tempo_label()

    def set_tempo(self, obj: QtWidgets.QComboBox):
        model = obj.model()
        if obj.currentIndex() < 6:
            obj.setCurrentIndex(6)
        for i in range(7):
            model.item(i).setEnabled(False)
        for i in range(6, 8):
            model.item(i).setEnabled(True)

    def unset_tempo(self, obj: QtWidgets.QComboBox):
        model = obj.model()
        if obj.currentIndex() > 5:
            obj.setCurrentIndex(0)
        for i in range(6):
            model.item(i).setEnabled(True)
        for i in range(6, 8):
            model.item(i).setEnabled(False)

    def disable_actions(self,):
        for i in range(1, 7):
            obj = eval(f'self.btn_action_{i}')
            self.set_tempo(obj)

    def enable_actions(self):
        for i in range(1, 7):
            obj = eval(f'self.btn_action_{i}')
            self.unset_tempo(obj)

    def change_active(self, name, index):
        if index == 0:
            self.program_view(name)
        elif index == 1:
            self.non_latch_view(name)
        elif index == 2:
            self.toggle_view(name)
        elif index == 3:
            self.latch_view(name)
        elif index == 4:
            self.scene_view(name)
        elif index == 5:
            self.plus_view(name)
        elif index == 6:
            self.min_view(name)
        elif index == 7:
            self.nothing_view(name)

    def check_func(self):
        for i in range(1, 7):
            obj = eval(f'self.btn_func_{i}')
            obj: QtWidgets.QComboBox
            index = obj.currentIndex()
            self.change_active(str(i), index)

    def program_view(self, name):
        eval(f'self.pc_num_{name}').setEnabled(True)
        eval(f'self.cc_num_{name}').setEnabled(False)
        eval(f'self.cc_value_{name}').setEnabled(False)
        eval(f'self.midi_ch_{name}').setEnabled(True)
        eval(f'self.scene_{name}').setEnabled(False)
        eval(f'self.pre_min_{name}').setEnabled(False)
        eval(f'self.pre_max_{name}').setEnabled(False)

    def non_latch_view(self, name):
        eval(f'self.pc_num_{name}').setEnabled(False)
        eval(f'self.cc_num_{name}').setEnabled(True)
        eval(f'self.cc_value_{name}').setEnabled(True)
        eval(f'self.midi_ch_{name}').setEnabled(True)
        eval(f'self.scene_{name}').setEnabled(False)
        eval(f'self.pre_min_{name}').setEnabled(False)
        eval(f'self.pre_max_{name}').setEnabled(False)

    def latch_view(self, name):
        eval(f'self.pc_num_{name}').setEnabled(False)
        eval(f'self.cc_num_{name}').setEnabled(True)
        eval(f'self.cc_value_{name}').setEnabled(True)
        eval(f'self.midi_ch_{name}').setEnabled(True)
        eval(f'self.scene_{name}').setEnabled(False)
        eval(f'self.pre_min_{name}').setEnabled(False)
        eval(f'self.pre_max_{name}').setEnabled(False)

    def toggle_view(self, name):
        eval(f'self.pc_num_{name}').setEnabled(False)
        eval(f'self.cc_num_{name}').setEnabled(True)
        eval(f'self.cc_value_{name}').setEnabled(False)
        eval(f'self.midi_ch_{name}').setEnabled(True)
        eval(f'self.scene_{name}').setEnabled(False)
        eval(f'self.pre_min_{name}').setEnabled(False)
        eval(f'self.pre_max_{name}').setEnabled(False)

    def scene_view(self, name):
        eval(f'self.pc_num_{name}').setEnabled(False)
        eval(f'self.cc_num_{name}').setEnabled(False)
        eval(f'self.cc_value_{name}').setEnabled(False)
        eval(f'self.midi_ch_{name}').setEnabled(True)
        eval(f'self.scene_{name}').setEnabled(True)
        eval(f'self.pre_min_{name}').setEnabled(False)
        eval(f'self.pre_max_{name}').setEnabled(False)

    def plus_view(self, name):
        eval(f'self.pc_num_{name}').setEnabled(False)
        eval(f'self.cc_num_{name}').setEnabled(False)
        eval(f'self.cc_value_{name}').setEnabled(False)
        eval(f'self.midi_ch_{name}').setEnabled(True)
        eval(f'self.scene_{name}').setEnabled(False)
        eval(f'self.pre_min_{name}').setEnabled(True)
        eval(f'self.pre_max_{name}').setEnabled(True)

    def min_view(self, name):
        eval(f'self.pc_num_{name}').setEnabled(False)
        eval(f'self.cc_num_{name}').setEnabled(False)
        eval(f'self.cc_value_{name}').setEnabled(False)
        eval(f'self.midi_ch_{name}').setEnabled(True)
        eval(f'self.scene_{name}').setEnabled(False)
        eval(f'self.pre_min_{name}').setEnabled(True)
        eval(f'self.pre_max_{name}').setEnabled(True)

    def nothing_view(self, name):
        eval(f'self.pc_num_{name}').setEnabled(False)
        eval(f'self.cc_num_{name}').setEnabled(False)
        eval(f'self.cc_value_{name}').setEnabled(False)
        eval(f'self.midi_ch_{name}').setEnabled(False)
        eval(f'self.scene_{name}').setEnabled(False)
        eval(f'self.pre_min_{name}').setEnabled(False)
        eval(f'self.pre_max_{name}').setEnabled(False)

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

        self.check_action()
        self.check_func()

    def read_data(self):
        data = []

        addr = self.start_addr

        data.append(self.get_value(addr + 0, self.btn_action_1))
        data.append(self.get_value(addr + 1, self.btn_func_1))
        data.append(self.get_value(addr + 2, self.pc_num_1))
        data.append(self.get_value(addr + 3, self.cc_num_1))
        data.append(self.get_value(addr + 4, self.cc_value_1))
        data.append(self.get_value(addr + 5, self.midi_ch_1))
        data.append(self.get_value(addr + 6, self.scene_1))
        data.append(self.get_value(addr + 7, self.pre_min_1))
        data.append(self.get_value(addr + 8, self.pre_max_1))
        data.append(self.get_value(addr + 9, self.btn_label_1))
        addr += self.label_size + 9

        data.append(self.get_value(addr + 0, self.btn_action_2))
        data.append(self.get_value(addr + 1, self.btn_func_2))
        data.append(self.get_value(addr + 2, self.pc_num_2))
        data.append(self.get_value(addr + 3, self.cc_num_2))
        data.append(self.get_value(addr + 4, self.cc_value_2))
        data.append(self.get_value(addr + 5, self.midi_ch_2))
        data.append(self.get_value(addr + 6, self.scene_2))
        data.append(self.get_value(addr + 7, self.pre_min_2))
        data.append(self.get_value(addr + 8, self.pre_max_2))
        data.append(self.get_value(addr + 9, self.btn_label_2))
        addr += self.label_size + 9

        data.append(self.get_value(addr + 0, self.btn_action_3))
        data.append(self.get_value(addr + 1, self.btn_func_3))
        data.append(self.get_value(addr + 2, self.pc_num_3))
        data.append(self.get_value(addr + 3, self.cc_num_3))
        data.append(self.get_value(addr + 4, self.cc_value_3))
        data.append(self.get_value(addr + 5, self.midi_ch_3))
        data.append(self.get_value(addr + 6, self.scene_3))
        data.append(self.get_value(addr + 7, self.pre_min_3))
        data.append(self.get_value(addr + 8, self.pre_max_3))
        data.append(self.get_value(addr + 9, self.btn_label_3))
        addr += self.label_size + 9

        data.append(self.get_value(addr + 0, self.btn_action_4))
        data.append(self.get_value(addr + 1, self.btn_func_4))
        data.append(self.get_value(addr + 2, self.pc_num_4))
        data.append(self.get_value(addr + 3, self.cc_num_4))
        data.append(self.get_value(addr + 4, self.cc_value_4))
        data.append(self.get_value(addr + 5, self.midi_ch_4))
        data.append(self.get_value(addr + 6, self.scene_4))
        data.append(self.get_value(addr + 7, self.pre_min_4))
        data.append(self.get_value(addr + 8, self.pre_max_4))
        data.append(self.get_value(addr + 9, self.btn_label_4))
        addr += self.label_size + 9

        data.append(self.get_value(addr + 0, self.btn_action_5))
        data.append(self.get_value(addr + 1, self.btn_func_5))
        data.append(self.get_value(addr + 2, self.pc_num_5))
        data.append(self.get_value(addr + 3, self.cc_num_5))
        data.append(self.get_value(addr + 4, self.cc_value_5))
        data.append(self.get_value(addr + 5, self.midi_ch_5))
        data.append(self.get_value(addr + 6, self.scene_5))
        data.append(self.get_value(addr + 7, self.pre_min_5))
        data.append(self.get_value(addr + 8, self.pre_max_5))
        data.append(self.get_value(addr + 9, self.btn_label_5))
        addr += self.label_size + 9

        data.append(self.get_value(addr + 0, self.btn_action_6))
        data.append(self.get_value(addr + 1, self.btn_func_6))
        data.append(self.get_value(addr + 2, self.pc_num_6))
        data.append(self.get_value(addr + 3, self.cc_num_6))
        data.append(self.get_value(addr + 4, self.cc_value_6))
        data.append(self.get_value(addr + 5, self.midi_ch_6))
        data.append(self.get_value(addr + 6, self.scene_6))
        data.append(self.get_value(addr + 7, self.pre_min_6))
        data.append(self.get_value(addr + 8, self.pre_max_6))
        data.append(self.get_value(addr + 9, self.btn_label_6))

        return data
