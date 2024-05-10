##MIT License

##Copyright (c) [2024] [Blaine Toderian]

## WIP Re-write of SpacePin tool
## Allows you to reparent objects via an intermediary object and constraints on animation layers for additional flexibility.

import maya.cmds as cmds
import maya.mel as mel
from sys import exit #spacepin

def spacePin(parent=None, childList=None, ):
    ## make control object for each child
    for Object in childList:
        makeCon = createCon(Object)
 
        ##setting vars
        conName = makeCon[0]
        ##making list to recall later
        offsetList.append ( makeCon[1] )
        grpName = makeCon[2]
 
        ## matching group to parent space object
        cmds.parentConstraint( parent, grpName )
 
        ## matching con to selected object regardless of constraint options
        matchConName = (cmds.parentConstraint( Object, conName))    #split to two cons
        bakeList.append (conName)
        bakeListConstraints.append (matchConName)
        ##scale for beast wars
        bakeListConstraints.append(cmds.scaleConstraint(Object, conName, maintainOffset=True))

    ## time range for bake
    time = getVisTimeRange()

    ##baking pin controls                                                                 
    cmds.bakeResults( bakeList, t=(time[0],time[1]), simulation=True, sampleBy = 1, minimizeRotation=True, at=("tx","ty","tz","rx","ry","rz","sx","sy","sz"))

    ##delete match constraints
    for mCon in bakeListConstraints:
        cmds.delete(mCon)


        

def spGetInputWrapper():
    ##checking if space object is in selection, throw warning if so
    if (cmds.textField( "spaceInput",q=True, tx=True)) in selectedObjects:
        cmds.headsUpMessage( "Parent Space Object Selected, Cannot Parent Selection to Self!", time = 0.1 )
        exit("Can't parent the object to itself, please pick a new object.")   #exit without traceback? 
 
    ## if nothing is selected
    if not selectedObjects:
        cmds.headsUpMessage( "NO SELECTION!", time = 1 )
        exit("NO SELECTION!")  #exit without traceback? 


def spInputButtonText(*args):
    inputText = cmds.ls(sl=True)
    if inputText:
        cmds.textField( "spaceInput", e=True, tx= inputText[0])
    else:
        cmds.textField( "spaceInput", e=True, tx="world")
 
## space pin interface Toggles
#def spEnableDisable(fieldName="layerName"):
#    newValue = not(cmds.textField( fieldName, q=True, en=True ))
#    cmds.textField( fieldName, e=True, en=bool(newValue) )
 
def spEnableDisable(fieldName="layerName"):
    fieldName="layerName"
    currentStatus = cmds.textField(fieldName, q=True, en=True)
    newValue = bool(0 if currentStatus else 1)
    cmds.textField(fieldName, e=True, en=newValue)

## space pin main
def sPinExecute(*args):
    cmds.headsUpMessage( "Reparenting...", time = 0 )
 
    ##  check for selection, prompt
    selectedObjects = cmds.ls(sl=True)
    bakeList = []
    bakeListConstraints = []
    offsetList = []
 
    ##checking if space object is in selection, throw warning if so
    if (cmds.textField( "spaceInput",q=True, tx=True)) in selectedObjects:
        cmds.headsUpMessage( "Parent Space Object Selected, Cannot Parent Selection to Self!", time = 0.1 )
        exit("Can't parent the object to itself, please pick a new object.")   #exit without traceback? 
 
    ## if nothing is selected
    if not selectedObjects:
        cmds.headsUpMessage( "NO SELECTION!", time = 1 )
        exit("NO SELECTION!")  #exit without traceback? 
 
    ## make cons
    for Object in selectedObjects:
        makeCon = createCon(Object)
 
        ##setting vars
        conName = makeCon[0]
        ##making list to recall later
        offsetList.append ( makeCon[1] )
        grpName = makeCon[2]
 
        ## matching group to parent space text option
        if (cmds.textField( "spaceInput",q=True, tx=True)) != "world":
            cmds.parentConstraint( (cmds.textField( "spaceInput",q=True, tx=True)), grpName )
 
        ## matching con to selected object regardless of constraint options
        matchConName = (cmds.parentConstraint( Object, conName))    #split to two cons
        bakeList.append (conName)
        bakeListConstraints.append (matchConName)
        ##scale for beast wars
        bakeListConstraints.append(cmds.scaleConstraint(Object, conName, maintainOffset=True))
 
    ## time range for bake
    time = getVisTimeRange()

    ##baking pin controls                                                                 
    cmds.bakeResults( bakeList, t=(time[0],time[1]), simulation=True, sampleBy = 1, minimizeRotation=True, at=("tx","ty","tz","rx","ry","rz","sx","sy","sz"))

    ##delete match constraints
    for mCon in bakeListConstraints:
        cmds.delete(mCon)
 
    ##setting up counter to syncronize list indices
    itemIndex = []
    counter = 0
    for numItems in selectedObjects:
        itemIndex.append (counter)
        counter = (counter + 1)
 
    ##make layer if using
    if (cmds.checkBox("viaAnimLayer", q=True, v=True)):
        nameString = cmds.textField( "layerName", q=True, tx=True)
        if nameString:
            #removeSpaces
            layerName = nameString.replace(" ", "")
            #check if it already exists
            if cmds.animLayer(layerName, q=True, exists=True):
                animLayerName = layerName
            else:
                animLayerName = makeAnimLayer(layerName=layerName, overrideMode=True)
        else:
            animLayerName = makeAnimLayer(layerName="pin_OR", overrideMode=True)

    ##setting separate constraints (in case one fails) from pin to rig if enabled and checks clear
    for item in itemIndex:
        ## anim layer version
        if (cmds.checkBox("viaAnimLayer", q=True, v=True)):
            #check if supposed to, and if each attr if free
            if ((cmds.checkBox("transMatch", q=True, v=True)) and (cmds.getAttr((selectedObjects[item] + ".ty"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".tx"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".tz"), keyable=True ))):   
                tConName = (cmds.pointConstraint(offsetList[item], selectedObjects[item], mo=True, layer=animLayerName))[0]
            if ((cmds.checkBox("rotMatch", q=True, v=True)) and (cmds.getAttr((selectedObjects[item] + ".ry"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".rx"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".rz"), keyable=True ))):   
                rConName = (cmds.orientConstraint( offsetList[item], selectedObjects[item],mo=True, layer=animLayerName))[0]
            if ((cmds.checkBox("scaleMatch", q=True, v=True))):
                #for beast wars, disconnect scale attrs to make constraint
                #cmds.cutKey(selectedObjects[item], cl=True, at=("sx","sy","sz"))  #not necessary for layers? 
                if ((cmds.getAttr((selectedObjects[item] + ".sy"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".sx"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".sz"), keyable=True ))):   
                    sConName = (cmds.scaleConstraint( offsetList[item], selectedObjects[item],mo=True, layer=animLayerName))[0]

        ## non-animation layer version
        else:
            #check if supposed to, and if each attr if free
            if ((cmds.checkBox("transMatch", q=True, v=True)) and (cmds.getAttr((selectedObjects[item] + ".ty"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".tx"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".tz"), keyable=True ))):   
                tConName = (cmds.pointConstraint(offsetList[item], selectedObjects[item]))[0]
            if ((cmds.checkBox("rotMatch", q=True, v=True)) and (cmds.getAttr((selectedObjects[item] + ".ry"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".rx"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".rz"), keyable=True ))):   
                rConName = (cmds.orientConstraint( offsetList[item], selectedObjects[item]))[0]
            if ((cmds.checkBox("scaleMatch", q=True, v=True))):
                #for beast wars, disconnect scale attrs to make constraint
                cmds.cutKey(selectedObjects[item], cl=True, at=("sx","sy","sz"))
                if ((cmds.getAttr((selectedObjects[item] + ".sy"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".sx"), keyable=True )) and (cmds.getAttr((selectedObjects[item] + ".sz"), keyable=True ))):   
                    sConName = (cmds.scaleConstraint( offsetList[item], selectedObjects[item]))[0]

        ##fix
        ## do for each constraint
    
        ##need to check for incoming.... then duplicate that?
        #cmds.connectAttr(selectedObjects[item] + '.parentInverseMatrix[0]', tConName + '.constraintParentInverseMatrix')
        #cmds.connectAttr(selectedObjects[item] + '.rotatePivot', tConName + '.constraintRotatePivot')
        #cmds.connectAttr(selectedObjects[item] + '.rotatePivotTranslate', tConName + '.constraintRotateTranslate')
        #cmds.setAttr(tConName + '.offset', 0, 0, 0)
 
    ##messages
    #cmds.refresh()
    cmds.headsUpMessage( "Reparenting Complete", time = 1 )


## get visible time range
def getVisTimeRange():
    time = []
    ## use selected range first or goto visible range second
    timeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    if (cmds.timeControl(timeSlider, q=True, rv=True)):
        selRange = cmds.timeControl(timeSlider, q=True, rng=True)
        time.append (selRange.split ( ":" ) [0])
        time.append (selRange.split ( ":" ) [1])
    if not (cmds.timeControl(timeSlider, q=True, rv=True)):
        time.append ( cmds.playbackOptions( q=True, min=True ))
        time.append ( cmds.playbackOptions( q=True, max=True ))
    return time


## space pin control stack
def createCon(ObjectName):
    ## rotation order rosetta stone to maya equivilent
    rOrder = []
    rOrderCase = (cmds.optionMenu ( "rOrderMenu", sl=True, q = True ))
    if rOrderCase == 1:
        rOrder = 2
    if rOrderCase == 2:
        rOrder = 1
    if rOrderCase == 3:
        rOrder = 0
    if rOrderCase == 4:
        rOrder = 3
    if rOrderCase == 5:
        rOrder = 5
    if rOrderCase == 6:
        rOrder = 4
 
    ## make the controls and name them, parent them
    #Object = ObjectName.split(":")[-1]    #strips off namespaces
    Object = ObjectName.replace(":", "_")    #keeps namespace but adds underscore for readability
    conNewName = (cmds.circle( radius=8, name=("pin_" + Object)))
    offsetNewName = (cmds.circle( radius=9, name=("pinOffset_" + Object)))
    grpName = (cmds.group( empty=True, name=("pin_space+" + Object)))
    conName = cmds.parent(conNewName[0], grpName)[0]
    offsetTempName = cmds.parent(offsetNewName[0], conName)[0]
    offsetName = cmds.ls(offsetTempName, l=True)[0]
 
    ## set common attrs                                                    ##add attrs for colour?
    customList = []
    customList.append(offsetName)
    customList.append(conName)
    
    for custom in customList:
        cmds.setAttr((custom + ".rotateOrder"), rOrder)
        cmds.setAttr((custom + ".overrideEnabled"), 1)
        #disabled hiding of scale for beast wars
        #cmds.setAttr((custom + ".scaleX"), keyable=False)
        #cmds.setAttr((custom + ".scaleY"), keyable=False)
        #cmds.setAttr((custom + ".scaleZ"), keyable=False)
        cmds.addAttr(custom, longName="controlSize", niceName = "Control Size", attributeType="float", defaultValue = 8, keyable=False)
        cmds.setAttr((custom + ".controlSize"), channelBox=True)
 
        ##set up radius control to makeNurbCircle node
        customConnections = cmds.listConnections((cmds.listRelatives(custom, shapes=True, f=True))) 
        for connected in customConnections:
            if "makeNurbCircle" in connected:
                cmds.connectAttr((custom + ".controlSize"),(connected + ".radius"))
 
    ##individual attrs
    cmds.setAttr((conName + ".overrideColor"), 21)
    cmds.setAttr((conName + ".visibility"), keyable=False, channelBox=True)
    cmds.setAttr((offsetName + ".overrideColor"), 20)
    cmds.setAttr((offsetName + ".visibility"), keyable=False)
    cmds.setAttr((offsetName + ".controlSize"), 8 )
 
    ##connect offset vis to pin attr
    cmds.addAttr(conName, longName="offsetConVis", niceName="Offset Visibility", attributeType="bool", keyable=False, dv=0)
    cmds.setAttr((conName + ".offsetConVis"), channelBox = True)
    cmds.connectAttr((conName + ".offsetConVis"),(offsetName + ".visibility"))
 
    return conName, offsetName, grpName

##  anim layers
def makeAnimLayer(layerName="animLayer",overrideMode=True):
    animLayerName = (cmds.animLayer(layerName, override=overrideMode))
    cmds.setAttr( (animLayerName + ".rotationAccumulationMode"), 1)
    return animLayerName

## spacePin interface - run this module!
def UI():
    if cmds.window("spacePin", exists=True):
        cmds.deleteUI("spacePin", window=True)
    if cmds.windowPref("spacePin", exists=True):
        cmds.windowPref("spacePin", remove=True)
    cmds.window("spacePin",title="Parent Space Switcher", widthHeight=[400,150] )    
    
    cmds.columnLayout("mainLayout")
    
    cmds.rowColumnLayout( numberOfRows=1 )
    cmds.text( "Parent Space Object:" )
    cmds.textField( "spaceInput", tx="world", w=230 )
    cmds.button( "getSpaceInput", label="<<",w=60, bgc=[0.5,0.5,0], command = spInputButtonText )    
    cmds.setParent("mainLayout")

    cmds.separator(height=10)
    cmds.rowColumnLayout( numberOfRows=1 )
    cmds.text( "Constrain:     " )
    cmds.checkBox("transMatch", label="Translations    ",v=True)
    cmds.checkBox("rotMatch", label="Rotations    ",v=True)
    cmds.checkBox("scaleMatch", label="Scales   ",v=False)
    
    cmds.optionMenu( "rOrderMenu", label='Order:')
    cmds.menuItem( label='ZXY' )
    cmds.menuItem( label='YZX' )
    cmds.menuItem( label='XYZ' )
    cmds.menuItem( label='XZY' )
    cmds.menuItem( label='ZYX' )
    cmds.menuItem( label='YXZ' )    
    
    cmds.setParent("mainLayout")
    
    cmds.separator(height=10)
 
    cmds.rowColumnLayout( numberOfRows=1 )
    cmds.checkBox("viaAnimLayer", label="via Anim Layer                                    ", cc=spEnableDisable, en=True)
    cmds.textField( "layerName", pht="Optional Layer Name", w=245, en=False )
 
    cmds.setParent("mainLayout")
    
    cmds.separator(height=10)
 
    cmds.button( label="Re-Parent Selected Objects", w=400, h=50, command=sPinExecute )
 
    cmds.showWindow()
