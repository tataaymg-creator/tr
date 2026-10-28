"""T1 one-shot v3 - red crayon -> flag patch on soldier A's hanging sleeve -> pull back while they raise the salute.

6.0 s @ 25 fps = 150 frames. One continuous camera, no cut.
  f1-40    (0.0-1.6 s)  grazing macro just BELOW soldier A's right sleeve patch, looking UP along the arm
                        (the director's corrected reference): black stitched border down frame right, red bar
                        receding to the top, stripes at top left - green farthest, white, black nearest.
                        Camera pushes 5 mm up along the red bar toward the shoulder (the director's arrow).
  f40-110  (1.6-4.4 s)  continuous pull-back and tilt-up out of the sleeve, lens widening 100 -> 35 mm,
                        landing exactly on the locked salute frame.
  f70-88   (2.8-3.5 s)  while the camera is pulling back, all four soldiers raise the salute together.
  f110-150 (4.4-6.0 s)  holds the salute frame; gentle handheld blends in.
All four start at attention, arms by their sides, already looking up at the flag.
Patch per the real UAE uniform reference: right upper sleeve, reversed flag - red hoist bar toward the
soldier's front, green on top.
"""
import importlib
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uae_set as S  # noqa: E402
importlib.reload(S)

RAISE = (70, 88)
# Opening angle solved against the director's corrected reference frame (black border x 0.84-0.87,
# red|stripes edge x 0.48 at the top and meeting frame left 63% down, patch top just at the top edge):
# grazing 8 deg off the sleeve, turned 10 deg toward the soldier's back, rolled 20 deg, 5 cm from the thread.
FOCUS_FRONT, FOCUS_UP, DIST = 0.036, 0.005, 0.05
GRAZE, YAW, ROLL = 8.0, 10.0, 20.0
PULL = (40, 110)

scene = S.reset_scene(150)
joints = S.build_salute_set(raise_frames=RAISE)
JA = joints['soldier_A']

# Patch on the outer side of A's right sleeve; it rides on the upper arm when the salute comes up.
patch, P, n, front = S.sleeve_patch('patch_A', S.COL_A, JA, side='r', along=0.40)
upper = bpy.data.objects['soldier_A_upperarm_r']
bpy.context.view_layer.update()
patch.parent = upper
patch.matrix_parent_inverse = upper.matrix_world.inverted()

rig, cam = S.camera_rig('cam_t1_patch_to_salute_v3', 100.0)
rig.rotation_mode = 'QUATERNION'

# Opening: grazing view UP along the hanging arm from below the patch, screen-up = away from the sleeve. Soldier's front (red hoist bar, black border) is frame right; the flag's
# top (green) is toward the shoulder, so the stripes recede top left.
arm_up = (JA['shoulder_r'] - JA['elbow_r']).normalized()
focus = P + front * FOCUS_FRONT + arm_up * FOCUS_UP     # red bar, black border just inside frame right
along = arm_up * math.cos(math.radians(YAW)) - front * math.sin(math.radians(YAW))
view = (along * math.cos(math.radians(GRAZE)) - n * math.sin(math.radians(GRAZE))).normalized()
start = focus - view * DIST                             # 100 mm at 5 cm -> frame 1.8 cm wide
q_start = S.look_quat(start, focus, Matrix.Rotation(math.radians(ROLL), 3, view) @ n)
drift = arm_up * 0.005                                  # push 5 mm up along the red bar, toward the shoulder


def key(frame, pos, quat, lens):
    rig.location = pos
    rig.rotation_quaternion = quat
    rig.keyframe_insert('location', frame=frame)
    rig.keyframe_insert('rotation_quaternion', frame=frame)
    cam.data.lens = lens
    cam.data.keyframe_insert('lens', frame=frame)


key(1, start, q_start, 100.0)
key(PULL[0], start + drift, q_start, 100.0)

# Pull-back: straight line out to the salute camera, orientation slerped, all eased with one smootherstep,
# keyed on every frame so the path is exactly this curve.
p0 = start + drift
p1 = Vector(S.SALUTE_CAM)
q1 = S.look_quat(p1, S.SALUTE_AIM)
if q_start.dot(q1) < 0:
    q1.negate()
for f in range(PULL[0] + 1, PULL[1] + 1):
    t = (f - PULL[0]) / (PULL[1] - PULL[0])
    s = t * t * t * (t * (6 * t - 15) + 10)
    key(f, p0.lerp(p1, s), q_start.slerp(q1, s), 100.0 + (S.SALUTE_LENS - 100.0) * s)
key(150, p1, q1, S.SALUTE_LENS)

S.set_interp(rig, 'LINEAR')
S.set_interp(cam.data, 'LINEAR')
for idb in (rig, cam.data):                             # ease the opening drift only
    for fc in S.fcurves_of(idb):
        fc.keyframe_points[0].interpolation = 'BEZIER'
S.handheld(cam, start=PULL[1], blend_in=25)             # no shake during the macro or the pull-back

S.key_outlines(scene, cam, list(range(1, 151, 3)) + [150])
S.save_blend(__file__, 't1_patch_to_salute', version=3)
