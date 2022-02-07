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

# Default Imports
import os
import sys
import json
import subprocess
from functools import partial

# Site-Packages
from PySide2.QtWidgets import *

# Custom
from themes import dark
from layout.gui import Ui_MainWindow

with open('layout/layout.json') as json_file:
    _layout_data = json.load(json_file)

script_dir = os.path.dirname(__file__)


def get_tabs():
    tab_names = []
    for tab in _layout_data:
        tab_names.append(tab)
    return tab_names


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Init inherited
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Launcher')
        self.setWindowIcon(QIcon('icon.png'))

        # Clean existing info
        self.dynamicTabWidget.removeTab(0)

        # Set layout
        self.fill_tabs()

    def execute_command(self, cmd):
        # Execute command
        action = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = action.communicate(input='x'.encode())[0]
        output = output.decode('ascii')

        # Update UI
        current = self.logTextEdit.toPlainText()
        log = current + '\n' + output
        self.logTextEdit.setPlainText(log)

    def fill_tabs(self):
        tabs = get_tabs()
        catalog = {'button': QPushButton, 'label': QLabel}
        for tab in tabs:
            new_tab = QTabWidget()
            self.dynamicTabWidget.addTab(new_tab, tab)
            grid_layout = QGridLayout(new_tab)
            x, y = 0, 0
            tab_items = _layout_data[tab]
            for item_label, value in tab_items.items():
                item_type = value['class']

                new_item = catalog[item_type](item_label)
                if item_type == 'button':
                    item_target = os.path.relpath(value['target'])
                    abs_file_path = os.path.join(script_dir, item_target)
                    new_item.clicked.connect(partial(self.execute_command, cmd=item_target))

                grid_layout.addWidget(new_item, y, x)
                if x == 2:
                    x = 0
                    y += 1
                else:
                    x += 1


if __name__ == "__main__":
    # Qapp thingy
    app = QApplication(sys.argv)

    # Set dark theme
    dark.set_dark_theme(app)

    # Start window
    MainWindow = MainWindow()
    MainWindow.show()

    sys.exit(app.exec_())
