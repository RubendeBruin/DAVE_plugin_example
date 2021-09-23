from DAVE import *
from DAVE.gui import Gui

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


Gui(s,
    plugins_init=[plugin_init],
    plugins_workspace = [plugin_activate_workspace],
    plugins_editor = [plugin_node_editor],
    plugins_context= [plugin_context])
