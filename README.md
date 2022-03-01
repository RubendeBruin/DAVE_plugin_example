# Extending DAVE

When adding (proprietary) elements to DAVE you may want to extend the GUI without
changing the source-code of DAVE itself.

Add:
- workspaces
- dockwidgets
- nodes

## New Node types



### Registering

#### Registering the class

DAVE executes python code when importing files, copying the scene or adding nodes.

New classes need to be made available to the environment when running code in order to be usable.

This is done by adding them to a global setting `DAVE_ADDITIONAL_RUNTIME_MODULES`:
```python
# Add the balloon class to the modules that are available when executing code

from DAVE.settings import DAVE_ADDITIONAL_RUNTIME_MODULES
DAVE_ADDITIONAL_RUNTIME_MODULES['Balloon'] = Balloon
```

#### Registering the properties and documentation

The properties of the and their documentation need to be added to DAVE as well. This makes them available for timelines, limits derived-properties, reporting and others.

The properties are registered in the following nested dictionary:

```python
from DAVE.settings import DAVE_NODEPROP_INFO,NodePropertyInfo

# type is the node-type, for example Point
# property-name is the name of the property, for example 'global_position'
info = DAVE_NODEPROP_INFO[type][property_name]

# info is a NodePropertyInfo object
```

The properties of nodes are used in various places in the guis and reporting:

- The limits screen to define limits for single numerical properties

  - Properties with a single numerical value

- The derived properties screen - to show the values of derived properties

  - Anything interesting, typically numerical and boolean values and sequences of those
    - type = float, bool

- Reporting module

  - All properties that have a physical meaning and/or define how the model is structured (parent, meshes, etc)

- Timeline module

  - All settable single properties, including nodes and booleans
    - type = float/bool/node
    - settable = True

- Exploration module

  - All settable single numerical properties 

  

Besides that we need to have the following documentation available for each node/property combination:

- short description (1 line)

- long description

- unit, eg [m]

- remarks, eg (global) or (parent)

  Here the property may be inherited and/or overridden.

- settable: not read-only

- single-settable: can be used in time-line - bool, Node, 

- single-numeric: can be used as limit



| Class | Property      | Short doc      | Long doc      | Unit       | Remarks  | type          | settable | single-settable | single-numeric |
| ----- | ------------- | -------------- | ------------- | ---------- | -------- | ------------- | -------- | --------------- | -------------- |
| Point | x             | x-position     | x-position... | [m]        | (parent) | float         | X        | X               | X              |
| Point | parent        | parent         | parent...     |            | (Node)   | Frame         | X        | X               |                |
| Node  | name          | name           | name...       |            | (unique) | str           | X        |                 |                |
| Point | position      | position       | position...   | [m,m,m]    | (parent) | float         | X        |                 |                |
| Point | applied_force | force          | force ...     | [kN,kN,kN] | (parent) | float         |          |                 | X              |
| Point | force         | \|force\|      | force ...     | [kN]       |          | float         |          |                 | X              |
| Frame | fixed_x       |                |               |            |          | bool          | X        | X               |                |
| Frame | fixed         |                |               |            |          | bool          | X        |                 |                |
| Node  | visible       | visible in GUI |               |            |          | bool          | X        | X               |                |
| Cable | connections   |                |               |            |          | Point\|Circle | X        |                 |                |

##### How, where and when

When looking up the properties this will be done using a Node object and optionally a property name (these two are therefore the index of the database). Matching class needs to be done on an is-instance basis and considering overriding. 

Say:

```
class A has property p
class B derives from A and overrides property p
class C derives from B
```

***How***

requesting the documentation for property p on a node of class C should give the documentation of p of class B. This can be done using the mro. The property of the class with the lowest index in the mro of the node class is the one we want.

The logical way to store is as a nested dictionary:

`data[class][propname(str)] = node_property_info`

with NodePropertyInfo a dataclass

***Where and when***

To store the data with the class as key, the class needs to be defined. So this info can only be created after definition of the classes.

It makes sense to read the data from a .csv or pickle file, but those can not store classes. This means resolving the class from the class name which is easy enough via either globals() or, even better, the DAVE_ADDITIONAL_RUNTIME_MODULES dict.











## Creating a new dock

Docks are floating or docked sub-windows of the main GUI. Everything except the 3d view-port and the menu is a dock.

Docks are QtWidgets derived from `guiDockWidget` 

Docks are created and activated by main. Upon creation they receive some references to things in the gui:

```python
d.guiScene = self.scene
d.guiEmitEvent = self.guiEmitEvent
d.guiRunCodeCallback = self.run_code
d.guiSelectNode = self.guiSelectNode
d.guiSelection = self.selected_nodes
d.guiPressSolveButton = self.solve_statics
d.gui = self
```

Communication between the docks is done via the `guiEmitEvent` which can send any of the ENUMs defined in `guiEventType`. Handling of these events is to be implemented in guiProcessEvent.

#### Registering

Any dock needs to be added to the `DAVE_GUI_DOCKS` dictionary.  The keys in this dictionary are strings. These strings are also used as the dock-window title.

```python
from DAVE.gui.dockwidget import DAVE_GUI_DOCKS
DAVE_GUI_DOCKS['Balloon'] = BalloonDock
```

#### Activating a dock

See workspaces



## Integrating into the main gui

Code can be executed at various moment by defining plugin-functions and adding a reference to that function to a globally available list.

### Init

plugin_init is executed at the end of the .__init__ function.
It takes a single parameter being the instance of the Gui that is being intialized (
the `self` of the init function)

```python
def my_function(gui):
	print('executed on startup')

from DAVE.gui.main import DAVE_GUI_PLUGINS_INIT
DAVE_GUI_PLUGINS_INIT.append(my_function)
```




### Workspaces

The user can activate a workspace by pressing one of the buttons at the top side of the interface. Internally a workspace is identified by an WORKSPACE_ID which is a unique, upper-case string.

#### Adding a button

Adding a button can be done by adding (or inserting) an entry to the DAVE_GUI_WORKSPACE_BUTTONS list. This is a tuple where the first entry is the text on the button and the second entry is the workspace id

```PYTHON
from DAVE.gui.main import DAVE_GUI_WORKSPACE_BUTTONS
DAVE_GUI_WORKSPACE_BUTTONS.append(('BaLLoooon !', 'BALLOON'))

```

![image-20220203142649314](image-20220203142649314.png)

#### Activating the workspace

Workspaces are controlled by the "activate_workspace" function. This function typically creates one of more dockwidgets.

A plugin can be registered in `DAVE_GUI_PLUGINS_WORKSPACE`

```python
def my_plugin_activate_workspace(gui, workspacename):
    print('calling activateworkspace')
    if workspacename.upper() == 'BALLOON': 
        gui.close_all_open_docks() # close all other docks (optional)
        gui.show_guiWidget('Balloon')  # <-- ID of the balloon dock
        
    if worspacename.upper() == 'CONSTRUCT':   # <--- you can also act on activation of other docks
        gui.show_guiWidget('Balloon')  # <-- ID of the balloon dock
        
from DAVE.gui.main import DAVE_GUI_PLUGINS_WORKSPACE
DAVE_GUI_PLUGINS_WORKSPACE.append(my_plugin_activate_workspace)
```



### Context-menu

The context-menu is the right-click menu. This is used to add nodes. A plugin here has the following signature:

```
openContextMenyAt(menu, node_name, gui)
```

the plugin gets called with the following arguments:

1. QMenu object
2. The name of the first selected node (if any)
3. A reference to the main gui

the reference to the main gui can be used to run code as follows:
```python
def plugin_context(menu, node_name,gui):
    code = 'Balloon(s, s.available_name_like("new_balloon"))'
    def action():
        gui.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

    BalloonIcon = QIcon(str(Path(__file__).parent / 'balloon.png'))

    action = menu.addAction("Add balloon", action)
    action.setIcon(BalloonIcon)
```

The plugin needs to be registered in:

```python
from DAVE.gui.main import DAVE_GUI_PLUGINS_CONTEXT
DAVE_GUI_PLUGINS_CONTEXT.append(plugin_context)
```



## Editing nodes

Selecting a node while in "construction" makes the "Properties" dock-widget visible.


### Extending the node-editor

Sections in the node-propeties widget derive from `NodeEditor`

1. Create a new `MyNewNodeEditor` class which derives from `NodeEditor`
2. Register the node-editor class against the node-instances for which the editor should open.

```python
from DAVE.gui.widget_nodeprops import DAVE_GUI_NODE_EDITORS
DAVE_GUI_NODE_EDITORS[Balloon] = BalloonNodeEditor

# Note: Balloon is the Node-Class, BalloonNodeEditor is the editor class
```

![image-20220203143548291](image-20220203143548291.png)

### Alternatively

Create a new dock that reacts to the "SELECTION_CHANGED" event.



