from PySide2.QtWidgets import QPushButton
from balloon import BalloonDock
from .balloon_node import Balloon
from .ballon_editor import BalloonNodeEditor

def plugin_init(gui):
    """Add a button to the tool-bar and set it to activate a workspace with the name "Balloon" """

    ui = gui.ui
    button = QPushButton()
    button.setText('Balloon workspace')
    button.clicked.connect(lambda: gui.activate_workspace("BALLOON"))

    # insert on the left of the action-bar
    before = ui.toolBar.actions()[1]
    ui.toolBar.insertWidget(before, button)

def plugin_activate_workspace(gui, workspacename):

    print('calling activateworkspace')

    if workspacename.upper() == 'BALLOON':
        gui.show_guiWidget('BALLOON',BalloonDock)

    return False

def plugin_node_editor(node):
    if isinstance(node, Balloon):
        return BalloonNodeEditor