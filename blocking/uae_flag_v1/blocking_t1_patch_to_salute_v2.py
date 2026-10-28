"""T1 one-shot v2 - red crayon -> flag patch on soldier A's hanging sleeve -> pull back while they raise the salute.

6.0 s @ 25 fps = 150 frames. One continuous camera, no cut.
  f1-40    (0.0-1.6 s)  grazing macro just above soldier A's right sleeve patch, looking down along the arm:
                        black stitched border down frame left, red bar filling the frame and receding to the top,
                        green/white/black stripes far at top right (the director's reference frame).
                        Camera drifts UP 6 mm with the red (matches the crayon move at the end of shot_1).
  f40-110  (1.6-4.4 s)  continuous pull-back and tilt-up out of the sleeve, lens widening 100 -> 35 mm,
                        landing exactly on the locked salute frame.
  f70-88   (2.8-3.5 s)  while the camera is pulling back, all four soldiers raise the salute together.
  f110-150 (4.4-6.0 s)  holds the salute frame; gentle handheld blends in.
All four start at attention, arms by their sides, already looking up at the flag.
"""
import importlib
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uae_set as S  # noqa: E402
importlib.reload(S)

RAISE = (70, 88)
PULL = (40, 110)

scene = S.reset_scene(150)
joints = S.build_salute_set(raise_frames=RAISE)
JA = joints['soldier_A']

# Patch on the outer side of A's right sleeve; it rides on the upper arm when the salute comes up.
patch, P, n, front = S.sleeve_patch('patch_A', S.COL_A, JA, side='r')
upper = bpy.data.objects['soldier_A_upperarm_r']
bpy.context.view_layer.update()
patch.parent = upper
patch.matrix_parent_inverse = upper.matrix_world.inverted()

rig, cam = S.camera_rig('cam_t1_patch_to_salute_v2', 100.0)
rig.rotation_mode = 'QUATERNION'

# Opening: grazing view down along the hanging arm, 37 deg off the patch surface, screen-up = away from
# the sleeve, so the soldier's front (hoist edge, black border) is frame left and the stripes recede top right.
arm_down = (JA['elbow_r'] - JA['shoulder_r']).normalized()
focus = P + front * 0.032                               # red bar, black border just inside frame left
view = (arm_down * 0.8 - n * 0.6).normalized()
start = focus - view * 0.07                             # 100 mm at 7 cm -> frame 2.5 cm wide
q_start = S.look_quat(start, focus, n)
screen_up = q_start @ Vector((0, 1, 0))
drift = screen_up * 0.006                               # 6 mm up with the red


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
S.save_blend(__file__, 't1_patch_to_salute', version=2)
