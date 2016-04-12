#!/usr/bin/python
import os
import sys

file_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, file_path)

activate_this = os.path.join(file_path, '/env/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from werkzeug.debug import DebuggedApplication
from app import app
application = DebuggedApplication(app, True)
application.debug = True

