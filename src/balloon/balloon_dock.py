from PySide2 import QtWidgets, QtCore

from DAVE.gui.dockwidget import *

class BalloonDock(guiDockWidget):

    def guiCreate(self):
        """Is fired when created

        add gui widgets to self.contents
        """

        # Example code
        label = QtWidgets.QLabel(self.contents)
        label.setText("I'm the balloon widget")

        button = QtWidgets.QPushButton()
        button.clicked.connect(self.new_balloon)
        button.setText('Click me')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.contents.setLayout(layout)

    def new_balloon(self):
        QtWidgets.QMessageBox.information(self,
                                          'Up Up!',
                                          'We could have done something usefull here\nBut we will just run some code',
                                          QtWidgets.QMessageBox.Ok)
        self.guiRunCodeCallback("print('nothing special')", None)

    def guiDefaultLocation(self):
        """Return the default location, or None for floating"""
        return None

DAVE_GUI_DOCKS['Balloon'] = BalloonDock