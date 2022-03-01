from PySide2.QtGui import QIcon

from DAVE import *

from DAVE.settings import PROPS, PROPS_GUI,PROPS_SETTABLE

print('stop here')


from DAVE.gui import Gui
from DAVE.gui.dockwidget import guiEventType

from balloon import *

s = Scene()

#--- paint ---
# if new node types are introduced, then we need to tell the visuals engine how to paint them in each of the views.
# this can be done by adding entries to the PAINTERS dict.
# If the newly introduced type is an derivative of an already exising node type then it is sufficient to copy
# the already exising paint to a new key in the dict:
#
# import DAVE.settings_visuals as dvs
# for key, paintset in dvs.PAINTERS.items():
#     dvs.PAINTERS[key]["Balloon"] = dvs.PAINTERS[key]["Axis"]
#
# In this case this is not needed as balloon itself is not painted (only the nodes managed by balloon are)

new_balloon(s, "test balloon")

"""Normally the functions below would be added to the __init__.py files of the modules that define
the functionality such that they are automatically registered when imported.

For clarity of the example they are all placed together in this file.
"""


# ---- Adding a plugin to the interface start-up -----

def my_function(gui):
	print('executed on startup')

from DAVE.gui.main import DAVE_GUI_PLUGINS_INIT
DAVE_GUI_PLUGINS_INIT.append(my_function)

# ---- Adding a button -----

from DAVE.gui.main import DAVE_GUI_WORKSPACE_BUTTONS
DAVE_GUI_WORKSPACE_BUTTONS.insert(0,('BaLLoooon !', 'BALLOON'))  # insert tuple at front

# ---- Responding to the activate-workspace -----

def plugin_activate_workspace(gui, workspacename):
    print('calling activateworkspace')
    if workspacename.upper() == 'BALLOON':
        gui.show_guiWidget('Balloon')  # <-- ID of the balloon dock

from DAVE.gui.main import DAVE_GUI_PLUGINS_WORKSPACE
DAVE_GUI_PLUGINS_WORKSPACE.append(plugin_activate_workspace)

# ----- The context menu -----

def plugin_context(menu, node_name,gui):
    code = 'Balloon(s, s.available_name_like("new_balloon"))'
    def action():
        gui.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

    BalloonIcon = QIcon(str(Path(__file__).parent / 'balloon.png'))

    action = menu.addAction("Add balloon", action)
    action.setIcon(BalloonIcon)

from DAVE.gui.main import DAVE_GUI_PLUGINS_CONTEXT
DAVE_GUI_PLUGINS_CONTEXT.append(plugin_context)

Gui(s)
