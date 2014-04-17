import os
import sys
 
# Install venv by `virtualenv --distribute venv`
# Then install depedencies: `source venv/bin/active`
# `pip install -r requirements.txt`
activate_this = os.path.dirname(__file__) + '/muzik-venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
 
path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.append(path)
 
# The application object is used by any WSGI server configured to use this
# file.
 
# Ensure there is an app.py script in the current folder
from muzik import app as application
