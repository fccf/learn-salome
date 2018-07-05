
import salome
import SMESH
from salome.smesh import smeshBuilder
import os

def export_mesh(mesh,dirname='mesh'):

    if not os.path.exists(dirname):
        os.makedirs(dirname)
    try:
        fileHeader   = open(dirname + "/mesh.header",'w')
        fileNodes    = open(dirname + "/mesh.nodes",'w')
        fileNames    = open(dirname + "/mesh.names",'w')
        fileElements = open(dirname + "/mesh.elements",'w')
        fileBoundary = open(dirname + "/mesh.boundary",'w')
    except Exception:
        print "ERROR: Cannot open files for writting"
        return

    meshIs3D = False
    if mesh.NbVolumes()>0:
        meshIs3D = True

    # mesh.header
    if meshIs3D:
        print "Exporting 3D mesh..\n"
        fileHeader.write("%d %d %d\n" \
            %(mesh.NbNodes(),mesh.NbVolumes(),mesh.NbEdges()+mesh.NbFaces()))
    else:
        print "Exporting 2D mesh..\n"
        fileHeader.write("%d %d %d\n" \
            %(mesh.NbNodes(),mesh.NbFaces(),mesh.NbEdges()))

    elems = {str(k): v for k, v in mesh.GetMeshInfo().items() if v}
    fileHeader.write("%d\n" %(len(elems.values())-1))

    elemTypeNames = {'202': 'Entity_Edge', '303': 'Entity_Triangle', \
                     '404': 'Entity_Quadrangle', '504': 'Entity_Tetra', \
                     '605': 'Entity_Pyramid', '706': 'Entity_Penta', \
                     '808': 'Entity_Hexa'}

    for nbr, ele in sorted(elemTypeNames.items()):
        if elems.get(ele):
            fileHeader.write("%s %d\n" %(nbr,elems.get(ele)))

    fileHeader.flush()
    fileHeader.close()

    # mesh.nodes
    points=mesh.GetElementsByType(SMESH.NODE)
    for ni in points:
        pos=mesh.GetNodeXYZ(ni)
        fileNodes.write("%d -1 %.12g %.12g %.12g\n" %(ni,pos[0],pos[1],pos[2]))
    fileNodes.flush()
    fileNodes.close()

    # initialize arrays
    invElemType = {v: k for k, v in elemTypeNames.items()}
    invElemIDs = [mesh.NbGroups()+1 for el in range(mesh.NbElements())]
    elemGrp = list(invElemIDs)

    edgeIDs = mesh.GetElementsByType(SMESH.EDGE)
    faceIDs = mesh.GetElementsByType(SMESH.FACE)
    elemIDs = edgeIDs + faceIDs
    NbBoundaryElems = mesh.NbEdges()

    if meshIs3D:
        volumeIDs = mesh.GetElementsByType(SMESH.VOLUME)
        elemIDs = elemIDs + volumeIDs
        NbBoundaryElems = NbBoundaryElems + mesh.NbFaces()

    if len(elemGrp) != max(elemIDs):
        raise Exception("ERROR: the number of elements does not match!")

    for el in range(mesh.NbElements()):
        invElemIDs[elemIDs[el]-1] = el+1

    # mesh.names
    fileNames.write("! ----- names for bodies -----\n")
    groupID = 1

    if meshIs3D:
        bodyType = SMESH.VOLUME
        boundaryType = SMESH.FACE
    else:
        bodyType = SMESH.FACE
        boundaryType = SMESH.EDGE

    for grp in mesh.GetGroups(bodyType):
        fileNames.write("$ %s = %d\n" %(grp.GetName(), groupID))
        for el in grp.GetIDs():
            elemGrp[invElemIDs[el-1]-1] = groupID
        groupID = groupID + 1

    fileNames.write("! ----- names for boundaries -----\n")

    for grp in mesh.GetGroups(boundaryType):
        fileNames.write("$ %s = %d\n" %(grp.GetName(), groupID))
        for el in grp.GetIDs():
            if elemGrp[invElemIDs[el-1]-1] > groupID:
                elemGrp[invElemIDs[el-1]-1] = groupID
        groupID = groupID + 1

    fileNames.write("$ empty = %d\n" %(mesh.NbGroups()+1))

    fileNames.flush()
    fileNames.close()

    # mesh.elements
    for el in mesh.GetElementsByType(bodyType):
        elemType = mesh.GetElementGeomType(el)
        elemTypeNbr = int(invElemType.get(str(elemType)))
        fileElements.write("%d %d %d" %(invElemIDs[el-1]-NbBoundaryElems, \
                                        elemGrp[invElemIDs[el-1]-1],elemTypeNbr))
        for nid in mesh.GetElemNodes(el):
            fileElements.write(" %d" %(nid))
        fileElements.write("\n")

    fileElements.flush()
    fileElements.close()

    # mesh.boundary
    for el in elemIDs[:NbBoundaryElems]:
        elemType = mesh.GetElementGeomType(el)
        elemTypeNbr = int(invElemType.get(str(elemType)))

        x,y,z = mesh.BaryCenter( el )
        parents = mesh.FindElementsByPoint( x,y,z, bodyType )

        if len(parents) is 2 and elemTypeNbr is not 202:
            fileBoundary.write("%d %d %d %d %d" \
                %(invElemIDs[el-1],elemGrp[invElemIDs[el-1]-1], \
                  invElemIDs[parents[0]-1]-NbBoundaryElems, \
                  invElemIDs[parents[1]-1]-NbBoundaryElems,elemTypeNbr))
        else:
            fileBoundary.write("%d %d %d 0 %d" \
                %(invElemIDs[el-1],elemGrp[invElemIDs[el-1]-1], \
                  invElemIDs[parents[0]-1]-NbBoundaryElems,elemTypeNbr))

        for nid in mesh.GetElemNodes(el):
            fileBoundary.write(" %d" %(nid))
        fileBoundary.write("\n")

    fileBoundary.flush()
    fileBoundary.close()

    print "Done exporting!\n"

def findSelectedMeshes():
    meshes=list()
    smesh = smeshBuilder.New(salome.myStudy)
    nrSelected=salome.sg.SelectedCount() # total number of selected items

    foundMesh=False
    for i in range(nrSelected):
        selected=salome.sg.getSelected(i)
        selobjID=salome.myStudy.FindObjectID(selected)
        selobj=selobjID.GetObject()
        if selobj.__class__ == SMESH._objref_SMESH_Mesh or \
                selobj.__class__ == salome.smesh.smeshBuilder.meshProxy :
            mName=selobjID.GetName().replace(" ","_")
            foundMesh=True
            mesh=smesh.Mesh(selobj)
            meshes.append(mesh)

    if not foundMesh:
        print "ERROR: Mesh is not selected"
        return list()
    else:
        return meshes


def export():
    u"""
    Export selected meshes
    """
    meshes=findSelectedMeshes()
    for mesh in meshes:
        if not mesh == None:
            mName=mesh.GetName()
            outdir=os.path.dirname(salome.myStudy._get_URL())+os.path.sep+mName
            print "Exporting mesh to " + outdir + "\n"
            export_mesh(mesh,outdir)
