import sys
import os
import bpy

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
    sys.path.append(blend_dir)

from addons.io_export_i3d import  io_export_i3d
from importlib import reload
reload(io_export_i3d)
i3d_ui.main()
