#!/usr/bin/env python3
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

import bpy

print(__file__)
bl_info = {
    "name": "GIANTS I3D Blender Tools",
    "description": "GIANTS i3D Game Engine Import-Export.",
    "author": "GIANTS Software, Jason Oppermann",
    "version": (8, 1, 1),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "warning": "Community Version under testing",
    "wiki_url": "https://github.com/Tallion-07/Blender-2.8-Plug-in-Giants-Engine/wiki",
    "tracker_url": "https://github.com/Tallion-07/Blender-2.8-Plug-in-Giants-Engine",
    "support": "community",
    "category": "Import-Export"
}

if "bpy" in locals():

    import importlib

    importlib.reload('i3d_ui')
    importlib.reload('i3d_lib')
    importlib.reload('dccBlender')
    importlib.reload('i3d_export')
    importlib.reload('i3d_IOexport')
    importlib.reload('i3d_UIexport')

else:
    from io_export_i3d import dccBlender, i3d_export, i3d_IOexport, i3d_lib, \
       i3d_ui, i3d_UIexport


# ------------------------------------------------------------------------------
#   I3D Menu Class
# ------------------------------------------------------------------------------


class I3D_Menu(bpy.types.Menu):
    """Menu labels."""

    bl_idname = "i3d_menu"
    bl_label = "GIANTS I3D"


def Draw(self, context):
    """Label layout."""
    layout = self.layout
    layout.label(text="v {0}".format(bl_info["version"]))
    layout.operator("i3d.menu_export")

# ------------------------------------------------------------------------------
#   I3D Menu Draw
# ------------------------------------------------------------------------------


def draw_I3D_Menu(self, context):
    """Draw Menu."""
    self.layout.menu(I3D_Menu.bl_idname)

# ------------------------------------------------------------------------------
#   Register
# ------------------------------------------------------------------------------


def register():
    """Register i3d_ui file."""
    i3d_ui.register()
    bpy.utils.register_class(I3D_Menu)
    bpy.types.INFO_HT_header.append(draw_I3D_Menu)

# ------------------------------------------------------------------------------
# UnRegister
# ------------------------------------------------------------------------------


def unregister():
    """Unregister i3d_ui file."""
    i3d_ui.unregister()
    bpy.utils.unregister_class(I3D_Menu)
    bpy.types.INFO_HT_header.remove(draw_I3D_Menu)


if __name__ == "__main__":
    register()
# ------------------------------------------------------------------------------
