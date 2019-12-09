#
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
"""
# TODO: check current programming

# <pep8-120 compliant>

import time
import bpy
time_start = time.time()

bl_info = {
    "name": "GIANTS I3D Blender Tools",
    "description": "GIANTS i3D Game Engine Import-Export.",
    "author": "GIANTS Software, Jason Oppermann",
    "version": (8, 1, 1),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "warning": "Community Version under testing",
    "wiki_url": "https://github.com/Tallion-07/Blender-2.8-Plug-in-Giants-Engine/wiki",
    "support": "TESTING",
    "category": "Import-Export"
    },

# global DCC_PLATFORM
# DCC_PLATFORM = "blender"

# if "bpy" in locals():
#    import importlib
# if "i3d_ui" in locals():
#    importlib.reload(i3d_ui)
# if "export_i3d" in locals():
#    importlib.reload(dcc)
# else:
#    from io_export_i3d import i3d_ui
#    from io_export_i3d import dcc


# -------------------------------------------------------------------------------
#   I3D Menu Class
# -------------------------------------------------------------------------------


class MenuI3D(bpy.types.Menu):
    bl_label = "Giants I3D Menu"
    bl_idname = "i3d_menu"  # "OBJECT_MT_custom_menu"


def draw(self, context):
    layout = self.layout

    layout.label(text="v {0}".format(bl_info["version"]), icon='WORLD_DATA')
    layout.operator("wm.i3d.menu_export")
    layout.operator("wm.open_mainfile")
    layout.operator("wm.save_as_mainfile").copy = True
    layout.operator("object.shade_smooth")

    # use an operator enum property to populate a sub-menu
    layout.operator_menu_enum("object.select_by_type",
                              property="type",
                              text="Select All by Type...",
                              )

    # call another menu
    layout.operator("wm.call_menu", text="Unwrap").name = "VIEW3D_MT_uv_map"


# -------------------------------------------------------------------------------
#   I3D Menu Draw
# -------------------------------------------------------------------------------


def draw_I3D_Menu(self, context):
    layout = self.layout
    self.menu(MenuI3D.bl_idname)

# -------------------------------------------------------------------------------
#   Register
# -------------------------------------------------------------------------------


def register():
    # i3d_ui.register() <- # NOTE does this need to be called for next file
    bpy.utils.register_class(MenuI3D)

    # lets add ourselves to the main header
    bpy.types.INFO_HT_header.append(draw_I3D_Menu)


def unregister():
    # i3d_ui.unregister() <- # NOTE see above
    bpy.utils.unregister_class(MenuI3D)

    bpy.types.INFO_HT_header.remove(draw_I3D_Menu)


if __name__ == "__main__":
    register()

    # the menu can also be called from scripts
    bpy.ops.wm.call_menu(name=MenuI3D.bl_idname)

# -------------------------------------------------------------------------------
