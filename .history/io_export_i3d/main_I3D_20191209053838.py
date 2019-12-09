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
    "support": "community",
    "category": "Import-Export"
},

# global DCC_PLATFORM
# DCC_PLATFORM = "blender"
 
if "bpy" in locals():
    import importlib
# if "import_i3d" in locals():
#    importlib.reload('import_i3d') 
# if "export_i3d" in locals():
#    importlib.reload('export_i3d')

importlib.import_module('export_i3d', 'io_export_i3d')
import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
    )
from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper,
    axis_conversion,
    orientation_helper,
    path_reference_mode,
    )

# ----------------------------------------------
# Export section of Menu - Recreated from i3d_ui
# Format based on FBX export "init" file
# ----------------------------------------------
class Import_I3D(bpy.types.Operator, ImportHelper):
    """Import a i3d file."""
    bl_idname = "import_scene.i3d"
    bl_label = "Import I3D"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".i3d"
    filter_glob: StringProperty(default="*.i3d", options={'HIDDEN'})

    def execute(self, context):
        from . import i3d_import

        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "filter_glob",
                                            ))
        global_matrix = axis_conversion(from_forward=self.axis_forward,
                                        from_up=self.axis_up,
                                        ).to_4x4()
        keywords["global_matrix"] = global_matrix

        return i3d_import.load(context, **keywords)

    def draw(self, context):
        pass
# ----------------------------------------------
# Export section of Menu - Recreated from i3d_ui
# Format based on FBX export "init" file
# ----------------------------------------------
@orientation_helper(axis_forward='-Z', axis_up='Y')  # added
class Export_I3D(bpy.types.Operator, ExportHelper):  # changed bpy_extras.io_utils.ExportHelper
    """Export a I3D file."""

    bl_idname = "export_scene.i3d"
    bl_label = "Export I3D"
    bl_options = {'UNDO', 'PRESET'}  # preset added
    filename_ext = ".i3d"

    filter_glob: StringProperty(default="*.i3d", options={'HIDDEN'})


""" List of Operator properties, the attributes are assigned
    to the class instance from the operator settings before calling."""

ui_tab: EnumProperty(
    items=(('EXPORT', 'Export', 'Export-related settings'),
           ('ATTRIBUTES', 'Attributes', 'Attribute-related settings'),
           ),
    name="ui_tab", 
    description="Export Options Catagories",
    )
UI_exportOptions: BoolProperty(
    name="Export Options",
    description="Available Export Options",
    default=True,
    )
UI_shapeExportSubparts: BoolProperty(
    name="Shape Export Subparts",
    default=True,
    )
UI_miscellaneous: BoolProperty(
    name="Miscellaneous",
    default=True,
    )
UI_outputFile: BoolProperty(
    name="Output File",
    default=True,
    )
UI_currentNode: BoolProperty(
    name="Current Node",
    default=True,
    )
UI_rigidBody: BoolProperty(
    name="Rigid Body",
    default=True,
    )
UI_joint: BoolProperty(
    name="Joint",
    default=False,
    )
UI_rendering: BoolProperty(
    name="Rendering",
    default=True,
    )
I3D_exportIK: BoolProperty(
    name="IK",
    default=False,
    )
I3D_exportAnimation: BoolProperty(
    name="Animation",
    default=True,
    )
I3D_exportShapes: BoolProperty(
    name="Shapes",
    default=True,
    )
I3D_exportNurbsCurves: BoolProperty(
    name="Nurbs Curves",
    default=False,
    )
I3D_exportLights: BoolProperty(
    name="Lights",
    default=True,
    )
I3D_exportCameras: BoolProperty(
    name="Cameras",
    default=True,
    )
I3D_exportParticleSystems: BoolProperty(
    name="Particle Systems",
    default=False,
    )
I3D_exportUserAttributes: BoolProperty(
    name="User Attributes",
    default=True,
    )
I3D_exportNormals: BoolProperty(
    name="Normals",
    default=True,
    )
I3D_exportColors: BoolProperty(
    name="Vertex Colors",
    default=True,
    )
I3D_exportTexCoords: BoolProperty(
    name="UVs",
    default=True,
    )
I3D_exportSkinweights: BoolProperty(
    name="Skin weights",
    default=True,
    )
I3D_exportMergeGroups: BoolProperty(
    name="Merge Groups",
    default=True,
    )
I3D_exportVerbose: BoolProperty(
    name="Verbose",
    description="Print info",
    default=True,
    )
I3D_exportRelativePaths: BoolProperty(
    name="Relative Paths",
    default=True,
    )
I3D_exportApplyModifiers: BoolProperty(
    name="Apply Modifiers",
    default=True,
    )
I3D_exportAxisOrientations: EnumProperty(
    items=(("BAKE_TRANSFORMS", "Bake Transforms", "Change axis Z = Y"),
           ("KEEP_AXIS", "Keep Axis", "Rotate Root objects on 90 degrees by X"),
           ("KEEP_TRANSFORMS", "Keep Transforms", "Export with no changes"),
           ),
    name="Axis Orientations",
    default="BAKE_TRANSFORMS",
    )
I3D_exportUseSoftwareFileName: BoolProperty(
    name="Use Blender Filename",
    default=True,
    )
I3D_exportFileLocation: StringProperty(
    name="File Location",
    subtype="FILE_PATH",
    )
I3D_nodeName: StringProperty(
    name="Loaded Node",
    default='',
    )
I3D_nodeIndex: StringProperty(
    name="Node Index",
    default='',
    )
I3D_static: BoolProperty(
    name="Static",
    default=True,
    description="passive Rigid Body non movable",
    )
I3D_dynamic: BoolProperty(
    name="Dynamic",
    default=False,
    description="active Rigid Body simulated",
    )
I3D_kinematic: BoolProperty(
    name="Kinematic",
    default=False,
    description="passive Rigid Body movable",
    )
I3D_compound: BoolProperty(
    name="Compound",
    default=False,
    description="group of Rigid Bodies",
    )
I3D_compoundChild: BoolProperty(
    name="Compound Child",
    default=False,
    description="part of a group of Rigid Bodies",
    )
I3D_collision: BoolProperty(
    name="Collision",
    default=True,
    )
I3D_collisionMask: IntProperty(
    name="Collision Mask",
    default=255,
    )
I3D_solverIterationCount: IntProperty(
    name="Solver Iterations",
    default=4,
    )
I3D_restitution: FloatProperty(
    name="Restitution",
    default=0,
    )
I3D_staticFriction: FloatProperty(
    name="Static Friction",
    default=0.5,
    )
I3D_dynamicFriction: FloatProperty(
    name="Dynamic Friction",
    default=0.5,
    )
I3D_linearDamping: FloatProperty(
    name="Linear Damping",
    default=0.0,
    )
I3D_angularDamping: FloatProperty(
    name="Angular Damping",
    default=0.01,
    )
I3D_density: FloatProperty(
    name="Density",
    default=1.0,
    )
I3D_ccd: BoolProperty(
    name="Continues Collision Detection",
    default=False,
    )
I3D_trigger: BoolProperty(
    name="Trigger",
    default=False,
    )
I3D_splitType: IntProperty(
    name="Split Type",
    default=0,
    )
I3D_splitMinU: FloatProperty(
    name="Split Min U",
    default=0.0,
    )
I3D_splitMinV: FloatProperty(
    name="Split Min V",
    default=0.0,
    )
I3D_splitMaxU: FloatProperty(
    name="Split Max U",
    default=1.0,
    )
I3D_splitMaxV: FloatProperty(
    name="Split Max V",
    default=1.0,
    )
I3D_splitUvWorldScale: FloatProperty(
    name="Split UV's worldScale",
    default=1.0,
    )
I3D_joint: BoolProperty(
    name="Joint",
    default=False,
    )
I3D_projection: BoolProperty(
    name="Projection",
    default=False,
    )
I3D_projDistance: FloatProperty(
    name="Projection Distance",
    default=0.01,
    )
I3D_projAngle: FloatProperty(
    name="Projection Angle",
    default=0.01,
    )
I3D_xAxisDrive: BoolProperty(
    name="X-Axis Drive",
    default=False,
    )
I3D_yAxisDrive: BoolProperty(
    name="Y-Axis Drive",
    default=False,
    )
I3D_zAxisDrive: BoolProperty(
    name="Z-Axis Drive",
    default=False,
    )
I3D_drivePos: BoolProperty(
    name="Drive Position",
    default=False,
    )
I3D_driveForceLimit: FloatProperty(
    name="Drive Force Limit",
    default=100000,
    )
I3D_driveSpring: FloatProperty(
    name="Drive Spring",
    default=1.0,
    )
I3D_driveDamping: FloatProperty(
    name="Drive Damping",
    default=0.01,
    )
I3D_breakableJoint: BoolProperty(
    name="Breakable",
    default=False,
    )
I3D_jointBreakForce: FloatProperty(
    name="Break Force",
    default=0.0,
    )
I3D_jointBreakTorque: FloatProperty(
    name="Break Torque",
    default=0.0,
    )
I3D_oc: BoolProperty(
    name="Occlusion Culling",
    default=False,
    )
I3D_castsShadows: BoolProperty(
    name="Casts Shadows",
    default=False,
    )
I3D_receiveShadows: BoolProperty(
    name="Receive Shadows",
    default=False,
    )
I3D_nonRenderable: BoolProperty(
    name="Non Renderable",
    default=False,
    )
I3D_clipDistance: FloatProperty(
    name="Clip Distance",
    default=0,
    )
I3D_objectMask: IntProperty(
    name="Object Mask",
    default=255,
    )
I3D_lightMask: StringProperty(
    name="Light Mask (Hex)",
    default='FFFF',
    )
I3D_decalLayer: IntProperty(
    name="Decal Layer",
    default=0,
    )
I3D_mergeGroup: IntProperty(
    name="Merge Group",
    default=0,
    )
I3D_mergeGroupRoot: BoolProperty(
    name="Merge Group Root",
    default=False,
    )
I3D_boundingVolume: StringProperty(
    name="Bounding Volume",
    default='',
    )
I3D_cpuMesh: BoolProperty(
    name="CPU Mesh",
    default=False,
    )
I3D_lod: BoolProperty(
    name="LOD",
    default=False,
    )
I3D_lod0: FloatProperty(
    name="Child 0 Distance",
    default=0,
    )
I3D_lod1: FloatProperty(
    name="Child 1 Distance",
    default=0,
    )
I3D_lod2: FloatProperty(
    name="Child 2 Distance",
    default=0,
    )
I3D_lod3: FloatProperty(
    name="Child 3 Distance",
    default=0,
    )
path_mode: path_reference_mode

def draw(self, context):
    layout = self.layout
# NOTE TODO check if required   layout.label(text="v {0}".format(bl_info["version"]))
    layout.operator("i3d.menu_export")

    # -----------------------------------------
    # "Export Selected" box
    # -----------------------------------------
    box = layout.box()
    row = box.row()
    row.prop(self, "I3D_exportSelected")
    # ----------------------------------------
    # "Export Options" box
    # ----------------------------------------
    box = layout.box()
    row = box.row()
    # expand button for "Export Options"
    row.prop(self, "UI_exportOptions",
             icon='TRIA_DOWN'
             if self.UI_exportOptions
             else
             'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if self.UI_exportOptions:
        row = box.row()
        row.prop(self, "I3D_exportIK")
        row.prop(self, "I3D_exportAnimation")
        row = box.row()
        row.prop(self, "I3D_exportShapes")
        row.prop(self,
                 "I3D_exportNurbsCurves")
        row = box.row()
        row.prop(self, "I3D_exportLights")
        row.prop(self, "I3D_exportCameras")
        row = box.row()
        row.prop(self, "I3D_exportParticleSystems")
        row.prop(self,"I3D_exportUserAttributes")
    # -----------------------------------------
    # "Shape Export Subparts" box
    # -----------------------------------------
    box = layout.box()
    row = box.row()
    # expand button for "Shape Export Subparts"
    row.prop(self,
             "UI_shapeExportSubparts",
             icon='TRIA_DOWN'
             if self.UI_shapeExportSubparts
             else
             'TRIA_RIGHT', icon_only=True, emboss=False)
    if self.UI_shapeExportSubparts:
        row = box.row()
        row.prop(self, "I3D_exportNormals")
        row.prop(self, "I3D_exportTexCoords")
        row = box.row()
        row.prop(self, "I3D_exportColors")
        row.prop(self, "I3D_exportSkinweights")
        row = box.row()
        row.prop(self, "I3D_exportMergeGroups")
    # -----------------------------------------
    # "Miscellaneous" box
    # -----------------------------------------
    box = layout.box()
    row = box.row()
    # expand button for "Miscellaneous"
    row.prop(self, "UI_miscellaneous",
             icon='TRIA_DOWN'
             if self.UI_miscellaneous
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    if self.UI_miscellaneous:
        row = box.row()
        row.prop(self, "I3D_exportVerbose")
        row.prop(self, "I3D_exportRelativePaths")
        row = box.row()
        row.prop(self, "I3D_exportApplyModifiers")
        row = box.row()
        row.prop(self, "I3D_exportAxisOrientations")
    # -----------------------------------------


def execute(self, context):
    bpy.self.I3D_exportUseSoftwareFileName = False
    bpy.self.I3D_exportFileLocation = self.filepath
    if (self.I3D_exportSelected):
        io_export_i3d.export_i3d.I3DExportSelected()
    else:
        io_export_i3d.export_i3d.I3DExportAll()
    return {'FINISHED'}

# -----------------------------------------------------------------------------
#   Properties Panel
# -----------------------------------------------------------------------------


class I3D_PanelExportView:
    bl_label = "GIANTS I3D Exporter"
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = "TOOL_PROPS"
    bl_idname = "i3d_panel_export"
    bl_category = "scene"


def draw(self, context):
    layout = self.layout

    layout.prop(self, "UI_settingsMode", expand=True)
    # -----------------------------------------
    # "Export" tab
    # -----------------------------------------
    if 'exp' == self.UI_settingsMode:
        # -----------------------------------------
        # "Export Options" box
        # -----------------------------------------
        box = layout.box()
    row = box.row()
    # expand button for "Export Options"
    row.prop(self, "UI_exportOptions",
             icon='TRIA_DOWN'
             if self.UI_exportOptions
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if self.UI_exportOptions:
        row = box.row()
        row.prop(self, "I3D_exportIK")
        row.prop(self, "I3D_exportAnimation")
        row = box.row()
        row.prop(self, "I3D_exportShapes")
        row.prop(self, "I3D_exportNurbsCurves")
        row = box.row()
        row.prop(self, "I3D_exportLights")
        row.prop(self, "I3D_exportCameras")
        row = box.row()
        row.prop(self, "I3D_exportParticleSystems")
        row.prop(self, "I3D_exportUserAttributes")
    # -----------------------------------------
    # "Shape Export Subparts" box
    # -----------------------------------------
    box = layout.box()
    row = box.row()
    # expand button for "Shape Export Subparts"
    row.prop(self,
             "UI_shapeExportSubparts", icon='TRIA_DOWN'
             if self.UI_shapeExportSubparts
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    if self.UI_shapeExportSubparts:
        row = box.row()
        row.prop(self, "I3D_exportNormals")
        row.prop(self, "I3D_exportTexCoords")
        row = box.row()
        row.prop(self, "I3D_exportColors")
        row.prop(self, "I3D_exportSkinweights")
        row = box.row()
        row.prop(self, "I3D_exportMergeGroups")
    # -----------------------------------------
    # "Miscellaneous" box
    # -----------------------------------------
    box = layout.box()
    row = box.row()
    # expand button for "Miscellaneous"
    row.prop(self, "UI_miscellaneous",
             icon='TRIA_DOWN'
             if self.UI_miscellaneous
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    if self.UI_miscellaneous:
        row = box.row()
        row.prop(self, "I3D_exportVerbose")
        row.prop(self, "I3D_exportRelativePaths")
        row = box.row()
        row.prop(self, "I3D_exportApplyModifiers")
        row = box.row()
        row.prop(self, "I3D_exportAxisOrientations")
    # -----------------------------------------
    # "Output File" box
    # -----------------------------------------
    box = layout.box()
    row = box.row()
    # expand button for "Output File"
    row.prop(self, "UI_outputFile",
             icon='TRIA_DOWN'
             if self.UI_outputFile
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    if self.UI_outputFile:
        row = box.row()
        row.prop(self, "I3D_exportUseSoftwareFileName")
        row = box.row()
        row.enabled = not self.I3D_exportUseSoftwareFileName
        row.prop(self, "I3D_exportFileLocation")
    # -----------------------------------------
    row = layout.row(align=True)
    row.operator("i3d.panel_export_do", text="Export All").state = 1
    row.operator("i3d.panel_export_do", text="Export Selected").state = 2
    # -----------------------------------------
    # TODO Check "Attributes tab" elif
    # "Attributes" tab
    # -----------------------------------------
    if 'attr' == self.UI_settingsMode:
        # -----------------------------------------
        # "Current Node" box
        # -----------------------------------------
        box = layout.box()
        row = box.row()
    # expand button for "Current Node"
    row.prop(self, "UI_currentNode",
             icon='TRIA_DOWN'
             if self.UI_currentNode
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if self.UI_currentNode:
        row = box.row()
        row.enabled = False
        row.prop(self, "I3D_nodeName", text="Loaded Node")
        row = box.row()
        row.enabled = False
        row.prop(self, "I3D_nodeIndex", text="Node Index")
    # -----------------------------------------
    # "Rigid Body" box
    # -----------------------------------------
    box = layout.box()
    row = box.row()
    # expand button for "Rigid Body"
    row.prop(self, "UI_rigidBody",
             icon='TRIA_DOWN'
             if self.UI_rigidBody
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if self.UI_rigidBody:
        col = box.column()
        col.prop(self, "I3D_static", text="Static")
        col.prop(self, "I3D_kinematic", text="Kinematic")
        col.prop(self, "I3D_dynamic", text="Dynamic")
        col.prop(self, "I3D_compound", text="Compound")
        col.prop(self, "I3D_compoundChild", text="Compound Child")
        col.prop(self, "I3D_collision", text="Collision")
        col.prop(self, "I3D_collisionMask", text="Collision Mask")
        col.prop(self, "I3D_restitution", text="Restitution")
        col.prop(self, "I3D_staticFriction", text="Static Friction")
        col.prop(self, "I3D_dynamicFriction", text="Dynamic Friction")
        col.prop(self, "I3D_linearDamping", text="Linear Damping")
        col.prop(self, "I3D_angularDamping", text="Angular Damping")
        col.prop(self, "I3D_density", text="Density")
        col.prop(self, "I3D_solverIterationCount", text="Solve Iterations")
        col.prop(self, "I3D_ccd", text="Continues Collision Detection")
        col.prop(self, "I3D_trigger", text="Trigger")
        col.prop(self, "I3D_splitType", text="Split Type")
        row = col.row()
        row.prop(self, "I3D_splitMinU", text="Split Min U")
        row.prop(self, "I3D_splitMaxU", text="Split Max U")
        row = box.row()
        row.prop(self, "I3D_splitMinV", text="Split Min V")
        row.prop(self, "I3D_splitMaxV", text="Split Max V")
        row = box.row()
        row.prop(self, "I3D_splitUvWorldScale", text="Split UV's worldScale")
    # -----------------------------------------
    # "Joint" box
    # -----------------------------------------
    box = layout.box()
    row = box.row()
    # expand button for "Joint"
    row.prop(self, "UI_joint", icon='TRIA_DOWN'
             if self.UI_joint
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if self.UI_joint:
        col = box.column()
        col.prop(self, "I3D_joint", text="Joint")
        col.prop(self, "I3D_projection", text="Projection")
        col.prop(self, "I3D_projDistance", text="Projection Distance")
        col.prop(self, "I3D_projAngle", text="Projection Angle")
        col.prop(self, "I3D_xAxisDrive", text="X-Axis Drive")
        col.prop(self, "I3D_yAxisDrive", text="Y-Axis Drive")
        col.prop(self, "I3D_zAxisDrive", text="Z-Axis Drive")
        col.prop(self, "I3D_drivePos", text="Drive Position")
        col.prop(self, "I3D_driveForceLimit", text="Drive Force Limit")
        col.prop(self, "I3D_driveSpring", text="Drive Spring")
        col.prop(self, "I3D_driveDamping", text="Drive Damping")
        col.prop(self, "I3D_breakableJoint", text="Breakable")
        col.prop(self, "I3D_jointBreakForce", text="Break Force")
        col.prop(self, "I3D_jointBreakTorque", text="Break Torque")
    # -----------------------------------------
    # "Rendering" box
    # -----------------------------------------
    box = layout.box()
    row = box.row()
    # expand button for "Rendering"
    row.prop(self, "UI_rendering",
             icon='TRIA_DOWN'
             if self.UI_rendering
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if self.UI_rendering:
        col = box.column()
        col.prop(self, "I3D_oc", text="Occlusion Culling")
        col.prop(self, "I3D_castsShadows", text="Casts Shadows")
        col.prop(self, "I3D_receiveShadows", text="Receive Shadows")
        col.prop(self, "I3D_nonRenderable", text="Non Renderable")
        col.prop(self, "I3D_clipDistance", text="Clip Distance")
        col.prop(self, "I3D_objectMask", text="Object Mask")
        col.prop(self, "I3D_lightMask", text="Light Mask (Hex)")
        col.prop(self, "I3D_decalLayer", text="Decal Layer")
        col.prop(self, "I3D_mergeGroup", text="Merge Group")
        col.prop(self, "I3D_mergeGroupRoot", text="Merge Group Root")
        col.prop(self, "I3D_boundingVolume", text="Bounding Volume")
        col.prop(self, "I3D_cpuMesh", text="CPU Mesh")
        col.prop(self, "I3D_lod", text="LOD")
        row = col.row()
        row.enabled = False
        row.prop(self, "I3D_lod0", text="Child 0 Distance")
        col.prop(self, "I3D_lod1", text="Child 1 Distance")
        col.prop(self, "I3D_lod2", text="Child 2 Distance")
        col.prop(self, "I3D_lod3", text="Child 3 Distance")
    # -----------------------------------------
    row = layout.row(align=True)
    row.operator("i3d.panel_export_attr", text="Load Current").state = 1
    row.operator("i3d.panel_export_attr", text="Save Current").state = 2
    row.operator("i3d.panel_export_attr", text="Remove Current").state = 3
    row = layout.row(align=True)
    row.operator("i3d.panel_export_attr", text="Apply Selected").state = 4
    row.operator("i3d.panel_export_attr", text="Remove Selected").state = 5
    
    def set_buttonAttrSelect(self, context):
        selected_objs = context.selected_objects
    
    buttonAttrSelect_type = None

    if self.ButtonAttrSelect == 'LC':
        buttonAttrSelect_type = 'Load Current'
    elif self.ButtonAttrSelect == 'SC':
        buttonAttrSelect_type = 'Save Current'
    elif self.ButtonAttrSelect == 'RC':
        buttonAttrSelect_type = 'Remove Current' 
    elif self.ButtonAttrSelect == 'AS':
        buttonAttrSelect_type = 'Apply Selected'
    elif self.ButtonAttrSelect == 'RS':
        buttonAttrSelect_type = 'Remove Selected'

    else:
        UIShowWarning('Nothing Selected')

    bpy.types,Scene.ButtonAttrSelect = bpy.props.EmumProperty(
        items=[('LC', 'None', ''),
        ('SC', 'Save Current', ''),
        ('RC', 'Remove Current', ''),
        ('AS', 'Apply Selected', ''),
        ('RS', 'Remove Selected', '')],
        name="ButtonAttrSelect",
        update=set_buttonAttrSelect
    )    

    # -----------------------------------------
    row = layout.row()
    row.operator("i3d.panel_export_close", icon='X')


# -----------------------------------------------------------------------------
#   Panel Buttons # NOTE TODO
# -----------------------------------------------------------------------------
class I3D_PanelExport_ButtonAttr(bpy.types.Operator):
    bl_idname = "i3d.panel_export_attr"
    bl_label = "Attributes"
        
    def execute(self, context):
        if self.state == 1:
            i3d.panel_export_attr == I3DLoadObjectAttributes()
        elif 2 == self.state:
            I3DSaveObjectAttributes()
        elif 3 == self.state:
            I3DRemoveObjectAttributes()
        elif 4 == self.state:
            I3DApplySelectedAttributes()
        elif 5 == self.state:
            I3DRemoveSelectedAttributes()
        return {'FINISHED'}


class I3D_PanelExport_ButtonExport(bpy.types.Operator):
    bl_idname = "i3d.panel_export_do"
    bl_label = "Export"
    state = bpy.props.IntProperty()
    
def execute(self, context):
    if 1 == self.state:
       io_export_i3d.export_i3d.I3DExportAll()
    elif 2 == self.state:
        io_export_i3d.export_i3d.I3DExportSelected()
    return {'FINISHED'}
        
@property
def check_extension(self):
    return self.batch_mode == 'OFF'

def execute(self, context):
    from mathutils import Matrix
    if not self.filepath:
        raise Exception("filepath not set")

    global_matrix = (axis_conversion(to_forward=self.axis_forward, to_up=self.axis_up, ).to_4x4())
    keywords = self.as_keywords(ignore=("check_existing", "filter_glob", "ui_tab"))
    keywords["global_matrix"] = global_matrix
    from . import export_i3d_bin
    return export_i3d_bin.save(self, context, **keywords)




def menu_func_import(self, context):
    self.layout.operator(Import_I3D.bl_idname, text="GIANTS I3D (.i3d)")
    
def menu_func_export(self, context):
    self.layout.operator(Export_I3D.bl_idname, text="GIANTS I3D (.i3d)")    

classes = (
    Import_I3D,
    Export_I3D,
    
)

def register():
    """Change in register function but retain bpy.types header.append."""
    for cls in classes:
        bpy.utils.register_class(cls)     
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    


def unregister():
    """Change in Unregister method but retain bpy.types.header.remover"""
    bpy.types.TOPBAR_HT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
   

    for cls in classes:
        bpy.utils.unregister_class(cls)


print("My Script Finished: %.4f sec" % (time.time() - time_start))

if __name__ == "__main__":
    register()
