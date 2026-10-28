"""T1 one-shot - red crayon -> flag patch on soldier A's sleeve -> pull straight back out to the salute.

6.0 s @ 25 fps = 150 frames. One continuous camera, no cut.
  f1-40    (0.0-1.6 s)  macro on the patch's red hoist bar, frame filled with red thread, drifting UP 6 mm
                        (matches the crayon move at the end of shot_1). The crayon texture becomes thread here.
  f40-110  (1.6-4.4 s)  continuous pull-back straight out of the sleeve along the line to the salute camera;
                        lens widens 100 -> 35 mm; lands exactly on the locked salute frame.
  f110-150 (4.4-6.0 s)  holds the salute frame; gentle handheld blends in.
The patch is on soldier A's RIGHT upper sleeve (his saluting arm), on the side facing the camera:
from behind-right his left arm is hidden by his body.
"""
import importlib
import os
import sys

import bpy  # noqa: F401  (loads mathutils when run as the pip bpy module)
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uae_set as S  # noqa: E402
importlib.reload(S)

scene = S.reset_scene(150)
joints = S.build_salute_set()
JA = joints['soldier_A']
cam_end = Vector(S.SALUTE_CAM)
patch, P, n, front = S.sleeve_patch('patch_A', S.COL_A, JA, side='r', facing=cam_end - JA['shoulder_r'])

rig, cam = S.camera_rig('cam_t1_patch_to_salute', 100.0)

# Red hoist bar = front quarter of the patch. The camera starts on the line to the salute camera,
# so the pull-back is one straight move out of the sleeve.
red = P + front * 0.031
start = red + (cam_end - red).normalized() * 0.05     # 100 mm at 5 cm -> frame 1.8 cm wide: only red thread
# Drift 6 mm along the red bar (the arm axis), in the direction that reads as UP on screen,
# so the frame stays all red while it matches the crayon move.
up = (red - start).to_track_quat('-Z', 'Y') @ Vector((0, 1, 0))
along_bar = (JA['shoulder_r'] - JA['elbow_r']).normalized()
drift = along_bar * (0.006 if along_bar.dot(up) > 0 else -0.006)
S.key_rig(rig, 1, start, red)
S.key_rig(rig, 40, start + drift, red + drift)
S.key_rig(rig, 110, cam_end, S.SALUTE_AIM)
S.key_rig(rig, 150, cam_end, S.SALUTE_AIM)
S.set_interp(rig, 'BEZIER')

for f, lens in ((1, 100.0), (40, 100.0), (110, S.SALUTE_LENS), (150, S.SALUTE_LENS)):
    cam.data.lens = lens
    cam.data.keyframe_insert('lens', frame=f)
S.set_interp(cam.data, 'BEZIER')
S.handheld(cam, start=110, blend_in=25)              # no shake during the macro or the pull-back

S.key_outlines(scene, cam, list(range(1, 151, 3)) + [150])
S.save_blend(__file__, 't1_patch_to_salute')
