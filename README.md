# DAVE_plugin_example

# Expanding the GUI / Plugins

When adding (proprietary) elements to DAVE you may want to extend the GUI without
changing the source-code of DAVE itself.

Add:
- workspaces
- dockwidgets
- nodes


## Making new node-types available when running code

DAVE executes python code when importing files, copying the scene or adding nodes.

New classes need to be made availalbe to the environment when running code in order to be usable.

This is done by adding them to a global setting `DAVE_ADDITIONAL_RUNTIME_MODULES`:
```python
# Add the balloon class to the modules that are available when executing code

from DAVE.settings import DAVE_ADDITIONAL_RUNTIME_MODULES
DAVE_ADDITIONAL_RUNTIME_MODULES['Balloon'] = Balloon
```

## Adding stuff to the main gui

plugin_init is executed at the end of the .__init__ function.
It takes a single parameter being the instance of the Gui that is being intialized (
the `self` of the init function)


## Workspaces

Workspaces are controlled by the "activate_workspace" function. This function
may create one of more dockwidgets. This is done by the 

- activate_workspace  --> creates dockwidgets and adds them to ```self.guiWidgets```
this may be done by calling the show_guiWidget function with the widget class as parameter.
  
plugin to extend "activate_workspace"

- workspace name


## Adding nodes

This works via the context-menu

```
openContextMenyAt(..., node_name, ...)
```

plug-in to add entries to context menu.

the plugin gets called with the following arguments:

1. QMenu object
2. The name of the first selected node (if any)
3. A reference to the main gui

```python
for plugin in self.plugins_context:
    plugin(menu, node_name, self)
```

the reference to the main gui can be used to run code as follows:
```python
code = 'Balloon(s, s.available_name_like("new_balloon"))'
def action():
    gui.run_code(code, guiEventType.MODEL_STRUCTURE_CHANGED)

menu.addAction("Add balloon", action)
```


## Editing nodes

Selecting a node while in "construction" makes the "Properties" dock-widget visible.
Also the SELECTION_CHANGED event is emitted which a dockwidget can respond to.

### Extending the node-editor

"Name" and "visible" properties are set in the widget.

Sections in the node-propeties widget derive from `NodeEditor`

`WidgetNodeProps` creates `NodeEditor`s for the node class.

plug-in to add more widgets to the nodes-properties-widget:
- selected node
- returns: MyNewNodeEditor class.

Widget-nodeprops will call this class with the following arguments:
`MyNewNodeEditor(node, self.node_property_changed, self.guiScene, self.run_code)`

1. Create a new `MyNewNodeEditor` class which derives from `NodeEditor`
2. Provide a plug-in function which takes a node as input and returns `MyNewNodeEditor` or `None`. 

### Alternatively

Create a new workspace with a workspace-widget that reacts to the "SELECTION_CHANGED" event.




