import traceback
from SalomePyQt import *
from qtsalome import *

import export_salome_mesh

# Get SALOME PyQt interface
sgPyQt = SalomePyQt()

################################################
# GUI context class
# Used to store actions, menus, toolbars, etc...
################################################

class GUIcontext:

    # constructor
    def __init__( self ):
        # about action
        sgPyQt.createAction(dict_actions["about"], "about", "software information")
        # Save File action
        sgPyQt.createAction(dict_actions["savemesh"], "Save mesh File", "Save mesh file")
        # Create 'mesh_app' menu
        menumesh_app = sgPyQt.createMenu( "mesh_app", -1, -1, 50)
        # Add actions in the menu 'mesh_app'
        sgPyQt.createMenu( dict_actions["about"], menumesh_app, 10 )
        # Add actions in the menu 'mesh_app'
        sgPyQt.createMenu( dict_actions["savemesh"], menumesh_app, 10 )

def about():
    import salome
    import os
    QMessageBox.information(sgPyQt.getDesktop(),"Information",
    "current work directory"+os.path.dirname(salome.myStudy._get_URL()))

def savemesh():
    from export_salome_mesh import *
    export()

################################################
# verbosity level
__verbose__ = None

###
# Get verbose level
###
def verbose():
    global __verbose__
    if __verbose__ is None:
        try:
            __verbose__ = int( os.getenv( 'SALOME_VERBOSE', 0 ) )
        except:
            __verbose__ = 0
            pass
        pass
    return __verbose__

# Create actions and menus
def initialize():
    if verbose(): print("mesh_appGUI::initialize()")
    return

# called when module is activated
# returns True if activating is successfull and False otherwise
def activate():
    if verbose() : print("mesh_appGUI.activate()")
    GUIcontext()
    return True

# called when module is deactivated
def deactivate():
    if verbose() : print("mesh_appGUI.deactivate()")
    pass

# Process GUI action
def OnGUIEvent(commandID):
    if verbose() : print("mesh_appGUI::OnGUIEvent : commandID = %d" % commandID)
    if commandID in dict_command:
        try:
            dict_command[commandID]()
        except:
            traceback.print_exc()
    else:
       if verbose() : print("The command is not implemented: %d" % commandID)
    pass


# Define commands
dict_command = {
    991 : about,
    992 : savemesh,
    }

# Define actions
dict_actions = {
    "about"   :    991,
    "savemesh":    992,
    }
