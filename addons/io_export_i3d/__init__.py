# #!/usr/bin/env python3
# <pep8-80 compliant>

"""
             ##### BEGIN GPL LICENSE BLOCK #####.

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software Foundation,
  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
                ##### END GPL LICENSE BLOCK #####

TODO: check current programming
"""
# <pep8-120 compliant>


bl_info = {
    "name": "GIANTS I3D Blender Tools",
    "description": "GIANTS i3D Game Engine Import-Export.",
    "author": "GIANTS Software, Jason Oppermann",
    "version": (8, 1, 1),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "warning": "Community Version under testing",
    "wiki_url": "https://github.com/Tallion-07/Blender-2.8-Plug-in-Giants-Engine/wiki",
    "support": "community",
    "category": "Import-Export"
}

global DCC_PLATFORM
DCC_PLATFORM = "blender"

if "bpy" in locals():
    import importlib
    if "i3d_ui" in locals():
        importlib.reload(i3d_ui)
        importlib.reload(dcc)

else:
    from io_export_i3d import i3d_ui
    from . import dcc

import bpy


class I3D_Menu(bpy.types.Menu):
    """Menu class labels."""
    
    bl_label = "GIANTS I3D"
    bl_idname = "i3d_menu"

def draw(self, context):
    """Menu layout."""
    layout = self.layout
    layout.label(text="v {0}".format(bl_info["version"]))
    layout.operator("i3d.menu_export")
      
def draw_I3D_Menu(self, context):
    """Field filling of menu label."""
    self.layout.menu(I3D_Menu.bl_idname)

"""TODO
classes = (
    ImportI3D,
    ExportI3D,
)
"""
"""Registration and reverse to be completed."""
def register():
    """Registration of plug-in."""
    """TODO - for cls in classes:
        from bpy.utils import register_class
        for cls in classes:
            register_class(cls)
    """
    i3d_ui.register()
    bpy.utils.register_class(I3D_Menu)
    bpy.types.INFO_HT_header.append(draw_I3D_Menu)

def unregister():
    """Deregistration of plug-in."""
    """TODO - from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    """
    i3d_ui.unregister()
    bpy.utils.unregister_class(I3D_Menu)
    bpy.types.INFO_HT_header.remove(draw_I3D_Menu)

if __name__ == "__main__":
    register()

# -----------------------------------------------------------------------------

