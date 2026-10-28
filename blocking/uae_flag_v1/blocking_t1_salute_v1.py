"""T1 world shot - four soldiers salute the UAE flag, seen from behind three-quarter (hard cut after the bridge).

4.0 s @ 25 fps = 100 frames. 35 mm, low (1.0 m), gentle handheld, slow push-in.
Row along X at Y = 0, all facing +Y toward the flagpole. Left to right on screen: D, C, B, A.
Soldier A (rightmost, nearest camera) is the patch soldier from the bridge.
Flag flies toward +X from a 7 m pole, upper left of frame, against the sky.
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uae_set as S  # noqa: E402
importlib.reload(S)

scene = S.reset_scene(100)
S.ground()

for name, col, x in (('soldier_D', S.COL_D, -1.5), ('soldier_C', S.COL_C, -0.5),
                     ('soldier_B', S.COL_B, 0.5), ('soldier_A', S.COL_A, 1.5)):
    S.build_figure(name, col, S.POSE_SALUTE, loc=(x, 0.0, 0.0))

# Flagpole + flag (flag is a flat board; it flies toward +X so the camera sees it broad).
POLE = (-3.0, 9.0)
bm = S.bmesh.new()
S.add_capsule(bm, (POLE[0], POLE[1], 0.0), (POLE[0], POLE[1], 7.0), 0.06, segs=10)
S.add_ellipsoid(bm, (POLE[0], POLE[1], 7.1), (0.1, 0.1, 0.1), segs=10, rings=6)
S.outline(S._new_object('flagpole', bm), S.COL_SET, S.PX_SET)
bm = S.bmesh.new()
S.add_box(bm, (POLE[0] + 0.95, POLE[1], 6.45), (1.8, 0.03, 0.9))
S.outline(S._new_object('flag', bm), S.COL_SET, S.PX_SET)

# Date palms behind the flag, seeded so every take is the same.
rng = S.random.Random(S.SEED)
bm = S.bmesh.new()
for k in range(9):
    S.palm(bm, (-14.0 + k * 3.6 + rng.uniform(-1, 1), 22.0 + rng.uniform(-3, 5), 0.0),
           rng.uniform(7.0, 10.0), rng.uniform(0, 6), rng.uniform(0, 360), rng)
S.outline(S._new_object('palms', bm), S.COL_SET, S.PX_SET)

rig, cam = S.camera_rig('cam_t1_salute', 35.0)
S.key_rig(rig, 1, (3.6, -4.6, 1.0), (-1.4, 3.0, 2.4))
S.key_rig(rig, 100, (3.1, -3.9, 1.0), (-1.4, 3.0, 2.4))
S.set_interp(rig, 'BEZIER')
S.handheld(cam)

S.key_outlines(scene, cam, [1, 25, 50, 75, 100])
S.save_blend(__file__, 't1_salute')
