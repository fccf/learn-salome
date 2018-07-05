import traceback
from SalomePyQt import *
from qtsalome import *

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
        # Create 'fish_app' menu
        menufish_app = sgPyQt.createMenu( "fish_app", -1, -1, 50)
        # Add actions in the menu 'fish_app'
        sgPyQt.createMenu( dict_actions["about"], menufish_app, 10 );


def about():
    QMessageBox.information(sgPyQt.getDesktop(),"Information","fish is a radiation shielding calculation program using finite element & spherical harmonics method")

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
    if verbose(): print("fish_appGUI::initialize()")
    return

# called when module is activated
# returns True if activating is successfull and False otherwise
def activate():
    if verbose() : print("fish_appGUI.activate()")
    GUIcontext()
    return True

# called when module is deactivated
def deactivate():
    if verbose() : print("fish_appGUI.deactivate()")
    pass

# Process GUI action
def OnGUIEvent(commandID):
    if verbose() : print("fish_appGUI::OnGUIEvent : commandID = %d" % commandID)
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
    }

# Define actions
dict_actions = {
    "about"   :    991,
    }
