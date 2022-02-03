from PySide2 import QtWidgets

from DAVE.gui.widget_nodeprops import NodeEditor, Singleton, DAVE_GUI_NODE_EDITORS
from balloon.balloon_node import Balloon

@Singleton
class BalloonNodeEditor(NodeEditor):

    def __init__(self):
        """Create the gui, store the main widget as self._widget"""

        print('creating widgets for balloon')
        self._widget =  QtWidgets.QWidget()

        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        label.setText('Im the editor for balloon')
        self.spinbox = QtWidgets.QSpinBox()
        self.spinbox.setMinimum(0)
        self.spinbox.setMaximum(10000)
        self.spinbox.setValue(30)

        layout.addWidget(label)
        layout.addWidget(self.spinbox)

        self.spinbox.valueChanged.connect(self.generate_code)

        self._widget.setLayout(layout)


    def post_update_event(self):
        """Sync the properties of the node to the gui"""

        self.spinbox.blockSignals(True)
        self.spinbox.setValue(self.node.balloon_size)
        self.spinbox.blockSignals(False)

    def generate_code(self):
        """Generate code to update the node, then run it"""

        value = self.spinbox.value()
        if value != self.node.balloon_size:
            code =  f"s['{self.node.name}'].balloon_size = {value}"
        else:
            code = ''

        self.run_code(code)

DAVE_GUI_NODE_EDITORS[Balloon] = BalloonNodeEditor
