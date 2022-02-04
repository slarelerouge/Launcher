"""
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 3
"""

#!/usr/bin/python3
# -*- coding : utf-8 -*-

# IMPORT
import sys
import json
import subprocess
from PySide2.QtGui import *
from PySide2.QtWidgets import *


# CLASS

# Main window creation from layout data
class MainWindow( QMainWindow ):
    
    def __init__ (self, _layout_data) :
        # Window settings
        QMainWindow.__init__(self)
        self.setWindowTitle( 'Launcher' )
        self.setWindowIcon(QIcon('icon.png'))
        
        # Resize window
        self.resize(400, 300)
        
        # UI Dressing
        self._layout_data = _layout_data
        self._tabs = QTabWidget(self)
        self._scheduling = QWidget(self)
        
        ## Tabs
        ### Resize
        self._tabs.resize(300, 200)
        ### Fill in
        for tab_name in self._layout_data:
            tab_layout_data = self._layout_data[tab_name]
            tab = Tab(tab_layout_data).get_tab()
            self._tabs.addTab(tab, tab_name)
             
        ## Scheduling
        ### Resize
        self._scheduling.move(000, 250)
        ### Fill in
        label = QLabel("Scheduling", self._scheduling)
        frame = QFrame(self._scheduling)
        frame.setFrameShape(QFrame.StyledPanel)


# Tab creation from layout data
class Tab:

    def __init__(self, tab_layout_data):
        self._tab_layout_data = tab_layout_data

        # UI dressing
        self.tab = QWidget()
        
        # Create UI creation function catalog
        self._ui_item_catalog = {"button": self._create_button, "label": self._create_label}
        
        # Create every UI item
        for ui_item_name in tab_layout_data:
            ui_item_class = tab_layout_data[ui_item_name]["class"]
            self._create_ui_item(ui_item_name, ui_item_class)

    # Returns the actual tab QWidget
    def get_tab(self):
        return self.tab

    # Create the ui_item corresponding to the ui_item_class
    def _create_ui_item(self, ui_item_name, ui_item_class):
        self._ui_item_catalog[ui_item_class](ui_item_name)

    # Create a button in the tab from the layout data corresponding to the ui_item_name
    def _create_button(self, ui_item_name):
        # UI Dressing
        ui_item = self._tab_layout_data[ui_item_name]
        button = QPushButton(ui_item_name, self.tab)
        
        # Resize and position
        args = ui_item["position"]+ui_item["size"]
        button.setGeometry(*args)
        
        # Set click interaction
        button.clicked.connect(lambda: subprocess.call([ui_item["target"]]))

    # Create a label in the tab from the layout data corresponding to the ui_item_name
    def _create_label(self, ui_item_name):
        # UI Dressing
        ui_item = self._tab_layout_data[ui_item_name]
        label = QLabel(ui_item_name, self.tab)
        
        # Resize and position
        args = ui_item["position"]+ui_item["size"]
        label.setGeometry(*args)
        
    
# CORE
if __name__ == "__main__" :
    # Import window layout
    with open('layout/layout.json') as json_file:
        _layout_data = json.load(json_file)
    
    # Qapp thingy
    app = QApplication(sys.argv)

    #Start window
    MainWindow = MainWindow(_layout_data)
    MainWindow.show()
    
    sys.exit(app.exec_())