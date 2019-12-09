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


import bpy


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


class MenuI3D(bpy.types.Menu):
    bl_label = "Giants I3D Menu"
    bl_idname = "OBJECT_MT_i3d_menu"  # "OBJECT_MT_custom_menu"


def draw(self, context):
    layout = self.layout

    
    layout.operator("wm.i3d_menu_export")
    layout.operator("wm.open_mainfile")
    layout.operator("wm.save_as_mainfile").copy = True
    
    layout.operator("object.shade_smooth")
    
    layout.label(text="v {0}".format(bl_info["version"]), icon='WORLD_DATA')
    
    # use an operator enum property to populate a sub-menu
    layout.operator_menu_enum("object.select_by_type",
                              property="type",
                              text="Select All by Type...",
                              )

    # call another menu
    layout.operator("wm.call_menu", text="Unwrap").name = "VIEW3D_MT_uv_map"


def draw_I3D_Menu(self, context):
    layout = self.layout
    layout.menu(MenuI3D.bl_idname)


def register():
    bpy.utils.register_class(MenuI3D)

    # lets add ourselves to the main header
    bpy.types.INFO_HT_header.append(draw_I3D_Menu)


def unregister():
    bpy.utils.unregister_class(MenuI3D)

    bpy.types.INFO_HT_header.remove(draw_I3D_Menu)


if __name__ == "__main__":
    register()

    # the menu can also be called from scripts
    bpy.ops.wm.call_menu(name=MenuI3D.bl_idname)
