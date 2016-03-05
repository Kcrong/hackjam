#!/usr/bin/python

import sys
sys.path.insert(0, '/home/hyunwoo/wargame_bt')

activate_this = '/home/hyunwoo/wargame_bt/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from werkzeug.debug import DebuggedApplication
from app import app
application = DebuggedApplication(app, True)
application.debug = True

