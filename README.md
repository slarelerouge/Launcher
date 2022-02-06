# Dynamic Launcher
Dynamic launcher that can be configured. Read the description below for more information.

Includes: 
- layout/
    - .ui file used to generate initial UI.
    - .py file, autogenerated from the UI. 
    - layout.json, which can be treated as the config file where you can customize tabs and actions. 
- test_targets/
    - Folder that contains test ".bat" files to link to WIP buttons.
- themes/
    - Folder to add your PySide2 themes.
    
Installation steps:
1. Download the .zip file.
2. Customize the "layout.json".
3. Navigate to the directory containing the main.py
3. Use the command line to launch your application.
    `python main.py`

Pre-Requisites:
- Python 3.+ must be installed on your local computer. 
- PySide2 must be installed on your local computer. 