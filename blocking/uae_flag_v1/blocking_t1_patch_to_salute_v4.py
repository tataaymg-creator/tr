"""T1 one-shot v4 - straight-on stitch still -> move up -> straight pull-back -> salute. Camera always level.

6.0 s @ 25 fps = 150 frames. One continuous camera, no cut.
  f1-30    (0.0-1.2 s)  straight-on macro on the red bar of soldier A's right sleeve patch (the director's
                        stitch still: vertical stitches, red edge to edge). Camera moves UP 6 mm along the stitches.
  f30-70   (1.2-2.8 s)  pulls back out from the patch, curving gently toward the salute side: patch -> arm -> soldier A.
  f70-110  (2.8-4.4 s)  keeps backing away, panning one way onto the row, landing exactly on the locked salute frame.
  f80-98   (3.2-3.9 s)  all four raise the salute together (after the move up, camera already well away).
  f110-150 (4.4-6.0 s)  holds the salute frame; gentle handheld blends in.
Rig: CAM_move (position) + CAM_aim (look-at target). Track To with world-Z up, so the camera never rolls.
Few keys on each: grab either empty to adjust the move.
"""
import importlib
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uae_set as S  # noqa: E402
importlib.reload(S)

RAISE = (80, 98)

scene = S.reset_scene(150)
joints = S.build_salute_set(raise_frames=RAISE)
JA = joints['soldier_A']

# Patch on the outer side of A's right sleeve (arm hanging at attention); it rides up with the salute.
patch, P, n, front = S.sleeve_patch('patch_A', S.COL_A, JA, side='r', along=0.40)
upper = bpy.data.objects['soldier_A_upperarm_r']
bpy.context.view_layer.update()
patch.parent = upper
patch.matrix_parent_inverse = upper.matrix_world.inverted()

rig, cam = S.camera_rig('cam_t1_patch_to_salute_v4', 100.0)
rig.name = 'CAM_move'
rig.empty_display_type = 'ARROWS'
rig.empty_display_size = 0.15
aim = bpy.data.objects.new('CAM_aim', None)
scene.collection.objects.link(aim)
aim.empty_display_type = 'SPHERE'
aim.empty_display_size = 0.08
con = rig.constraints.new('TRACK_TO')
con.target = aim
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'

red = P + front * 0.031                       # centre of the red hoist bar
n_flat = Vector((n.x, n.y, 0.0)).normalized()  # straight-on, level
up = Vector((0.0, 0.0, 0.006))                # 6 mm move up along the vertical stitches
reveal = red + Vector((0.0, 0.0, 0.05))       # aim holds on the patch until f70
back = Vector((0.0, -1.0, 0.0))               # toward the salute camera side (behind the row)

FRAMES = (1, 30, 70, 110, 150)
CAM = (red + n_flat * 0.05, red + n_flat * 0.05 + up,
       reveal + n_flat * 0.75 + back * 0.45,   # pulled back ~0.9 m, already curving toward the salute side
       Vector(S.SALUTE_CAM), Vector(S.SALUTE_CAM))
AIM = (red, red + up, reveal, Vector(S.SALUTE_AIM), Vector(S.SALUTE_AIM))
LENS = (100.0, 100.0, 60.0, S.SALUTE_LENS, S.SALUTE_LENS)   # 100 mm at 5 cm: frame 1.8 cm, red only
creep = up / 29.0                             # already moving up on frame 1, like the crayon
CAM_TAN = (creep, creep, (CAM[3] - CAM[1]) / 80.0 * 0.4, Vector(), Vector())
AIM_TAN = (creep, creep, Vector(), Vector(), Vector())      # aim leaves the patch from rest at f70


def key_path(idb, path, values, tangents):
    """Keys with FREE handles from one shared 3D tangent per key, so every channel follows
    the same timing and the move is the planned spatial curve (no per-axis drift)."""
    for f, v in zip(FRAMES, values):
        setattr(idb, path, v)
        idb.keyframe_insert(path, frame=f)
    for fc in S.fcurves_of(idb):
        if fc.data_path != path:
            continue
        kps = fc.keyframe_points
        for i, kp in enumerate(kps):
            kp.interpolation = 'BEZIER'
            kp.handle_left_type = kp.handle_right_type = 'FREE'
            t, val = kp.co
            tan = tangents[i][fc.array_index] if isinstance(tangents[i], Vector) else tangents[i]
            dl = (t - kps[i - 1].co[0]) / 3.0 if i > 0 else 1.0
            dr = (kps[i + 1].co[0] - t) / 3.0 if i < len(kps) - 1 else 1.0
            kp.handle_left = (t - dl, val - tan * dl)
            kp.handle_right = (t + dr, val + tan * dr)


key_path(rig, 'location', CAM, CAM_TAN)
key_path(aim, 'location', AIM, AIM_TAN)
key_path(cam.data, 'lens', LENS, (0.0,) * 5)

S.handheld(cam, start=110, blend_in=20)       # nothing but the planned move until the salute frame

S.key_outlines(scene, cam, list(range(1, 151, 3)) + [150])
S.save_blend(__file__, 't1_patch_to_salute', version=4)
