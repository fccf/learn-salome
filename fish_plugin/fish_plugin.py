try:
    from PyQt4 import QtGui
    from PyQt4 import QtCore
except ImportError:
    from PyQt5 import QtWidgets as QtGui
    from PyQt5 import QtCore


widget = None

def control(context):
    global widget, about, showMaterials, showBoundaryConditions,startSolver
    global QtCore

    # QWidget
    widget = QtGui.QWidget()
    widget.setWindowTitle('Fish')
    widget.setWindowFlags(widget.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

    # QPushButtons
    button_about = QtGui.QPushButton('About', widget)
    button_mat = QtGui.QPushButton('Materials', widget)
    button_bc = QtGui.QPushButton('Boundary conditions', widget)
    button_solve = QtGui.QPushButton('Run', widget)

    # QPushButton-Events
    button_about.clicked.connect(lambda: about(context))
    button_mat.clicked.connect(lambda: showMaterials(context))
    button_bc.clicked.connect(lambda: showBoundaryConditions(context))
    button_solve.clicked.connect(lambda: startSolver(context))

    layout = QtGui.QVBoxLayout()
    layout.addWidget(button_about)
    layout.addWidget(button_mat)
    layout.addWidget(button_bc)
    layout.addWidget(button_solve)

    widget.setLayout(layout)

    widget.show()

# %% define about Function
def about(context):
    """Shows an info dialog for the plugin. May contain additional information
    in the future.

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """
    global QtGui
    # get active module and check if SMESH
    active_module = context.sg.getActiveComponent()
    if active_module != "SMESH":
        QtGui.QMessageBox.about(None, str(active_module),
                                "Functionality is only provided in mesh module.")
        return

    title = "Fish interface for SALOME editor"
    msg = "by c.fang"
    QtGui.QMessageBox.about(None, title, msg)
    return

# %% material defintion
def showMaterials(context):
    """Shows the window for the definition of materials.

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """
    global QtGui
    # get active module and check if SMESH
    active_module = context.sg.getActiveComponent()
    if active_module != "SMESH":
        QtGui.QMessageBox.information(None, str(active_module),
                                "Functionality is only provided in mesh module.")
        return

    title = "Fish material interface for SALOME editor"
    msg = "by c.fang"
    QtGui.QMessageBox.about(None, title, msg)
    return

# %% boundary conditions
def showBoundaryConditions(context):
    """Shows the window for the definition of boundary conditions.

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """
    global QtGui
    # get active module and check if SMESH
    active_module = context.sg.getActiveComponent()
    if active_module != "SMESH":
        QtGui.QMessageBox.information(None, str(active_module),
                                "Functionality is only provided in mesh module.")
        return

    title = "Fish BC interface for SALOME editor"
    msg = "by c.fang"
    QtGui.QMessageBox.about(None, title, msg)
    return

# %% call to ElmerSolver
def startSolver(context):
    """Calls the ElmerSolver. Checks if a sif-file is present and whether
    multiprocessing is available.

    Args:
    -----
    context: salome context
        Context variable provided by the Salome environment
    """
    global QtGui
    # get active module and check if SMESH
    active_module = context.sg.getActiveComponent()
    if active_module != "SMESH":
        QtGui.QMessageBox.information(None, str(active_module),
                                "Functionality is only provided in mesh module.")
        return

    title = "Fish solver interface for SALOME editor"
    msg = "by c.fang"
    QtGui.QMessageBox.about(None, title, msg)
    return
