"""
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>. 3

Contributors:
Slarelerouge (github.com/slarelerouge)
Secarri ()
"""

# !/usr/bin/python3
# -*- coding : utf-8 -*-

# IMPORT
import sys
import json
import subprocess
import os
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import themes.dark
from enum import Enum, unique

# ENUM

# Set the type of action once clicking on a button
@unique
class ButtonStateEnum(Enum):
    """
    Enum to store the possible button state
    """
    CMD = 1
    SELECT = 2


# SINGLETON

# Singleton to store the current button state
class ButtonState:
    """
    Singleton to manage the button state, that allow to control how the dynamic buttons react to click
    """

    state = ButtonStateEnum.CMD

    def select(self):
        self.state = ButtonStateEnum.SELECT

    def cmd(self):
        self.state = ButtonStateEnum.CMD

    def is_select(self):
        if self.state is ButtonStateEnum.SELECT:
            return True
        return False

    def is_cmd(self):
        if self.state is ButtonStateEnum.CMD:
            return True
        return False

button_state = ButtonState()

# CLASS

# Main window creation from layout data
class MainWindow(QMainWindow):
    """
    Class to manage the main window of the Launcher.
    @string_dictionary layout_data: Json dictionary input to determine the layout of the dynamic buttons
    """

    def __init__(self, layout_data):
        self._layout_data = layout_data

        # Window settings
        QMainWindow.__init__(self)
        self.setWindowTitle('Launcher')
        #self.setWindowIcon(QIcon('icon.png'))
        
        # Resize main window
        self.resize(600, 500)

        # Create main group and main layout
        self._main_layout = QVBoxLayout()
        self._main_group = QGroupBox(self)
        self._main_group.setLayout(self._main_layout)

        # Create tab holder
        self._tabs = QTabWidget()
        # Layout filling
        self._main_layout.addWidget(self._tabs)
        # Creates the tab for the tab holder
        for tab_name in self._layout_data:
            tab_layout_data = self._layout_data[tab_name]
            tab = TabWidget(tab_layout_data)
            self._tabs.addTab(tab, tab_name)

        # Scheduler
        self.scheduler = Scheduler()
        self._main_layout.addWidget(self.scheduler)
        # Set as scheduler to be accessed from anywhere
        global scheduler
        scheduler = self.scheduler

        # Splitter between the tab area and the scheduler
        hsplitter = QSplitter(Qt.Vertical)
        hsplitter.addWidget(self._tabs)
        hsplitter.addWidget(self.scheduler)
        self._main_layout.addWidget(hsplitter)

        self.scheduler.load_scedule()

    #
    def set_select(self):
        for child in self._tabs.children():
            for child2 in child.children():
                for child3 in child2.children():
                    child3.set_select()

    def resizeEvent(self, event):
        self._main_group.resize(self.size())


# Scheduler widget creation
# A list of scheduled tasks, where time and occurence can be set as well as a set of subtasks
class Scheduler(QGroupBox):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Schedule dict
        self.schedule_name_list = []

        #
        self.setTitle("Scheduler")

        # Set layout to self
        self._schedule_layout = QHBoxLayout()
        self.setLayout(self._schedule_layout)

        # Schedule list buttons
        self.schedule_list_button_layout = QVBoxLayout()
        self.schedule_list_button_group = QGroupBox()
        self.schedule_list_button_group.setLayout(self.schedule_list_button_layout)
        #
        self.scroll = QScrollArea()
        #self.scroll.setWidget(self.schedule_list_button_group)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        #
        self.schedule_name_label = QLabel("Schedule Name")
        self.schedule_list_button_layout.addWidget(self.schedule_name_label)
        self.schedule_name = QLineEdit()
        self.schedule_list_button_layout.addWidget(self.schedule_name)
        #
        self.add_schedule_button = QPushButton("Create New")
        self.schedule_list_button_layout.addWidget(self.add_schedule_button)
        self.add_schedule_button.clicked.connect(lambda: self._create_schedule_item())
        #
        self.del_schedule_button = QPushButton("Delete")
        self.schedule_list_button_layout.addWidget(self.del_schedule_button)
        self.del_schedule_button.clicked.connect(lambda: self._remove_selected_schedule_item())
        #self.del_schedule_button.clicked.connect(lambda: self._schedule_list.takeItem(self._schedule_list.currentRow()))
        #
        self.save_schedule_button = QPushButton("Save")
        self.schedule_list_button_layout.addWidget(self.save_schedule_button)
        self.save_schedule_button.clicked.connect(lambda: self._save_schedule())

        self._schedule_layout.addWidget(self.schedule_list_button_group)
        #self._schedule_layout.addWidget(self.scroll)

        # Add schedule list
        self._schedule_list = QListWidget()
        self._schedule_layout.addWidget(self._schedule_list)
        self._schedule_list.itemSelectionChanged.connect(self._schedule_list_item_change)

        # Schedule list occurrence
        #
        self._stacked_time_panel = StackedTimePanel()
        self._schedule_layout.addWidget(self._stacked_time_panel)

        # Add task list
        self._stacked_task_list = StackedTasksList()
        self._schedule_layout.addWidget(self._stacked_task_list)

        # Add task list button
        self.schedule_task_list_button_layout = QVBoxLayout()
        self.schedule_task_list_button_group = QGroupBox()
        self.schedule_task_list_button_group.setLayout(self.schedule_task_list_button_layout)
        #
        self.add_button = QPushButton("Add Task")
        self.schedule_task_list_button_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(lambda: button_state.select())
        self.remove_button = QPushButton("Remove Task")
        self.schedule_task_list_button_layout.addWidget(self.remove_button)
        self.remove_button.clicked.connect(lambda: self._remove_selected_task())
        #
        self._schedule_layout.addWidget(self.schedule_task_list_button_group)

    def _add_task(self, button):
        self._stacked_task_list.get_current().addItem(button.text())

    def _remove_selected_task(self):
        current_tasks_list_widget = self._stacked_task_list.get_current()
        current_row = current_tasks_list_widget.currentRow()
        current_tasks_list_widget.takeItem(current_row)

    def _create_schedule_item(self):
        name = self.schedule_name.text()
        if name not in self.schedule_name_list:
            self._schedule_list.addItem(self.schedule_name.text())
        self._stacked_task_list.add_tasks_list()
        self._stacked_time_panel.add_panel()

        self.schedule_name_list.append(name)

    def _remove_selected_schedule_item(self):
        current_row = self._schedule_list.currentRow()
        self._schedule_list.takeItem(current_row)
        self._stacked_task_list.remove(current_row)
    
    def _save_schedule(self):
        # Recreate scheduled item anmes list
        schedule_name_list = []
        for i in range(self._schedule_list.count()):
            _dict = {}
            name = self._schedule_list.item(i).text()
            _dict["name"] = name
            schedule_name_list.append(name)
            time_panel = self._stacked_time_panel.get(i)
            _dict = _dict | self._stacked_time_panel.get_time(i)
            task_list_widget = self._stacked_task_list.get(i)
            task_count = task_list_widget.count()
            tasks = [task_list_widget.item(i).text() for i in range(task_count)]

            _dict["tasks"] = tasks
            with open(schedule_rw_path + name + ".json", "w") as schedule_json_file:
                json_object = json.dumps(_dict, indent=4)
                schedule_json_file.write(json_object)

        # Delete removed schedule
        listdir = os.listdir(schedule_rw_path)
        for file_name in listdir:
            if file_name.split(".")[0] not in schedule_name_list:
                os.remove(schedule_rw_path+file_name)

    def load_scedule(self):
        self._load_schedule()

    def _load_schedule(self):
        _dict = {}
        # Load all
        listdir = os.listdir(schedule_rw_path)
        for file_name in listdir:
            with open(schedule_rw_path + file_name, "r") as schedule_json_file:
                json_dict = json.load(schedule_json_file)
                _dict[json_dict["name"]] = json_dict

        print(_dict)


        for schedule_item in _dict:
            self._schedule_list.addItem(schedule_item)

            self._stacked_task_list.add_tasks_list()
            self._stacked_time_panel.add_panel()

            current_schedule_dict = _dict[schedule_item]

            self._stacked_time_panel.set_time(self._stacked_time_panel.count() - 1, current_schedule_dict)
            self._stacked_task_list.set_tasks(self._stacked_task_list.count() - 1, current_schedule_dict)


    def _schedule_list_item_change(self):
        idx = self._schedule_list.currentRow()
        self._stacked_task_list.set_current(idx)
        self._stacked_time_panel.set_current(idx)

    def _get_task_list(self):
        task_count = self._stacked_task_list.get_current().count()
        task_list = []
        for i in range(task_count):
            task_list.append(self._schedule_task_list.item(i).text())
        return task_list


class StackedWidgetWithDefault(QStackedWidget):
    def __init__(self):
        super().__init__()

    def remove(self, i):
        # Remove the i-th tasks list, but excluding the default
        widget = self.get(i)
        self.removeWidget(widget)

    def get(self, i):
        return self.widget(i + 1)

    def get_current(self):
        return self.currentWidget()

    def set_current(self, i):
        self.setCurrentIndex(i + 1)

    def count(self):
        return super().count() - 1


class StackedTasksList(StackedWidgetWithDefault):
    def __init__(self):
        super().__init__()
        # Add default tasks list
        self.add_tasks_list()
        # Select default tasks list
        self.set_current(-1)
tasks
    def add_tasks_list(self):
        schedule_task_list = QListWidget()
        self.addWidget(schedule_task_list)

    def set_tasks(self, i, tasks_dict):
        for tasks in tasks_dict["tasks"]:
            self.get(i).addItem(tasks)


class StackedTimePanel(StackedWidgetWithDefault):
    def __init__(self):
        super().__init__()
        self.add_panel()

    def add_panel(self):
        panel_group = QGroupBox()
        panel_group.setTitle("set occurrence")

        panel_layout = QVBoxLayout()
        panel_group.setLayout(panel_layout)

        occurrence_choice = QComboBox()
        occurrence_choice.addItems(["Once", "Every Day", "Every Week"])

        date_edit = QDateTimeEdit(QDate.currentDate())
        date_edit.setMinimumDate(QDate.currentDate().addDays(-365))
        date_edit.setMaximumDate(QDate.currentDate().addDays(365))
        date_edit.setDisplayFormat("dd.MM.yyyy")

        time_edit = QDateTimeEdit(QTime.currentTime())

        panel_layout.addWidget(date_edit)
        panel_layout.addWidget(time_edit)
        panel_layout.addWidget(occurrence_choice)

        self.addWidget(panel_group)

    def get_time(self, i):
        panel = self.get(i)
        children = panel.children()

        date = children[1].date().toString()
        time = children[2].time().toString()
        occurence = children[3].currentText()

        return {"date": date, "time": time, "occurence": occurence}

    def set_time(self, i, time_dict):
        date = QDate.fromString(time_dict["date"][4:], "MMM d yyyy")
        time = QTime.fromString(time_dict["time"], "hh:mm:ss")
        occurence = time_dict["occurence"]

        panel = self.get(i)
        children = panel.children()
        print("ch: ", children)
        print("children 0: ", )
        children[1].setDate(date)
        children[2].setTime(time)
        print(occurence)
        if occurence == "Once":
            children[3].setCurrentIndex(0)
        if occurence == "Every Day":
            children[3].setCurrentIndex(1)
        if occurence == "Every Week":
            children[3].setCurrentIndex(2)

# Tab creation from layout data
class TabWidget(QWidget):
    def __init__(self, tab_layout_data):
        super().__init__()

        self._tab_layout_data = tab_layout_data

        # Create every dynamic buttons for the UI
        for ui_item_name in tab_layout_data:
            if tab_layout_data[ui_item_name]["class"] == "button":
                button = DynButtonWidget(tab_layout_data[ui_item_name], ui_item_name, self)
                print(button.text())
                

# Dynamic button class that manage the buttons defined in the settings
class DynButtonWidget(QPushButton):
    def __init__(self, button_layout_data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Resize and position
        args = button_layout_data["position"] + button_layout_data["size"]
        self.setGeometry(*args)
        bat_path = os.path.normpath(button_layout_data["target"])
        if bat_path[0] == "\\":
            bat_path = bat_path[1:]
        self._call = os.path.join(os.path.abspath(sys.path[0]), bat_path)
        self.clicked.connect(lambda: self.on_click())

    def on_click(self):
        # Depending on the button state, execute the cmd or add it to the schedule
        if button_state.is_select():
            _add_task(self)
            button_state.cmd()
        elif button_state.is_cmd():
            rlt = subprocess.getoutput([self._call])
            print("rlt :" + rlt)


class DynLabelWidget():
    def __init__(self, label_layout_data, *args, **kwargs):
        super(DynLabelWidget, self).__init__(*args, **kwargs)


# FUNCTION
def _add_task(button):
    scheduler._add_task(button)


# PARAMETERS
# Paths should be defined from a cfg file
schedule_rw_path = "schedule/"
schedule_r_path = ""
layout_path = ""

try:
    os.mkdir(schedule_rw_path)
except:
    pass

# VARIABLES

scheduler = None


# FUNCTIONS

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