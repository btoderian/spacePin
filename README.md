# spacePin

A Maya 2022 script that allows you to reparent your selection to a new parent by adding a new controller shape that  preserves the motion.  Works with simple constraints and or animation layers for increased flexibility. 

Drop the spacePin.py file into your maya scripts folder.  

Refresh Maya or your code cache with this python code:

```
#rehash command
import maya.mel as mel
mel.eval('rehash;')
```

Run the script with this python code:

```
#spacePin
import spacePin
spacePin.UI()
```
