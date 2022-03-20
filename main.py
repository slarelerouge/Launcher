"""
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>. 3
"""

# !/usr/bin/python3
# -*- coding : utf-8 -*-

# IMPORT
import sys
import json
import subprocess
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import themes.dark
import schedule


# CLASS

# Main window creation from layout data
class MainWindow(QMainWindow):
    def __init__(self, _layout_data):
        self._layout_data = _layout_data

        # Window settings
        QMainWindow.__init__(self)
        self.setWindowTitle('Launcher')
        self.setWindowIcon(QIcon('icon.png'))

        self.selected = None
        
        # Resize main window
        self.resize(400, 300)

        # Create main group and main layout
        self.main_group = QGroupBox("launcher", self)
        self.main_layout = QVBoxLayout()
        self.main_group.setLayout(self.main_layout)

        # Create tab holder
        self._tabs = QTabWidget()
        # Layout filling
        self.main_layout.addWidget(self._tabs)
        # Fill in tabs
        for tab_name in self._layout_data:
            tab_layout_data = self._layout_data[tab_name]
            tab = Tab(tab_layout_data)
            self._tabs.addTab(tab, tab_name)

        self._scheduling_group = Scheduler()
        self.main_layout.addWidget(self._scheduling_group)

        """# Create schedule group and schedule layout
        self._scheduling_group = QGroupBox("Scheduler", self)
        self._schedule_layout = QHBoxLayout()
        self._scheduling_group.setLayout(self._schedule_layout)
        # Layout filling
        self.main_layout.addWidget(self._scheduling_group)
        # Fill in schedule
        # Time group and layout
        self.time_group = QGroupBox(self)
        self.time_layout = QVBoxLayout()
        self.time_group.setLayout(self.time_layout)
        self._schedule_layout.addWidget(self.time_group)
        #
        date_edit = QDateTimeEdit(QDate.currentDate())
        date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        date_edit.setMaximumDate(QDate.currentDate().addDays(365))
        date_edit.setDisplayFormat("yyyy.MM.dd")
        #
        time_edit = QDateTimeEdit(QTime.currentTime())
        #
        self.time_layout.addWidget(date_edit)
        self.time_layout.addWidget(time_edit)
        #
        self.buttons_group = QGroupBox(self)
        self.buttons_layout = QVBoxLayout()
        self.buttons_group.setLayout(self.buttons_layout)
        self._schedule_layout.addWidget(self.buttons_group)
        #
        occurrence_choice = QComboBox()
        occurrence_choice.addItems(["Once", "Every Day", "Every Week"])
        self.buttons_layout.addWidget(occurrence_choice)
        #
        self.list_w = QListWidget()
        #self.list_w.addItem("test")
        #self.list_w.addItem("test2")
        self.list_w_group = QGroupBox(self)
        self.list_w_layout = QHBoxLayout()
        self.list_w_group.setLayout(self.list_w_layout)
        self.list_w_layout.addWidget(self.list_w)
        self._schedule_layout.addWidget(self.list_w)
        #
        select_button = QPushButton("Select Task")
        self.buttons_layout.addWidget(select_button)
        select_button.clicked.connect(lambda: self.set_select())
        add_button = QPushButton("Add To Schedule")
        self.buttons_layout.addWidget(add_button)
        add_button.clicked.connect(lambda: self._deselect())"""

    def _deselect(self):
        print(self.selected)
        try:
            #self.list_w.addItem(self.selected.text())
            self.selected = None
        except:
            pass

    def set_select(self):
        for child in self._tabs.children():
            for child2 in child.children():
                for child3 in child2.children():
                    child3.set_select()

    def set_call(self):
        for child in self._tabs.children():
            for child2 in child.children():
                for child3 in child2.children():
                    child3.set_call()

    def resizeEvent(self, event):
        self.main_group.resize(self.size())

    def add_schedule_task(self):
        self._scheduling_group.add_schedule_task()


# Scheduler widget creation
# A list of scheduled tasks, where time and occurence can be set as well as a set of subtasks
class Scheduler(QGroupBox):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Set layout to self
        self._schedule_layout = QHBoxLayout()
        self.setLayout(self._schedule_layout)

        # Schedule list buttons
        self.schedule_lst_button_layout = QVBoxLayout()
        self.schedule_list_button_group = QGroupBox(self)
        self.schedule_list_button_group.setLayout(self.schedule_lst_button_layout)
        #
        self.schedule_name = QLineEdit()
        self.schedule_lst_button_layout.addWidget(self.schedule_name)
        #
        self.add_schedule_button = QPushButton("Create new")
        self.schedule_lst_button_layout.addWidget(self.add_schedule_button)
        self.add_schedule_button.clicked.connect(lambda: self._schedule_list.addItem(self.schedule_name.text()))
        #
        self.del_schedule_button = QPushButton("Delete")
        self.schedule_lst_button_layout.addWidget(self.del_schedule_button)
        self.del_schedule_button.clicked.connect(lambda: self._schedule_list.takeItem(self._schedule_list.currentRow()))
        #
        self._schedule_layout.addWidget(self.schedule_list_button_group)

        # Add schedule list
        self._schedule_list = QListWidget()
        self._schedule_layout.addWidget(self._schedule_list)

        # Schedule list occurrence
        #
        self.occurrence_choice = QComboBox()
        self.occurrence_choice.addItems(["Once", "Every Day", "Every Week"])
        #
        self.schedule_list_occurrence_layout = QVBoxLayout()
        self.schedule_list_occurrence_group = QGroupBox(self)
        self.schedule_list_occurrence_group.setLayout(self.schedule_list_occurrence_layout)
        self.schedule_list_occurrence_group.setTitle("set occurrence")
        #
        self.date_edit = QDateTimeEdit(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.date_edit.setMaximumDate(QDate.currentDate().addDays(365))
        self.date_edit.setDisplayFormat("yyyy.MM.dd")
        #
        self.time_edit = QDateTimeEdit(QTime.currentTime())
        #
        self.schedule_list_occurrence_layout.addWidget(self.date_edit)
        self.schedule_list_occurrence_layout.addWidget(self.time_edit)
        self.schedule_list_occurrence_layout.addWidget(self.occurrence_choice)
        #
        self._schedule_layout.addWidget(self.schedule_list_occurrence_group)

        # Add schedule list
        self._schedule_task_list = QListWidget()
        self._schedule_layout.addWidget(self._schedule_task_list)
        #
        self.schedule_task_list_button_layout = QVBoxLayout()
        self.schedule_task_list_button_group = QGroupBox(self)
        self.schedule_task_list_button_group.setLayout(self.schedule_task_list_button_layout)
        #
        self.select_button = QPushButton("Add Task")
        self.schedule_task_list_button_layout.addWidget(self.select_button)
        self.select_button.clicked.connect(lambda: self.set_select())
        self.add_button = QPushButton("Remove Task")
        self.schedule_task_list_button_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(lambda: self._deselect())
        #
        self._schedule_layout.addWidget(self.schedule_task_list_button_group)

        """# Schedule list group
        self.schedule_list_group = QGroupBox(self)
        self.schedule_list_layout = QHBoxLayout()
        self.schedule_list_group.setLayout(self.schedule_list_layout)

        # Schedule_list_detail group
        self.schedule_list_occurrence_layout = QVBoxLayout()
        self.schedule_list_occurrence_group = QGroupBox(self)
        self.schedule_list_occurrence_group.setLayout(self.schedule_list_occurrence_layout)




        self.schedule_list_group.setLayout(self.schedule_list_layout)
        self._schedule_layout.addWidget(self.list_w)

        self.list_w_group = QGroupBox(self)
        self.list_w_layout = QHBoxLayout()
        self.list_w_group.setLayout(self.list_w_layout)
        self.list_w_layout.addWidget(self.list_w)
        self._schedule_layout.addWidget(self.list_w)

        # Fill in schedule
        # Time group and layout
        self.time_group = QGroupBox(self)
        self.time_layout = QVBoxLayout()
        self.time_group.setLayout(self.time_layout)
        self._schedule_layout.addWidget(self.time_group)
        date_edit = QDateTimeEdit(QDate.currentDate())
        date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        date_edit.setMaximumDate(QDate.currentDate().addDays(365))
        date_edit.setDisplayFormat("yyyy.MM.dd")
        #
        time_edit = QDateTimeEdit(QTime.currentTime())
        #
        self.time_layout.addWidget(date_edit)
        self.time_layout.addWidget(time_edit)
        #
        self.buttons_group = QGroupBox(self)
        self.buttons_layout = QVBoxLayout()
        self.buttons_group.setLayout(self.buttons_layout)
        self._schedule_layout.addWidget(self.buttons_group)
        #
        occurrence_choice = QComboBox()
        occurrence_choice.addItems(["Once", "Every Day", "Every Week"])
        self.buttons_layout.addWidget(occurrence_choice)
        #
        select_button = QPushButton("Select Task")
        self.buttons_layout.addWidget(select_button)
        add_button = QPushButton("Add To Schedule")
        self.buttons_layout.addWidget(add_button)"""

    def _deselect(self):
        print(self.parent().parent())
        try:
            self._schedule_task_list.addItem(self.parent().parent().selected.text())
            self.self.parent().parent().selected = None
        except:
            pass

    def set_select(self):
        self.parent().parent().set_select()
        #self._schedule_task_list.addItem(self.parent().parent().selected.text())
        #self.self.parent().parent().selected = None

    def add_schedule_task(self):
        self._schedule_task_list.addItem(self.parent().parent().selected.text())
        self.parent().parent().selected = None

    def set_call(self):
        self.parent().parent().set_call()


# Tab creation from layout data
class Tab(QWidget):
    def __init__(self, tab_layout_data):
        super().__init__()

        self._tab_layout_data = tab_layout_data

        # Create every UI item
        for ui_item_name in tab_layout_data:
            if tab_layout_data[ui_item_name]["class"] == "button":
                button = DynButton(tab_layout_data[ui_item_name], ui_item_name, self)
                print(button.text())
            #ui_item_class = tab_layout_data[ui_item_name]["class"]
            #_ui_item_catalog[ui_item_class](self, ui_item_name)

    def set_call(self):
        for child in self.children():
            if child.__class__ == DynButton:
                child.set_call()

    def set_select(self):
        for child in self.children():
            if child.__class__ == DynButton:
                child.set_select()


class DynButton(QPushButton):
    def __init__(self, button_layout_data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Resize and position
        args = button_layout_data["position"] + button_layout_data["size"]
        self.setGeometry(*args)
        self._call = button_layout_data["target"]
        print(self._call)

        self.set_call()

    def set_call(self):
        #self.clicked.connect(lambda x=self.call: subprocess.call([x]))
        #self.clicked.connect(lambda x=self.call: x)
        try:
            self.clicked.disconnect()
        except:
            pass
        self.clicked.connect(lambda: subprocess.call([self._call]))

    def set_select(self):
        try:
            self.clicked.disconnect()
        except:
            pass
        self.clicked.connect(lambda: self._be_selected())
        #self.set_call()

    def _be_selected(self):
        main_window = self.parent().parent().parent().parent().parent()
        main_window.selected = self
        main_window.add_schedule_task()
        main_window.set_call()


class DynLabel():
    def __init__(self):
        super(DynLabel, self).__init__()

# FUNCTION
# Create a button in the tab from the layout data corresponding to the ui_item_name
def _create_button(widget, ui_item_name):
    # UI Dressing
    ui_item = widget._tab_layout_data[ui_item_name]
    button = QPushButton(ui_item_name, widget)

    # Resize and position
    args = ui_item["position"] + ui_item["size"]
    button.setGeometry(*args)

    # Set click interaction
    button.clicked.connect(lambda: subprocess.call([ui_item["target"]]))

    return button

# Create a label in the tab from the layout data corresponding to the ui_item_name
def _create_label(widget, ui_item_name):
    # UI Dressing
    ui_item = widget._tab_layout_data[ui_item_name]
    label = QLabel(ui_item_name, widget)

    # Resize and position
    args = ui_item["position"] + ui_item["size"]
    label.setGeometry(*args)

# Create UI creation function catalog
_ui_item_catalog = {"button": _create_button, "label": _create_label}

# CORE

if __name__ == "__main__":
    # Import window layout
    with open('layout/layout.json') as json_file:
        _layout_data = json.load(json_file)
    
    # Qapp thingy
    app = QApplication(sys.argv)

    # To set dark theme uncomment line below
    themes.dark.set_dark_theme(app)

    # Start window
    MainWindow = MainWindow(_layout_data)
    MainWindow.show()
    
    sys.exit(app.exec_())