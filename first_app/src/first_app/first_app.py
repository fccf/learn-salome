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
import first_app_ORB__POA
import SALOME_ComponentPy
import SALOME_DriverPy
import SALOMEDS

from first_app_utils import *

class first_app(first_app_ORB__POA.first_app_Gen,
              SALOME_ComponentPy.SALOME_ComponentPy_i,
              SALOME_DriverPy.SALOME_DriverPy_i):
    """
    Construct an instance of first_app module engine.
    The class first_app implements CORBA interface first_app_Gen (see first_app_Gen.idl).
    It is inherited from the classes SALOME_ComponentPy_i (implementation of
    Engines::EngineComponent CORBA interface - SALOME component) and SALOME_DriverPy_i
    (implementation of SALOMEDS::Driver CORBA interface - SALOME module's engine).
    """
    def __init__ ( self, orb, poa, contID, containerName, instanceName,
                   interfaceName ):
        SALOME_ComponentPy.SALOME_ComponentPy_i.__init__(self, orb, poa,
                    contID, containerName, instanceName, interfaceName, False)
        SALOME_DriverPy.SALOME_DriverPy_i.__init__(self, interfaceName)
        #
        self._naming_service = SALOME_ComponentPy.SALOME_NamingServicePy_i( self._orb )
        #
        pass

    """
    Get version information.
    """
    def getVersion( self ):
        import salome_version
        return salome_version.getVersion("first_app", True)

    """
    Generate hello banner.
    """
    def makeBanner( self, name ):
        banner = "Hello %s!" % name
        return banner

    """
    Intentionnally raises an exception for test purposes.
    """
    def raiseAnException( self ):
        import SALOME
        exData = SALOME.ExceptionStruct( SALOME.BAD_PARAM, "Test exception in raiseAnException()",'',0)
        raise SALOME.SALOME_Exception( exData )

    """
    Create object.
    """
    def createObject( self, study, name ):
        builder = study.NewBuilder()
        father  = findOrCreateComponent( study )
        object  = builder.NewObject( father )
        attr    = builder.FindOrCreateAttribute( object, "AttributeName" )
        attr.SetValue( name )
        attr    = builder.FindOrCreateAttribute( object, "AttributeLocalID" )
        attr.SetValue( objectID() )
        pass

    """
    Dump module data to the Python script.
    """
    def DumpPython( self, study, isPublished, isMultiFile ):
        abuffer = []
        names = []
        father = study.FindComponent( moduleName() )
        if father:
            iter = study.NewChildIterator( father )
            while iter.More():
                name = iter.Value().GetName()
                if name: names.append( name )
                iter.Next()
                pass
            pass
        if names:
            abuffer += [ "from salome import lcc" ]
            abuffer += [ "import first_app_ORB" ]
            abuffer += [ "" ]
            abuffer += [ "first_app = lcc.FindOrLoadComponent( 'FactoryServerPy', '%s' )" % moduleName() ]
            abuffer += [ "" ]
            abuffer += [ "first_app.createObject( theStudy, '%s' )" % name for name in names ]
            abuffer += [ "" ]
            pass
        if isMultiFile:
            abuffer       = [ "  " + s for s in abuffer ]
            abuffer[0:0]  = [ "def RebuildData( theStudy ):" ]
            abuffer      += [ "  pass" ]
        abuffer += [ "\0" ]
        return ("\n".join( abuffer ), 1)
