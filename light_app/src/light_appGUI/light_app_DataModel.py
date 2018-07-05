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

#  Author : Roman NIKOLAEV Open CASCADE S.A.S. (roman.nikolaev@opencascade.com)
#  Date   : 13/04/2009
#
import SalomePyQt
from qtsalome import *

# Get SALOME PyQt interface
sgPyQt=SalomePyQt.SalomePyQt()

def processText(text):
    '''
    Remove "\n" sumbol from end of line
    '''
    processed = str(text)
    if processed[len(processed)-1:] == "\n":
        processed = processed[:len(processed)-1]
        
    return processed

class light_app_DataModel:
    '''
    Data model of light_app module
    '''
    def __init__(self):
        '''
        Constructor of light_app_DataModel class.
        '''
        self.myObjects = []
        pass
    
    def getParagraphs(self):
        '''
        Return the list of all paragraph entries.
        '''
        return sgPyQt.getChildren()

    def getObject(self,entry):
        '''
        Return light_app_DataObject by its entry.
        '''
        for obj in self.myObjects:
            if obj.getEntry() == entry:
                return obj
        return None
              
    def createObject(self, text="\n", parent=None):
        '''
        Create light_app_DataObject (Paragraph or Line).
        '''
        obj = light_app_DataObject(text,parent)
        self.myObjects.append(obj)
        return obj.getEntry()
        pass

    def removeObjects(self,lines):
        '''
        Remove objects by its entries
        '''
        for ln in lines:
            sgPyQt.removeObject(ln)
            self.myObjects.remove(self.getObject(ln))
            pass
        pass

    def loadFile(self,filename):
        '''
        Read text file and publish it.
        '''
        with open(str(filename), "r") as aFile:
            lines = aFile.readlines()
            if(lines[0] != "\n"):
                paragr = self.createObject()
            for line in lines:
                if line == "\n":
                    paragr = self.createObject()

                else:
                    self.createObject(processText(line), paragr)
                    pass
                pass
            pass
        pass
    
    def saveFile(self, filename):
        with open(str(filename), "w") as aFile:
            paragrs = self.getParagraphs()
            for paragr in paragrs:
                aFile.write("\n")
                lines = sgPyQt.getChildren(paragr)
                for line in lines:
                    aFile.write(str(sgPyQt.getName(line)) + "\n")
                    pass
                pass
            pass
        pass
    pass

class light_app_DataObject:
    '''
    Data Object of light_app module
    '''
    def __init__(self,text,parent):
        '''
        Constructor of light_app_DataObject class
        '''
        if(parent == None):
            entry = sgPyQt.createObject("Paragraph",
                                        "",
                                        "Paragraph object")
            sgPyQt.setIcon(entry,"light_app_PARAGR_ICON")
        else:
            entry = sgPyQt.createObject(processText(text),
                                        "light_app_LINE_ICON",
                                        "Line object",
                                        parent)
            pass
        self.entry = entry
        self.text = text
        pass
    
    def getEntry(self):
        '''
        Return entry of object 
        '''
        return self.entry
        pass

    def setText(self,text):
        '''
        Set text string
        '''
        self.text = text
        if(text != ""):
            sgPyQt.setName(self.entry,text)
        pass

    def getText(self):
        '''
        Return text string
        '''
        return self.text
    
    pass
