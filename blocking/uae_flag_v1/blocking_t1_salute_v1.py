"""T1 world shot - four soldiers salute the UAE flag, seen from behind three-quarter (hard cut after the bridge).

4.0 s @ 25 fps = 100 frames. 35 mm, low (1.0 m), gentle handheld, slow push-in.
Row along X at Y = 0, all facing +Y toward the flagpole. Left to right on screen: D, C, B, A.
Soldier A (rightmost, nearest camera) is the patch soldier from the bridge.
Flag flies toward +X from a 7 m pole, upper middle of frame, against the sky.
Frame 1 is the composition the director locked (S.SALUTE_CAM / S.SALUTE_AIM).
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uae_set as S  # noqa: E402
importlib.reload(S)

scene = S.reset_scene(100)
S.build_salute_set()

rig, cam = S.camera_rig('cam_t1_salute', S.SALUTE_LENS)
S.key_rig(rig, 1, S.SALUTE_CAM, S.SALUTE_AIM)
S.key_rig(rig, 100, (3.1, -3.9, 1.0), S.SALUTE_AIM)
S.set_interp(rig, 'BEZIER')
S.handheld(cam)

S.key_outlines(scene, cam, [1, 25, 50, 75, 100])
S.save_blend(__file__, 't1_salute')
