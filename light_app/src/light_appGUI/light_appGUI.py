# Copyright (C) 2009-2016  OPEN CASCADE
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

#  Author : Roman NIKOLAEV, Open CASCADE S.A.S. (roman.nikolaev@opencascade.com)
#  Date   : 13/04/2009
#
import traceback
from SalomePyQt import *
import light_app_DataModel
from qtsalome import *
import libSALOME_Swig

import os
import libSalomePy
import vtk

# Get SALOME PyQt interface
sgPyQt = SalomePyQt()
# Get SALOME Swig interface
sg = libSALOME_Swig.SALOMEGUI_Swig()

################################################
# GUI context class
# Used to store actions, menus, toolbars, etc...
################################################

# data model
__data_model__ = None

class GUIcontext:

    # constructor
    def __init__( self ):
        global __data_model__
        # Load File action
        sgPyQt.createAction(dict_actions["loadfile"], "Load text File", "Load text file")
        # Save File action
        sgPyQt.createAction(dict_actions["savefile"], "Save text File", "Save text file")
        # Insert Line action
        sgPyQt.createAction(dict_actions["insertLine"], "Insert Line", "Insert new text line")
        # Insert new line action
        sgPyQt.createAction(dict_actions["insertLine"], "Insert Line", "Insert new line")
        # Edit selected line action
        sgPyQt.createAction(dict_actions["editLine"], "Edit Line", "Edit selected line")
        # Remove selected line action
        sgPyQt.createAction(dict_actions["removeLine"], "Remove Lines", "Remove selected lines")
        # Clear paragraph
        sgPyQt.createAction(dict_actions["clearParagraph"], "Clear Paragraph", "Clear selected paragraph")
        # Clear all paragraphs
        sgPyQt.createAction(dict_actions["clearAll"], "Clear All", "Clear all paragraphs")
        # Display line
        sgPyQt.createAction(dict_actions["displayLine"], "Display Line", "Display selected line")
        # Erase line
        sgPyQt.createAction(dict_actions["eraseLine"], "Erase Line", "Erase selected line")
        # Separator
        separator = sgPyQt.createSeparator()

        # # Get Menu 'File'
        # menuFile = sgPyQt.createMenu( "File", -1, -1 )
        # # Add actions in the menu 'File'
        # sgPyQt.createMenu( separator,                menuFile, -1, 10)
        # sgPyQt.createMenu( dict_actions["loadfile"], menuFile, 10 );
        # sgPyQt.createMenu( dict_actions["savefile"], menuFile, 10 );
        # sgPyQt.createMenu( separator,                menuFile, -1, 10)
        # Create 'light_app' menu
        menulight_app = sgPyQt.createMenu( "light_app", -1, -1, 50)
        # Add actions in the menu 'light_app'
        sgPyQt.createMenu( separator,                menulight_app, -1, 10)
        sgPyQt.createMenu( dict_actions["loadfile"], menulight_app, 10 );
        sgPyQt.createMenu( dict_actions["savefile"], menulight_app, 10 );
        sgPyQt.createMenu( separator,                menulight_app, -1, 10)
        sgPyQt.createMenu( dict_actions["insertLine"],  menulight_app, 10 );
        sgPyQt.createMenu( dict_actions["editLine"],    menulight_app, 10 );
        sgPyQt.createMenu( dict_actions["removeLine"],  menulight_app, 10 );
        sgPyQt.createMenu( separator,                   menulight_app, -1, 10);
        sgPyQt.createMenu( dict_actions["clearAll"],    menulight_app, 10 );
        sgPyQt.createMenu( separator,                   menulight_app, -1, 10);
        sgPyQt.createMenu( dict_actions["displayLine"], menulight_app, 10 );
        sgPyQt.createMenu( dict_actions["eraseLine"],   menulight_app, 10 );

        # Create DataModel
        if __data_model__ is None:
            __data_model__ = light_app_DataModel.light_app_DataModel()
            pass

        pass # def __init__( self )

    pass # class GUIcontext

################################################
# Global variables and functions
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

################################################

# Create actions and menus
def initialize():
    if verbose(): print("light_appGUI::initialize()")
    return

# called when module is activated
# returns True if activating is successfull and False otherwise
def activate():
    if verbose() : print("light_appGUI.activate()")
    GUIcontext()
    return True

# called when module is deactivated
def deactivate():
    if verbose() : print("light_appGUI.deactivate()")
    pass

# Process GUI action
def OnGUIEvent(commandID):
    if verbose() : print("light_appGUI::OnGUIEvent : commandID = %d" % commandID)
    if commandID in dict_command:
        try:
            dict_command[commandID]()
        except:
            traceback.print_exc()
    else:
       if verbose() : print("The command is not implemented: %d" % commandID)
    pass

# Customize popup menu
def createPopupMenu(popup, context):
    global __data_model__
    if verbose() : print("light_appGUI.createPopupMenu(): context = %s" % context)

    if context != 'ObjectBrowser':
        return

    selcount = sg.SelectedCount()
    if selcount == 1:
        entry = sg.getSelected( 0 )
        obj = __data_model__.getObject(entry)
        if obj is not None:
            if obj.getText() != "\n":
                # Line is selected
                popup.addAction(sgPyQt.action(dict_actions["editLine"]))
                popup.addAction(sgPyQt.action(dict_actions["removeLine"]))
                popup.addSeparator()
                popup.addAction(sgPyQt.action(dict_actions["displayLine"]))
                popup.addAction(sgPyQt.action(dict_actions["displayLine"]))
                popup.addAction(sgPyQt.action(dict_actions["eraseLine"]))
                pass
            else:
                # Paragraph is selected
                popup.addAction(sgPyQt.action(dict_actions["insertLine"]))
                popup.addAction(sgPyQt.action(dict_actions["clearParagraph"]))
                pass
            pass
        else:
            onlyLines = True
            pass
        pass # if selcount == 1
    pass

# For saving data in the study
def saveFiles(prefix):
    global __data_model__
    if verbose(): print("light_appGUI::saveFile()")
    postfix = "light_app.txt"
    filename = prefix+postfix
    __data_model__.saveFile(filename)
    return postfix

# For restore data from the study
def openFiles(filelist):
    global __data_model__
    if verbose(): print("light_appGUI::openFile()")
    filename =  filelist[0]
    filename.append(filelist[1])
    __data_model__.loadFile(filename)
    return True

# Loading a text file
def loadfile():
    global __data_model__
    aFilter = "Text files (*.txt)"
    filename = QFileDialog.getOpenFileName(sgPyQt.getDesktop(), "Open text file", "", aFilter, "Choose a text file to open")

    if isinstance(filename,tuple) and len(filename) >=2:
       filename = filename[0]

    if len(filename) == 0:
        return

    if os.access(str(filename),os.R_OK):
        __data_model__.loadFile(filename)
    else:
        QMessageBox.warning(sgPyQt.getDesktop(),
                            "Error!",
                            "Can not read file:\n%s"%(filename))
        pass
    sg.updateObjBrowser()
    pass

# Saving a text file
def savefile():
    global __data_model__
    aFilter = "Text files (*.txt)"
    filename = QFileDialog.getSaveFileName(sgPyQt.getDesktop(),"Save text file", "", aFilter, "Choose a text file to save")

    if isinstance(filename,tuple) and len(filename) >=2:
        filename = filename[0]

    if filename.endswith(".txt") == 0:
        filename+=".txt"
        pass

    fn = filename
    # Get directory name and check access
    if os.access(str(fn[:fn.rindex(os.path.sep)]), os.W_OK):
        __data_model__.saveFile(filename)
    else:
        QMessageBox.warning(sgPyQt.getDesktop(),
                            "Error!",
                            "Can not save file:\n%s"%(filename))
        pass
    pass

def insertLine():
    '''
    Insert new line in the selected paragraph.
    '''
    global __data_model__
    #Get result
    res = QInputDialog.getText(sgPyQt.getDesktop(),
                               "Add new line",
                               "Enter the text",
                               QLineEdit.Normal)
    if not res[1]: ### user click cancel button
        return

    text = res[0]
    # Nb selected objects
    selcount = sg.SelectedCount()
    # Nb object in the Data Model
    paragrCount = len(__data_model__.getParagraphs())

    # Create first paragraph
    if paragrCount == 0:
        __data_model__.createObject()
        # If line not empty create first line
        if text != "\n":
            __data_model__.createObject(text,__data_model__.getParagraphs()[0])
        sg.updateObjBrowser()
        return
    # Create paragraph
    if text == "\n":
        __data_model__.createObject()
        sg.updateObjBrowser()
        return
    else:
        if selcount == 0:
            QMessageBox.warning(sgPyQt.getDesktop(),
                                'Error!',
                                'Please, select paragraph!')
            return
        if selcount == 1:
            entry = sg.getSelected( 0 )
            obj = __data_model__.getObject(entry)
            if obj is not None:
                # Create line
                if(obj.getText() == "\n"):
                    __data_model__.createObject(text,entry)
                    sg.updateObjBrowser();
                    return
                else:
                    QMessageBox.warning(sgPyQt.getDesktop(),
                                        'Error!',
                                        'Please, select paragraph!')
            elif selcount > 1:
                QMessageBox.warning(sgPyQt.getDesktop(),
                                    'Error!',
                                    'Please, select only one paragraph!')
    pass


# Edit selected line
def editLine():
    global __data_model__
    if sg.SelectedCount() == 1:
        entry = sg.getSelected( 0 )
        obj = __data_model__.getObject(entry)
        if(obj is not None and obj.getText() != "\n"):
            #Get text line
            res = QInputDialog.getText(sgPyQt.getDesktop(),
                                       "Edit line",
                                       "Enter the text",
                                       QLineEdit.Normal,
                                       light_app_DataModel.processText(obj.getText()))
            if not res[1]: ### user click cancel button
                return
            text = res[0]

            obj.setText(text)
        else:
            QMessageBox.information(sgPyQt.getDesktop(),
                                    'Info',
                                    'Please, select line!')
    else:
        QMessageBox.information(sgPyQt.getDesktop(),
                                'Info',
                                'Please, select one line!')
    sg.updateObjBrowser();
    pass

# Remove selected lines
def removeLine():
    global __data_model__
    selcount = sg.SelectedCount()
    onlyLines = True
    lines = []
    while selcount != 0:
        entry = sg.getSelected( selcount - 1)
        #Check what only lines selected
        obj = __data_model__.getObject(entry)
        if obj is None:
            continue
        if obj.getText() == "\n":
            onlyLines = False
            break
        lines.append(entry)
        selcount = selcount-1
        pass
    if not onlyLines:
        return
    else:
        renderer=libSalomePy.getRenderer()
        for ln in lines:
            actor = getActor(ln)
            if actor is not None:
                renderer.RemoveActor(actor)
                pass
            pass
        __data_model__.removeObjects(lines)
        sg.updateObjBrowser()
        pass
    pass

# Remove all lines from all paragraphs
def clearAll():
    global __data_model__
    paragraphs = __data_model__.getParagraphs()
    for paragr in paragraphs:
        lines = sgPyQt.getChildren(paragr)
        __data_model__.removeObjects(lines)
        renderer=libSalomePy.getRenderer()
        for l in lines:
            actor = getActor(l)
            if actor is not None:
                renderer.RemoveActor(actor)
                pass
            pass
    sg.updateObjBrowser()
    pass

# Display the selected line
def displayLine():
    global __data_model__
    if sg.SelectedCount() != 1:
        return
    entry = sg.getSelected(0)
    obj = ctx.DM.getObject(entry)
    if obj is None:
        QMessageBox.information(sgPyQt.getDesktop(),
                                'Info',
                                'Please, select line!')
        return
    text = obj.getText()
    if text == "\n":
        return
    renderer=libSalomePy.getRenderer()
    actor = getActor(entry)
    if actor is None:
        actor = vtk.vtkTextActor()
        dict_actors[entry] = actor
        pass
    center = renderer.GetCenter()
    actor.SetInput(str(text))
    actor.SetPosition(center[0],center[1])
    txtPr = vtk.vtkTextProperty()
    txtPr.SetFontSize(30)
    actor.SetTextProperty(txtPr)
    for act in  list(dict_actors.values()):
        renderer.RemoveActor(act)
    renderer.AddActor(actor)
    pass

# Clear remove all lines under selected paragraph
def clearParagraph():
    global __data_model__
    lines = sgPyQt.getChildren(sg.getSelected(0))
    __data_model__.removeObjects(lines)
    sg.updateObjBrowser()
    pass

# Erase the selected line
def eraseLine():
    global __data_model__
    if sg.SelectedCount() != 1:
        return
    entry = sg.getSelected(0)
    obj = __data_model__.getObject(entry)
    if obj is None:
        QMessageBox.information(sgPyQt.getDesktop(),
                                'Info',
                                'Please, select line!')
        return
    text = obj.getText()
    if text == "\n":
        return
    renderer=libSalomePy.getRenderer()
    actor = getActor(entry)
    if actor is not None:
        renderer.RemoveActor(actor)
        pass
    pass

# Return vtkActor by entry
def getActor(entry):
    entry = str(entry)
    if entry in dict_actors:
        return dict_actors[entry]
    return None

# Define commands
dict_command = {
    951 : loadfile,
    952 : savefile,
    961 : insertLine,
    962 : editLine,
    963 : removeLine,
    964 : clearAll,
    971 : displayLine,
    972 : eraseLine,
    973 : clearParagraph,
    }

# Define actions
dict_actions = {
    "loadfile"   :    951,
    "savefile"   :    952,
    "insertLine" :    961,
    "editLine"   :    962,
    "removeLine" :    963,
    "clearAll"   :    964,
    "displayLine":    971,
    "eraseLine"  :    972,
    "clearParagraph": 973,
    }

# Define Actors
dict_actors = {}
