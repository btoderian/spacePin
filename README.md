SPACE PIN
A Maya 2022 script that allows you to reparent your selection to another object, or the world.  
Adds a new controller object that preserves the existing motion, but realtive to the chosen space. 

HOW TO USE
To parent your objects to worldspace: select nothing, press the yellow '<<' button.  Or type 'world' into the input field. 
To parent your object to another: select the parent, press the yellow '<<' button.
Or you can turn off the contraints, and simply record the information for later use - all transform data is recorded.

LAYERS
Use the optional Anim Layer feature to control the contraint strength with an override anim layer.    
Mute the Space Pin constraint layer to toggle the pin effect off. 
Do not animate the child object directly on the animation layer created by the script - that layer for controlling child constraints only, like a blendparent node.
But you CAN add additonal anim layers to add motion ontop of the pins effect.  
With this feature you can animate the new pin control, or the original control with additional animation layers that you add.  
If the space pin control object is destroyed, the Space Pin Anim layer must also be disabled as well, or the object will not transform.  
Merge the animation layer with the baselayer to bake the pin effect.  The Space Pin obejct will remain, but have no effect on the child object.




INSTALLATION
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
