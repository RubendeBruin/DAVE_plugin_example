from DAVE import *
from DAVE.gui import Gui

from balloon import *

s = Scene()

new_balloon(s, "test balloon")

Gui(s,
    plugins_init=[plugin_init],
    plugins_workspace = [plugin_activate_workspace],
    plugins_editor = [plugin_node_editor])
