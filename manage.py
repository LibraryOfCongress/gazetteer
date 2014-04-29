#!/usr/bin/env python
import os
import sys


root_dir = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
os.chdir(root_dir)

#using virtualenv's activate_this.py to reorder sys.path
activate_this = os.path.join(root_dir, 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))



if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gazetteer.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
