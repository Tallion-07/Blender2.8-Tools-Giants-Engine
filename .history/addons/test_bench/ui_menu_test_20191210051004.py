# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
bl_info = {
    "name": "I3D Tools",
    "author": "GIANTS Software, Jason Oppermann",
    "version": (8, 1, 2),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "GIANTS Utilities and Exporter",
    "warning": "TESTING",
    "wiki_url": "https://github.com/Tallion-07/Blender2.8-Tools-Giants-Engine/wiki",
    "support": "TESTING",
    "category": "Import-Export"}

# ---------------------------------------------
# I3D Menu Class
# ---------------------------------------------


class I3D_Menu(bpy.types.Menu):
    bl_label = "Giants i3d Menu"
    bl_idname = "i3d_menu"

    def draw(self, context):
        layout = self.layout

        layout.label(text="{1}{0}".format(bl_info["name"]), icon='WORLD_DATA')
        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile").copy = True
        layout.operator("save_as_i3d_mainfile")

        layout.operator("object.shade_smooth")

        # use an operator enum property to populate a sub-menu
        layout.operator_menu_enum("object.select_by_type",
                                  property="type",
                                  text="Select All by Type...",
                                  )

        # call another menu
        layout.operator("wm.call_menu", text="Unwrap").name = "VIEW3D_MT_uv_map"

# ---------------------------------------------
# Draw I3D Menu
# ---------------------------------------------


def draw_I3D_Menu(self, context):
    layout = self.layout
    layout.menu(I3D_Menu.bl_idname)

# ---------------------------------------------
# Register
# ---------------------------------------------


def register():
    bpy.utils.register_class(I3D_Menu)

    # lets add ourselves to the main header
    bpy.types.INFO_HT_header.append(draw_I3D_Menu)


def unregister():
    bpy.utils.unregister_class(I3D_Menu)

    bpy.types.INFO_HT_header.remove(draw_I3D_Menu)


if __name__ == "__main__":
    register()

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=I3D_Menu.bl_idname)
