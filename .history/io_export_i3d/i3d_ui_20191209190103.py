#!/usr/bin/env python3

"""
    ##### BEGIN GPL LICENSE BLOCK #####

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

# print(__file__)

import bpy
import bpy_extras
import io_export_i3d.dcc as dcc
import io_export_i3d.i3d_export

from bpy.props import (BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty)

from bpy_extras.io_utils import (ExportHelper, axis_conversion, orientation_helper, path_reference_mode)

# ----------------------------------------------------------------------------
#   File -> Export
# -----------------------------------------------------------------------------


@orientation_helper(axis_forward='-Z', axis_up='Y')  # added
class I3D_FileExport(bpy.types.Operator, ExportHelper):  # changed bpy_extras.io_utils.ExportHelper
    """Write a I3D file."""
    bl_idname = "i3d.file_export"
    bl_label = "Export I3D"
    bl_options = {'UNDO', 'PRESET'}  # preset added
    filename_ext = ".i3d"

    filter_glob: StringProperty(default="*.i3d", options={'HIDDEN'})


""" 
List of Operator properties, the attributes are assigned
    to the class instance from the operator settings before calling.
"""

I3D_exportSelected: BoolProperty(
    name="Export Selected",
    default=False,
    )
ui_tab: EnumProperty(
    items=(('EXPORT', 'Export', 'Export-related settings'),
           ('ATTRIBUTES', 'Attributes', 'Attribute-related settings'),
           ),
    name="ui_tab", 
    description="Export Settings",
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
    default=dcc.SETTINGS_UI['I3D_exportIK']['defaultValue'],
    )
I3D_exportAnimation: BoolProperty(
    name="Animation",
    default=dcc.SETTINGS_UI['I3D_exportAnimation']['defaultValue'],
    )
I3D_exportShapes: BoolProperty(
    name="Shapes",
    default=dcc.SETTINGS_UI['I3D_exportShapes']['defaultValue'],
    )
I3D_exportNurbsCurves: BoolProperty(
    name="Nurbs Curves",
    default=dcc.SETTINGS_UI['I3D_exportNurbsCurves']['defaultValue'],
    )
I3D_exportLights = bpy.props.BoolProperty(
    name="Lights",
    default=dcc.SETTINGS_UI['I3D_exportLights']['defaultValue'],
    )
I3D_exportCameras: BoolProperty(
    name="Cameras",
    default=dcc.SETTINGS_UI['I3D_exportCameras']['defaultValue'],
    )
I3D_exportParticleSystems: BoolProperty(
    name="Particle Systems",
    default=dcc.SETTINGS_UI['I3D_exportParticleSystems']['defaultValue'],
    )
I3D_exportUserAttributes: BoolProperty(
    name="User Attributes",
    default=dcc.SETTINGS_UI['I3D_exportUserAttributes']['defaultValue'],
    )
I3D_exportNormals: BoolProperty(
    name="Normals",
    default=dcc.SETTINGS_UI['I3D_exportNormals']['defaultValue'],
    )
I3D_exportColors: BoolProperty(
    name="Vertex Colors",
    default=dcc.SETTINGS_UI['I3D_exportColors']['defaultValue'],
    )
I3D_exportTexCoords: BoolProperty(
    name="UVs",
    default=dcc.SETTINGS_UI['I3D_exportTexCoords']['defaultValue'],
    )
I3D_exportSkinWeigths: BoolProperty(
    name="Skin Weigths",
    default=dcc.SETTINGS_UI['I3D_exportSkinWeigths']['defaultValue'],
    )
I3D_exportMergeGroups: BoolProperty(
    name="Merge Groups",
    default=dcc.SETTINGS_UI['I3D_exportMergeGroups']['defaultValue'],
    )
I3D_exportVerbose: BoolProperty(
    name="Verbose",
    description="Print info",
    default=dcc.SETTINGS_UI['I3D_exportVerbose']['defaultValue'],
    )
I3D_exportRelativePaths: BoolProperty(
    name="Relative Paths",
    default=dcc.SETTINGS_UI['I3D_exportRelativePaths']['defaultValue'],
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
    default=dcc.SETTINGS_UI['I3D_exportUseSoftwareFileName']['defaultValue'],
    )
I3D_exportFileLocation: StringProperty(
    name="File Location",
    subtype="FILE_PATH",
    )
I3D_nodeName: StringProperty(
    name="Loaded Node",
    default=dcc.SETTINGS_UI['I3D_nodeName']['defaultValue'],
    )
I3D_nodeIndex: StringProperty(
    name="Node Index",
    default=dcc.SETTINGS_UI['I3D_nodeIndex']['defaultValue'],
    )
I3D_static: BoolProperty(
    name="Static",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_static']['defaultValue'],
    description="passive Rigid Body non movable",
    )
I3D_dynamic: BoolProperty(
    name="Dynamic",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_dynamic']['defaultValue'],
    description="active Rigid Body simulated",
    )
I3D_kinematic: BoolProperty(
    name="Kinematic",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_kinematic']['defaultValue'],
    description="passive Rigid Body movable",
    )
I3D_compound: BoolProperty(
    name="Compound",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_compound']['defaultValue'],
    description="group of Rigid Bodies",
    )
I3D_compoundChild: BoolProperty(
    name="Compound Child",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_compoundChild']['defaultValue'],
    description="part of a group of Rigid Bodies",
    )
I3D_collision: BoolProperty(
    name="Collision",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_collision']['defaultValue'],
    )
I3D_collisionMask: IntProperty(
    name="Collision Mask",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_collisionMask']['defaultValue'],
    )
I3D_solverIterationCount: IntProperty(
    name="Solver Iterations",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_solverIterationCount']['defaultValue'],
    )
I3D_restitution: FloatProperty(
    name="Restitution",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_restitution']['defaultValue'],
    )
I3D_staticFriction: FloatProperty(
    name="Static Friction",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_staticFriction']['defaultValue'],
    )
I3D_dynamicFriction: FloatProperty(
    name="Dynamic Friction",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_dynamicFriction']['defaultValue'],
    )
I3D_linearDamping: FloatProperty(
    name="Linear Damping",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_linearDamping']['defaultValue'],
    )
I3D_angularDamping: FloatProperty(
    name="Angular Damping",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_angularDamping']['defaultValue'],
    )
I3D_density: FloatProperty(
    name="Density",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_density']['defaultValue'],
    )
I3D_ccd: BoolProperty(
    name="Continues Collision Detection",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_ccd']['defaultValue'],
    )
I3D_trigger: BoolProperty(
    name="Trigger",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_trigger']['defaultValue'],
    )
I3D_splitType: IntProperty(
    name="Split Type",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_splitType']['defaultValue'],
    )
I3D_splitMinU: FloatProperty(
    name="Split Min U",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_splitMinU']['defaultValue'],
    )
I3D_splitMinV: FloatProperty(
    name="Split Min V",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_splitMinV']['defaultValue'],
    )
I3D_splitMaxU: FloatProperty(
    name="Split Max U",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_splitMaxU']['defaultValue'],
    )
I3D_splitMaxV: FloatProperty(
    name="Split Max V",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_splitMaxV']['defaultValue'],
    )
I3D_splitUvWorldScale: FloatProperty(
    name="Split UV's worldScale",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_splitUvWorldScale']['defaultValue'],
    )
I3D_joint: BoolProperty(
    name="Joint",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_joint']['defaultValue'],
    )
I3D_projection: BoolProperty(
    name="Projection",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_projection']['defaultValue'],
    )
I3D_projDistance: FloatProperty(
    name="Projection Distance",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_projDistance']['defaultValue'],
    )
I3D_projAngle: FloatProperty(
    name="Projection Angle",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_projAngle']['defaultValue'],
    )
I3D_xAxisDrive: BoolProperty(
    name="X-Axis Drive",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_xAxisDrive']['defaultValue'],
    )
I3D_yAxisDrive: BoolProperty(
    name="Y-Axis Drive",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_yAxisDrive']['defaultValue'],
    )
I3D_zAxisDrive: BoolProperty(
    name="Z-Axis Drive",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_zAxisDrive']['defaultValue'],
    )
I3D_drivePos: BoolProperty(
    name="Drive Position",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_drivePos']['defaultValue'],
    )
I3D_driveForceLimit: FloatProperty(
    name="Drive Force Limit",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_driveForceLimit']['defaultValue'],
    )
I3D_driveSpring: FloatProperty(
    name="Drive Spring",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_driveSpring']['defaultValue'],
    )
I3D_driveDamping: FloatProperty(
    name="Drive Damping",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_driveDamping']['defaultValue'],
    )
I3D_breakableJoint: BoolProperty(
    name="Breakable",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_breakableJoint']['defaultValue'],
    )
I3D_jointBreakForce: FloatProperty(
    name="Break Force",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_jointBreakForce']['defaultValue'],
    )
I3D_jointBreakTorque: FloatProperty(
    name="Break Torque",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_jointBreakTorque']['defaultValue'],
    )
I3D_oc: BoolProperty(
    name="Occlusion Culling",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_oc']['defaultValue'],
    )
I3D_castsShadows: BoolProperty(
    name="Casts Shadows",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_castsShadows']['defaultValue'],
    )
I3D_receiveShadows: BoolProperty(
    name="Receive Shadows",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_receiveShadows']['defaultValue'],
    )
I3D_nonRenderable: BoolProperty(
    name="Non Renderable",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_nonRenderable']['defaultValue'],
    )
I3D_clipDistance: FloatProperty(
    name="Clip Distance",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_clipDistance']['defaultValue'],
    )
I3D_objectMask: IntProperty(
    name="Object Mask",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_objectMask']['defaultValue'],
    )
I3D_lightMask: StringProperty(
    name="Light Mask (Hex)",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_lightMask']['defaultValue'],
    )
I3D_decalLayer: IntProperty(
    name="Decal Layer",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_decalLayer']['defaultValue'],
    )
I3D_mergeGroup: IntProperty(
    name="Merge Group",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_mergeGroup']['defaultValue'],
    )
I3D_mergeGroupRoot: BoolProperty(
    name="Merge Group Root",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_mergeGroupRoot']['defaultValue'],
    )
I3D_boundingVolume: StringProperty(
    name="Bounding Volume",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_boundingVolume']['defaultValue'],
    )
I3D_cpuMesh: BoolProperty(
    name="CPU Mesh",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_cpuMesh']['defaultValue'],
    )
I3D_lod: BoolProperty(
    name="LOD",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_lod']['defaultValue'],
    )
I3D_lod0: FloatProperty(
    name="Child 0 Distance",
    default=0,
    )
I3D_lod1: FloatProperty(
    name="Child 1 Distance",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_lod1']['defaultValue'],
    )
I3D_lod2: FloatProperty(
    name="Child 2 Distance",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_lod2']['defaultValue'],
    )
I3D_lod3: FloatProperty(
    name="Child 3 Distance",
    default=dcc.SETTINGS_ATTRIBUTES['I3D_lod3']['defaultValue'],
    )


def __init__(self):
    self.filepath = \
        bpy.context.scene.I3D_UIexportSettings.I3D_exportFileLocation


def draw(self, context):
    layout = self.layout
    # -----------------------------------------
    # "Export Selected" box
    box = layout.box()
    row = box.row()
    row.prop(self, "I3D_exportSelected")
    # ----------------------------------------
    # "Export Options" box
    box = layout.box()
    row = box.row()
    # expand button for "Export Options"
    row.prop(context.scene.I3D_UIexportSettings, "UI_exportOptions",
             icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_exportOptions
             else
             'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if context.scene.I3D_UIexportSettings.UI_exportOptions:
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportIK")
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportAnimation")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportShapes")
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportNurbsCurves")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportLights")
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportCameras")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportParticleSystems")
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportUserAttributes")
    # -----------------------------------------
    # "Shape Export Subparts" box
    box = layout.box()
    row = box.row()
    # expand button for "Shape Export Subparts"
    row.prop(context.scene.I3D_UIexportSettings,
             "UI_shapeExportSubparts", icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_shapeExportSubparts
             else
             'TRIA_RIGHT', icon_only=True, emboss=False)
    if context.scene.I3D_UIexportSettings.UI_shapeExportSubparts:
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportNormals")
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportTexCoords")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportColors")
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportSkinWeigths")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportMergeGroups")
    # -----------------------------------------
    # "Miscellaneous" box
    box = layout.box()
    row = box.row()
    # expand button for "Miscellaneous"
    row.prop(context.scene.I3D_UIexportSettings, "UI_miscellaneous",
             icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_miscellaneous
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    if context.scene.I3D_UIexportSettings.UI_miscellaneous:
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportVerbose")
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportRelativePaths")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportApplyModifiers")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportAxisOrientations")
    # -----------------------------------------


def execute(self, context):
    bpy.context.scene.I3D_UIexportSettings.I3D_exportUseSoftwareFileName\
         = False
    bpy.context.scene.I3D_UIexportSettings.I3D_exportFileLocation = \
        self.filepath
    if (self.I3D_exportSelected):
        io_export_i3d.i3d_export.I3DExportSelected()
    else:
        io_export_i3d.i3d_export.I3DExportAll()
    return {'FINISHED'}


def fileExportMenuItem(self, context):
    self.layout.operator(I3D_FileExport.bl_idname, text="GIANTS I3D (.i3d)")
# -----------------------------------------------------------------------------
#   Properties Panel
# -----------------------------------------------------------------------------


class I3D_PanelExportView:
    bl_label = "GIANTS I3D Exporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "i3d_panel_export"
    bl_category = "scene"


def draw(self, context):
    layout = self.layout
    layout.prop(
        context.scene.I3D_UIexportSettings, "UI_settingsMode", expand=True)
    # -----------------------------------------
    # "Export" tab
    if 'exp' == context.scene.I3D_UIexportSettings.UI_settingsMode:
        # -----------------------------------------
        # "Export Options" box
        box = layout.box()
    row = box.row()
    # expand button for "Export Options"
    row.prop(context.scene.I3D_UIexportSettings, "UI_exportOptions",
             icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_exportOptions
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if context.scene.I3D_UIexportSettings.UI_exportOptions:
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportIK")
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportAnimation")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportShapes")
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportNurbsCurves")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportLights")
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportCameras")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportParticleSystems")
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportUserAttributes")
    # -----------------------------------------
    # "Shape Export Subparts" box
    box = layout.box()
    row = box.row()
    # expand button for "Shape Export Subparts"
    row.prop(context.scene.I3D_UIexportSettings,
             "UI_shapeExportSubparts", icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_shapeExportSubparts
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    if context.scene.I3D_UIexportSettings.UI_shapeExportSubparts:
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportNormals")
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportTexCoords")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportColors")
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportSkinWeigths")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportMergeGroups")
    # -----------------------------------------
    # "Miscellaneous" box
    box = layout.box()
    row = box.row()
    # expand button for "Miscellaneous"
    row.prop(context.scene.I3D_UIexportSettings, "UI_miscellaneous",
             icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_miscellaneous
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    if context.scene.I3D_UIexportSettings.UI_miscellaneous:
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportVerbose")
        row.prop(context.scene.I3D_UIexportSettings, "I3D_exportRelativePaths")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportApplyModifiers")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportAxisOrientations")
    # -----------------------------------------
    # "Output File" box
    box = layout.box()
    row = box.row()
    # expand button for "Output File"
    row.prop(context.scene.I3D_UIexportSettings, "UI_outputFile",
             icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_outputFile
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    if context.scene.I3D_UIexportSettings.UI_outputFile:
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportUseSoftwareFileName")
        row = box.row()
        row.enabled = \
            not context.scene.I3D_UIexportSettings.\
            I3D_exportUseSoftwareFileName
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_exportFileLocation")
    # -----------------------------------------
    row = layout.row(align=True)
    row.operator("i3d.panel_export_do", text="Export All").state = 1
    row.operator("i3d.panel_export_do", text="Export Selected").state = 2
    # -----------------------------------------
    # TODO Check "Attributes tab" elif
    # "Attributes" tab
    if 'attr' == context.scene.I3D_UIexportSettings.UI_settingsMode:
        # -----------------------------------------
        # "Current Node" box
        box = layout.box()
        row = box.row()
    # expand button for "Current Node"
    row.prop(context.scene.I3D_UIexportSettings, "UI_currentNode",
             icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_currentNode
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if context.scene.I3D_UIexportSettings.UI_currentNode:
        row = box.row()
        row.enabled = False
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_nodeName", text="Loaded Node")
        row = box.row()
        row.enabled = False
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_nodeIndex", text="Node Index")
    # -----------------------------------------
    # "Rigid Body" box
    box = layout.box()
    row = box.row()
    # expand button for "Rigid Body"
    row.prop(context.scene.I3D_UIexportSettings, "UI_rigidBody",
             icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_rigidBody
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if context.scene.I3D_UIexportSettings.UI_rigidBody:
        col = box.column()
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_static", text="Static")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_kinematic", text="Kinematic")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_dynamic", text="Dynamic")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_compound", text="Compound")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_compoundChild", text="Compound Child")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_collision", text="Collision")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_collisionMask", text="Collision Mask")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_restitution", text="Restitution")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_staticFriction", text="Static Friction")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_dynamicFriction", text="Dynamic Friction")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_linearDamping", text="Linear Damping")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_angularDamping", text="Angular Damping")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_density", text="Density")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_solverIterationCount", text="Solve Iterations")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_ccd", text="Continues Collision Detection")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_trigger", text="Trigger")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_splitType", text="Split Type")
        row = col.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_splitMinU", text="Split Min U")
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_splitMaxU", text="Split Max U")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_splitMinV", text="Split Min V")
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_splitMaxV", text="Split Max V")
        row = box.row()
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_splitUvWorldScale", text="Split UV's worldScale")
    # -----------------------------------------
    # "Joint" box
    box = layout.box()
    row = box.row()
    # expand button for "Joint"
    row.prop(context.scene.I3D_UIexportSettings, "UI_joint", icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_joint
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if context.scene.I3D_UIexportSettings.UI_joint:
        col = box.column()
        col.prop(context.scene.I3D_UIexportSettings, "I3D_joint", text="Joint")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_projection", text="Projection")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_projDistance", text="Projection Distance")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_projAngle", text="Projection Angle")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_xAxisDrive", text="X-Axis Drive")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_yAxisDrive", text="Y-Axis Drive")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_zAxisDrive", text="Z-Axis Drive")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_drivePos", text="Drive Position")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_driveForceLimit", text="Drive Force Limit")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_driveSpring", text="Drive Spring")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_driveDamping", text="Drive Damping")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_breakableJoint", text="Breakable")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_jointBreakForce", text="Break Force")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_jointBreakTorque", text="Break Torque")
    # -----------------------------------------
    # "Rendering" box
    box = layout.box()
    row = box.row()
    # expand button for "Rendering"
    row.prop(context.scene.I3D_UIexportSettings, "UI_rendering",
             icon='TRIA_DOWN'
             if context.scene.I3D_UIexportSettings.UI_rendering
             else 'TRIA_RIGHT', icon_only=True, emboss=False)
    # expanded view
    if context.scene.I3D_UIexportSettings.UI_rendering:
        col = box.column()
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_oc", text="Occlusion Culling")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_castsShadows", text="Casts Shadows")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_receiveShadows", text="Receive Shadows")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_nonRenderable", text="Non Renderable")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_clipDistance", text="Clip Distance")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_objectMask", text="Object Mask")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_lightMask", text="Light Mask (Hex)")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_decalLayer", text="Decal Layer")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_mergeGroup", text="Merge Group")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_mergeGroupRoot", text="Merge Group Root")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_boundingVolume", text="Bounding Volume")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_cpuMesh", text="CPU Mesh")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_lod", text="LOD")
        row = col.row()
        row.enabled = False
        row.prop(context.scene.I3D_UIexportSettings,
                 "I3D_lod0", text="Child 0 Distance")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_lod1", text="Child 1 Distance")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_lod2", text="Child 2 Distance")
        col.prop(context.scene.I3D_UIexportSettings,
                 "I3D_lod3", text="Child 3 Distance")
    # -----------------------------------------
    row = layout.row(align=True)
    row.operator("i3d.panel_export_attr", text="Load Current").state = 1
    row.operator("i3d.panel_export_attr", text="Save Current").state = 2
    row.operator("i3d.panel_export_attr", text="Remove Current").state = 3
    row = layout.row(align=True)
    row.operator("i3d.panel_export_attr", text="Apply Selected").state = 4
    row.operator("i3d.panel_export_attr", text="Remove Selected").state = 5
    # -----------------------------------------
    row = layout.row()
    row.operator("i3d.panel_export_close", icon='X')
# -----------------------------------------------------------------------------
#   Pannel Buttons
# -----------------------------------------------------------------------------


class I3D_PanelExport_ButtonAttr(bpy.types.Operator):
    bl_idname = "i3d.panel_export_attr"
    bl_label = "Attributes"
    state = bpy.props.IntProperty()

    def execute(self, context):
        if 1 == self.state:
            dcc.I3DLoadObjectAttributes()
        elif 2 == self.state:
            dcc.I3DSaveObjectAttributes()
        elif 3 == self.state:
            dcc.I3DRemoveObjectAttributes()
        elif 4 == self.state:
            dcc.I3DApplySelectedAttributes()
        elif 5 == self.state:
            dcc.I3DRemoveSelectedAttributes()
        return {'FINISHED'}


class I3D_PanelExport_ButtonExport(bpy.types.Operator):
    bl_idname = "i3d.panel_export_do"
    bl_label = "Export"
    state = bpy.props.IntProperty()

    def execute(self, context):
        if 1 == self.state:
            io_export_i3d.i3d_export.I3DExportAll()
        elif 2 == self.state:
            io_export_i3d.i3d_export.I3DExportSelected()
        return {'FINISHED'}
# ------------------------------------------------------------------------------
#   I3D Menu Item
# ------------------------------------------------------------------------------


class I3D_MenuExport(bpy.types.Operator):
    bl_label = "I3D Exporter"
    bl_idname = "i3d.menu_export"

    def execute(self, context):
        try:
            bpy.utils.register_class(I3D_PanelExport)
            bpy.utils.register_class(I3D_PanelExport_ButtonClose)
            bpy.utils.register_class(I3D_PanelExport_ButtonExport)
            bpy.utils.register_class(I3D_PanelExport_ButtonAttr)
        except:
            pass
        return {'FINISHED'}

class I3D_PanelExport_ButtonClose(bpy.types.Operator):
    bl_idname = "i3d.panel_export_close"
    bl_label = "Close"

    def execute(self, context):
        bpy.utils.unregister_class(I3D_PanelExport)
        bpy.utils.unregister_class(I3D_PanelExport_ButtonClose)
        bpy.utils.unregister_class(I3D_PanelExport_ButtonExport)
        bpy.utils.unregister_class(I3D_PanelExport_ButtonAttr)
        return {'FINISHED'}

# -----------------------------------------------------------------------------
#   Init Scene PropertyGroups
# -----------------------------------------------------------------------------

    @classmethod
    def register(cls):
        bpy.types.Scene.I3D_UIexportSettings = bpy.props.PointerProperty(
            name="I3D UI Export Settings",
            type=cls,
            description="I3D UI Export Settings"
        )

    @classmethod
    def unregister(cls):
        if bpy.context.scene.get('I3D_UIexportSettings'):
            del bpy.context.scene['I3D_UIexportSettings']
        try:
            del bpy.types.Scene.I3D_UIexportSettings

        except:
            pass
# -----------------------------------------------------------------------------
#   Register
# -----------------------------------------------------------------------------


def register():
    bpy.utils.register_class(I3D_UIexportSettings)
    # --------------------------------------------------------------------------
    bpy.utils.register_class(I3D_MenuExport)
    # --------------------------------------------------------------------------
    bpy.utils.register_class(I3D_FileExport)
    bpy.types.INFO_MT_file_export.append(fileExportMenuItem)


def unregister():
    bpy.utils.unregister_class(I3D_MenuExport)
    bpy.utils.unregister_class(I3D_UIexportSettings)
    # --------------------------------------------------------------------------
    try:
        bpy.utils.unregister_class(I3D_PanelExport)
        bpy.utils.unregister_class(I3D_PanelExport_ButtonClose)
        bpy.utils.unregister_class(I3D_PanelExport_ButtonExport)
        bpy.utils.unregister_class(I3D_PanelExport_ButtonAttr)
    except:
        pass
    # --------------------------------------------------------------------------
    bpy.utils.unregister_class(I3D_FileExport)
    bpy.types.INFO_MT_file_export.remove(fileExportMenuItem)


if __name__ == "__main__":
    register()