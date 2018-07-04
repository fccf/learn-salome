# Copyright (C) 2007-2016  CEA/DEN, EDF R&D, OPEN CASCADE
#
# Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
# CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
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

# ---
# File   : first_appGUI.py
# Author : Vadim SANDLER, Open CASCADE S.A.S. (vadim.sandler@opencascade.com)
# ---
#
import traceback
import os
from qtsalome import *

from first_app_utils import *

################################################
# GUI context class
# Used to store actions, menus, toolbars, etc...
################################################

class GUIcontext:
    # menus/toolbars/actions IDs
    first_app_MENU_ID  = 90
    HELLO_ID         = 941
    CREATE_OBJECT_ID = 942
    OPTIONS_ID       = 943
    OPTION_1_ID      = 944
    OPTION_2_ID      = 945
    OPTION_3_ID      = 946
    PASSWORD_ID      = 947
    first_app_TB_ID    = 90
    DELETE_ALL_ID    = 951
    SHOW_ME_ID       = 952
    DELETE_ME_ID     = 953
    RENAME_ME_ID     = 954
    # default object name
    DEFAULT_NAME     = "Object"
    # default password
    DEFAULT_PASSWD   = "Passwd"

    # constructor
    def __init__( self ):
        # create top-level menu
        mid = sgPyQt.createMenu( "first_app", -1, GUIcontext.first_app_MENU_ID, sgPyQt.defaultMenuGroup() )
        # create toolbar
        tid = sgPyQt.createTool( "first_app" )
        # create actions and fill menu and toolbar with actions
        a = sgPyQt.createAction( GUIcontext.HELLO_ID, "Hello", "Hello", "Show hello dialog box", "Execfirst_app.png" )
        sgPyQt.createMenu( a, mid )
        sgPyQt.createTool( a, tid )
        a = sgPyQt.createSeparator()
        sgPyQt.createMenu( a, mid )
        a = sgPyQt.createAction( GUIcontext.CREATE_OBJECT_ID, "Create object", "Create object", "Create object" )
        sgPyQt.createMenu( a, mid )
        a = sgPyQt.createSeparator()
        sgPyQt.createMenu( a, mid )
        try:
            ag = sgPyQt.createActionGroup( GUIcontext.OPTIONS_ID )
            ag.setText( "Creation mode" )
            ag.setUsesDropDown(True)
            a = sgPyQt.createAction( GUIcontext.OPTION_1_ID, "Default name", "Default name", "Use default name for the objects" )
            a.setCheckable( True )
            ag.add( a )
            a = sgPyQt.createAction( GUIcontext.OPTION_2_ID, "Generate name", "Generate name", "Generate name for the objects" )
            a.setCheckable( True )
            ag.add( a )
            a = sgPyQt.createAction( GUIcontext.OPTION_3_ID, "Ask name", "Ask name", "Request object name from the user" )
            a.setCheckable( True )
            ag.add( a )
            sgPyQt.createMenu( ag, mid )
            sgPyQt.createTool( ag, tid )
            default_mode = sgPyQt.integerSetting( "first_app", "creation_mode", 0 )
            sgPyQt.action( GUIcontext.OPTION_1_ID + default_mode ).setChecked( True )
        except:
            pass
        a = sgPyQt.createSeparator()
        a = sgPyQt.createAction( GUIcontext.PASSWORD_ID, "Display password", "Display password", "Display password" )
        sgPyQt.createMenu( a, mid )
        
        # the following action are used in context popup
        a = sgPyQt.createAction( GUIcontext.DELETE_ALL_ID, "Delete all", "Delete all", "Delete all objects" )
        a = sgPyQt.createAction( GUIcontext.SHOW_ME_ID,    "Show",       "Show",       "Show object name" )
        a = sgPyQt.createAction( GUIcontext.DELETE_ME_ID,  "Delete",     "Delete",     "Remove object" )
        a = sgPyQt.createAction( GUIcontext.RENAME_ME_ID,  "Rename",     "Rename",     "Rename object" )
        pass
    pass

################################################
# Global variables
################################################

# study-to-context map
__study2context__   = {}
# current context
__current_context__ = None
# object counter
__objectid__ = 0

################################################
       
# Get SALOME PyQt interface
import SalomePyQt
sgPyQt = SalomePyQt.SalomePyQt()

# Get SALOME Swig interface
import libSALOME_Swig
sg = libSALOME_Swig.SALOMEGUI_Swig()

################################################

################################################
# Internal methods
################################################

###
# get active study ID
###
def _getStudyId():
    return sgPyQt.getStudyId()

###
# get active study
###
def _getStudy():
    studyId = _getStudyId()
    study = getStudyManager().GetStudyByID( studyId )
    return study

###
# returns True if object has children
###
def _hasChildren( sobj ):
    if sobj:
        study = _getStudy()
        iter  = study.NewChildIterator( sobj )
        while iter.More():
            name = iter.Value().GetName()
            if name:
                return True
            iter.Next()
            pass
        pass
    return False

###
# get current GUI context
###
def _getContext():
    global __current_context__
    return __current_context__

###
# set and return current GUI context
# study ID is passed as parameter
###
def _setContext( studyID ):
    global __study2context__, __current_context__
    if not __study2context__.has_key(studyID):
        __study2context__[studyID] = GUIcontext()
        pass
    __current_context__ = __study2context__[studyID]
    return __current_context__

###
# increment object counter in the map
###
def _incObjToMap( m, id ):
    if id not in m: m[id] = 0
    m[id] += 1
    pass

###
# analyse selection
###
def _getSelection():
    selcount = sg.SelectedCount()
    seltypes = {}
    for i in range( selcount ):
        _incObjToMap( seltypes, getObjectID( _getStudy(), sg.getSelected( i ) ) )
        pass
    return selcount, seltypes

################################################
# Callback functions
################################################

# called when module is initialized
# perform initialization actions
def initialize():
    if verbose() : print "first_appGUI.initialize() : study : %d" % _getStudyId()
    # set default preferences values
    if not sgPyQt.hasSetting( "first_app", "def_obj_name"):
        sgPyQt.addSetting( "first_app", "def_obj_name", GUIcontext.DEFAULT_NAME )
    if not sgPyQt.hasSetting( "first_app", "creation_mode"):
        sgPyQt.addSetting( "first_app", "creation_mode", 0 )
    if not sgPyQt.hasSetting( "first_app", "Password"):
        sgPyQt.addSetting( "first_app", "Password", GUIcontext.DEFAULT_PASSWD )
    pass

# called when module is initialized
# return map of popup windows to be used by the module
def windows():
    if verbose() : print "first_appGUI.windows() : study : %d" % _getStudyId()
    wm = {}
    wm[SalomePyQt.WT_ObjectBrowser] = Qt.LeftDockWidgetArea
    wm[SalomePyQt.WT_PyConsole]     = Qt.BottomDockWidgetArea
    return wm

# called when module is initialized
# return list of 2d/3d views to be used ny the module
def views():
    if verbose() : print "first_appGUI.views() : study : %d" % _getStudyId()
    return []

# called when module is initialized
# export module's preferences
def createPreferences():
    if verbose() : print "first_appGUI.createPreferences() : study : %d" % _getStudyId()
    gid = sgPyQt.addPreference( "General" )
    gid = sgPyQt.addPreference( "Object creation", gid )
    pid = sgPyQt.addPreference( "Default name",  gid, SalomePyQt.PT_String,   "first_app", "def_obj_name" )
    pid = sgPyQt.addPreference( "Default creation mode", gid, SalomePyQt.PT_Selector, "first_app", "creation_mode" )
    strings = QStringList()
    strings.append( "Default name" )
    strings.append( "Generate name" )
    strings.append( "Ask name" )
    indexes = []
    indexes.append( QVariant(0) )
    indexes.append( QVariant(1) )
    indexes.append( QVariant(2) )
    sgPyQt.setPreferenceProperty( pid, "strings", QVariant( strings ) )
    sgPyQt.setPreferenceProperty( pid, "indexes", QVariant( indexes ) )
    pid = sgPyQt.addPreference( "Password",  gid, SalomePyQt.PT_String,   "first_app", "Password" )
    sgPyQt.setPreferenceProperty( pid, "echo", QVariant( 2 ) )
    pass

# called when module is activated
# returns True if activating is successfull and False otherwise
def activate():
    if verbose() : print "first_appGUI.activate() : study : %d" % _getStudyId()
    ctx = _setContext( _getStudyId() )
    return True

# called when module is deactivated
def deactivate():
    if verbose() : print "first_appGUI.deactivate() : study : %d" % _getStudyId()
    pass

# called when active study is changed
# active study ID is passed as parameter
def activeStudyChanged( studyID ):
    if verbose() : print "first_appGUI.activeStudyChanged(): study : %d" % studyID
    ctx = _setContext( _getStudyId() )
    pass

# called when popup menu is invoked
# popup menu and menu context are passed as parameters
def createPopupMenu( popup, context ):
    if verbose() : print "first_appGUI.createPopupMenu(): context = %s" % context
    ctx = _setContext( _getStudyId() )
    study = _getStudy()
    selcount, selected = _getSelection()
    if verbose() : print selcount, selected
    if selcount == 1:
        # one object is selected
        if moduleID() in selected:
            # menu for component
            popup.addAction( sgPyQt.action( GUIcontext.DELETE_ALL_ID ) )
        elif objectID() in selected:
            # menu for object
            popup.addAction( sgPyQt.action( GUIcontext.SHOW_ME_ID ) )
            popup.addAction( sgPyQt.action( GUIcontext.RENAME_ME_ID ) )
            popup.addSeparator()
            popup.addAction( sgPyQt.action( GUIcontext.DELETE_ME_ID ) )
            pass
        pass
    elif selcount > 1:
        # several objects are selected
        if len( selected ) == 1:
            if moduleID() in selected:
                # menu for component
                popup.addAction( sgPyQt.action( GUIcontext.DELETE_ALL_ID ) )
            elif objectID() in selected:
                # menu for list of objects
                popup.addAction( sgPyQt.action( GUIcontext.DELETE_ME_ID ) )
                pass
            pass
        pass
    pass

# called when GUI action is activated
# action ID is passed as parameter
def OnGUIEvent( commandID ):
    if verbose() : print "first_appGUI.OnGUIEvent(): command = %d" % commandID
    if dict_command.has_key( commandID ):
        try:
            dict_command[commandID]()
        except:
            traceback.print_exc()
    else:
        if verbose() : print "The command is not implemented: %d" % commandID
    pass

# called when module's preferences are changed
# preference's resources section and setting name are passed as parameters
def preferenceChanged( section, setting ):
    if verbose() : print "first_appGUI.preferenceChanged(): %s / %s" % ( section, setting )
    pass

# called when active view is changed
# view ID is passed as parameter
def activeViewChanged( viewID ):
    if verbose() : print "first_appGUI.activeViewChanged(): %d" % viewID
    pass

# called when active view is cloned
# cloned view ID is passed as parameter
def viewCloned( viewID ):
    if verbose() : print "first_appGUI.viewCloned(): %d" % viewID
    pass

# called when active view is viewClosed
# view ID is passed as parameter
def viewClosed( viewID ):
    if verbose() : print "first_appGUI.viewClosed(): %d" % viewID
    pass

# called when study is opened
# returns engine IOR
def engineIOR():
    if verbose() : print "first_appGUI.engineIOR()"
    return getEngineIOR()

# called to check if object can be dragged
# returns True if drag operation is allowed for this object
def isDraggable(what):
    if verbose() : print "first_appGUI.isDraggable()"
    # return True if object is draggable
    return False

# called to check if object allows dropping on it
# returns True if drop operation is allowed for this object
def isDropAccepted(where):
    if verbose() : print "first_appGUI.isDropAccepted()"
    # return True if object accept drops
    return False

# called when drag and drop operation is finished
# performs corresponding data re-arrangement if allowed
def dropObjects(what, where, row, action):
    if verbose() :
        print "first_appGUI.dropObjects()"
        # 'what' is a list of entries of objects being dropped
        for i in what: print "- dropped:", i
        # 'where' is a parent object's entry
        print "- dropping on:", where
        # 'row' is an position in the parent's children list;
        # -1 if appending to the end of children list is performed
        print "- dropping position:", row
        # 'action' is a dropping action being performed:
        # - 0x01 (Qt::CopyAction) for copy
        # - 0x02 (Qt::MoveAction) for move
        print "- drop action:", action
        pass
    pass

################################################
# GUI actions implementation
################################################

###
# 'HELLO' dialog box
###
class MyDialog( QDialog ):
    # constructor
    def __init__( self, parent = None, modal = 0):
        QDialog.__init__( self, parent )
        self.setObjectName( "MyDialog" )
        self.setModal( modal )
        self.setWindowTitle( "HELLO!" )
        vb = QVBoxLayout( self )
        vb.setContentsMargins( 8, 8, 8, 8 )

        hb0 = QHBoxLayout( self )
        label = QLabel( "Prenom: ", self )
        hb0.addWidget( label )
        self.entry = QLineEdit( self )
        self.entry.setMinimumWidth( 200 )
        hb0.addWidget( self.entry )
        vb.addLayout( hb0 )
        
        hb1 = QHBoxLayout( self )
        bOk = QPushButton( "&OK", self )
        bOk.setIcon( sgPyQt.loadIcon( 'first_app', 'ICO_HANDSHAKE' ) )
        bOk.clicked.connect(self.accept)
        hb1.addWidget( bOk )
        
        hb1.addStretch( 10 )
        
        bCancel = QPushButton( "&Cancel", self )
        bCancel.setIcon( sgPyQt.loadIcon( 'first_app', 'ICO_STOP' ) )
        bCancel.clicked.connect(self.close)
        hb1.addWidget( bCancel )
        vb.addLayout( hb1 )
        pass
    
    # OK button slot
    def accept( self ):
        name = str( self.entry.text() )
        if name != "":
            banner = getEngine().makeBanner( name )
            QMessageBox.information( self, 'Info', banner )
            self.close()
        else:
            QMessageBox.warning( self, 'Error!', 'Please, enter the name!' )
        pass

###
# Show 'HELLO' dialog box
###
def ShowHELLO():
    # create dialog box
    d = MyDialog( sgPyQt.getDesktop(), 1 )
    # show dialog box
    d.exec_()
    pass

###
# Create new object
###
def CreateObject():
    global __objectid__
    default_name = str( sgPyQt.stringSetting( "first_app", "def_obj_name", GUIcontext.DEFAULT_NAME ) ).strip()
    try:
        if sgPyQt.action( GUIcontext.OPTION_3_ID ).isChecked():
            # request object name from the user
            name, ok = QInputDialog.getText( sgPyQt.getDesktop(),
                                             "Create Object",
                                             "Enter object name:",
                                             QLineEdit.Normal,
                                             default_name )
            if not ok: return
            name = str( name ).strip()
        elif sgPyQt.action( GUIcontext.OPTION_2_ID ).isChecked():
            # generate object name
            __objectid__  = __objectid__ + 1
            name = "%s %d" % ( default_name, __objectid__ )
        else:
            name = default_name
            pass
        pass
    except:
        # generate object name
        __objectid__  = __objectid__ + 1
        name = "%s %d" % ( default_name, __objectid__ )
        pass
    if not name: return
    getEngine().createObject( _getStudy(), name )
    sg.updateObjBrowser( True )
    pass

###
# Delete all objects
###
def DeleteAll():
    study = _getStudy()
    father = study.FindComponent( moduleName() )
    if father:
        iter = study.NewChildIterator( father )
        builder = study.NewBuilder()
        while iter.More():
            sobj = iter.Value()
            iter.Next()
            builder.RemoveObjectWithChildren( sobj )
            pass
        sg.updateObjBrowser( True )
        pass
    pass

###
# Show object's name
###
def ShowMe():
    study = _getStudy()
    entry = sg.getSelected( 0 )
    if entry != '':
        sobj = study.FindObjectID( entry )
        if ( sobj ):
            test, attr = sobj.FindAttribute( "AttributeName" )
            if test:
                QMessageBox.information( sgPyQt.getDesktop(), 'Info', "My name is '%s'" % attr.Value() )
                pass
            pass
        pass
    pass

###
# Delete selected object(s)
###
def Delete():
    study = _getStudy()
    builder = study.NewBuilder()
    if sg.SelectedCount() <= 0: return
    for i in range( sg.SelectedCount() ):
        entry = sg.getSelected( i )
        if entry != '':
            sobj = study.FindObjectID( entry )
            if ( sobj ):
                builder.RemoveObject( sobj )
                pass
            pass
        pass
    sg.updateObjBrowser( True )
    pass

###
# Rename selected object
###
def Rename():
    study = _getStudy()
    builder = study.NewBuilder()
    entry = sg.getSelected( 0 )
    if entry != '':
        sobj = study.FindObjectID( entry )
        if ( sobj ):
            name, ok = QInputDialog.getText( sgPyQt.getDesktop(),
                                             "Object name",
                                             "Enter object name:",
                                             QLineEdit.Normal,
                                             sobj.GetName() )
            name = str( name ).strip()
            if not ok or not name: return
            attr = builder.FindOrCreateAttribute( sobj, "AttributeName" )
            attr.SetValue( name )
            sg.updateObjBrowser( True )
            pass
        pass
    pass

###
# Display password stored in the preferences
###
def Password():
  passwd = str( sgPyQt.stringSetting( "first_app", "Password", GUIcontext.DEFAULT_PASSWD ) ).strip()
  QMessageBox.information(sgPyQt.getDesktop(),
                          "Password",
                          passwd)

###
# Commands dictionary
###
dict_command = {
    GUIcontext.HELLO_ID         : ShowHELLO,
    GUIcontext.CREATE_OBJECT_ID : CreateObject,
    GUIcontext.DELETE_ALL_ID    : DeleteAll,
    GUIcontext.SHOW_ME_ID       : ShowMe,
    GUIcontext.DELETE_ME_ID     : Delete,
    GUIcontext.RENAME_ME_ID     : Rename,
    GUIcontext.PASSWORD_ID      : Password,
    }
