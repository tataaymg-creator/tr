"""T1 bridge - red crayon -> UAE flag patch on soldier A's sleeve, then pull-back.

3.0 s @ 25 fps = 75 frames. 100 mm macro.
  f1-40  (0.0-1.6 s)  low raking macro filled by the patch's red hoist bar (front quarter of the patch),
                      slow 6 mm upward drift only - this is where the crayon texture becomes thread.
  f40-75 (1.6-3.0 s)  continuous pull-back with a slight rise, ends medium close on the patch + shoulder.
Soldier A stands at attention, faces +Y. Patch on the LEFT upper sleeve (verify against a real reference).
"""
import importlib
import os
import sys

import bpy  # noqa: F401  (loads mathutils when run as the pip bpy module)
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uae_set as S  # noqa: E402
importlib.reload(S)

scene = S.reset_scene(75)
S.ground()

soldier, J = S.build_figure('soldier_A', S.COL_A, S.POSE_ATTENTION)
patch, P, n, front = S.sleeve_patch('patch_A', S.COL_A, J, side='l')

# Palms behind the soldier on the camera's side of frame (background bokeh only).
bm = S.bmesh.new()
for x, y, h in ((6.0, 9.0, 7.5), (7.5, 4.0, 8.5), (8.0, -2.0, 7.0), (7.0, -7.0, 8.0)):
    S.palm(bm, (x, y, 0), h)
S.outline(S._new_object('palms', bm), S.COL_SET, S.PX_SET)

rig, cam = S.camera_rig('cam_t1_patch', 100.0)

# Red hoist bar = front quarter of the patch (UAE flag proportion). Low raking: camera below the sleeve, 50 deg off the normal.
red = P + front * 0.031
rake = (n * 0.64 + Vector((0, 0, -0.77))).normalized()
start = red + rake * 0.055                      # 100 mm at 5.5 cm -> frame 2 cm wide: only red thread in frame
S.key_rig(rig, 1, start, red)
drift = Vector((0, 0, 0.006))                   # 6 mm drift along the stitch direction keeps the frame all red
S.key_rig(rig, 40, start + drift, red + drift)
pull = (n * 0.97 + Vector((0, 0, -0.10)) - front * 0.12).normalized()
end_aim = P + Vector((0, 0, 0.05))              # patch just below centre, top of the shoulder in frame
S.key_rig(rig, 75, end_aim + pull * 1.25, end_aim)  # 1.25 m -> frame 0.45 x 0.25 m
S.set_interp(rig, 'BEZIER')
# Slider move, no handheld: noise at 11 cm would read as a shake, and the look is dreamy/smooth.

S.key_outlines(scene, cam, list(range(1, 76, 3)) + [75])
S.save_blend(__file__, 't1_patch_pullback')
