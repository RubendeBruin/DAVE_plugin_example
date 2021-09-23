from PySide2.QtWidgets import QPushButton
from balloon import BalloonDock
from .balloon_node import Balloon
from .ballon_editor import BalloonNodeEditor
from DAVE.gui.main import guiEventType

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

def plugin_context(menu, node_name,gui):
    code = 'from balloon import Balloon\nBalloon(s, s.available_name_like("new_balloon"))'
    def action():
        gui.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

    menu.addAction("Add balloon", action)
