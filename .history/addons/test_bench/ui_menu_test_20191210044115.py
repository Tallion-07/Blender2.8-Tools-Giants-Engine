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
    "name": "GIANTS I3D Exporter Tools",
    "author": "GIANTS Software",
    "blender": (2, 80, 0),
    "version": (8, 1, 1),
    "location": "GIANTS I3D",
    "description": "GIANTS Utilities and Exporter",
    "warning": "",
    "wiki_url": "http://gdn.giants-software.com",
    "tracker_url": "http://gdn.giants-software.com",
    "category": "Game Engine"}

# ---------------------------------------------
# I3D Menu Class
# ---------------------------------------------


class I3D_Menu(bpy.types.Menu):
    bl_label = "Giants i3d Menu"
    bl_idname = "i3d_menu"

    def draw_I3D_menu(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile").copy = True
        layout.operator("wm.save_as_i3d_mainfile").copy = True

        layout.operator("object.shade_smooth")

        layout.label(text="v{0}".format(bl_info["version"]), icon='WORLD_DATA')

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
