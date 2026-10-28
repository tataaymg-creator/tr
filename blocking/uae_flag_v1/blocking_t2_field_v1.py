"""T2 world shot - green crayon rows -> vegetable field rows (composition matched to shot_2).

4.0 s @ 25 fps = 100 frames. 35 mm, camera 0.30 m above the soil, slow forward glide 0.6 m (slider, no handheld).
Crop rows run side to side (along X); camera looks +Y across them, like the horizontal crayon strokes.
Horizon sits ~8% from the top edge (the paper's back edge in shot_2): pitch down 13.7 deg.
One tall date palm on the horizon at ~40% from frame left, where the crayon tip was.
"""
import importlib
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uae_set as S  # noqa: E402
importlib.reload(S)

scene = S.reset_scene(100)
S.ground(800.0)

LENS, CAM_Z, Y0 = 35.0, 0.30, -0.5
HALF_H = math.atan(S.SENSOR / 2 / LENS)                      # horizontal half-FOV
HALF_V = math.atan(S.SENSOR * 9 / 16 / 2 / LENS)             # vertical half-FOV
PITCH = math.atan(0.84 * math.tan(HALF_V))                    # horizon 8% from top = 0.84 above centre

# Raised soil ridges every 0.8 m out to 60 m; plants on them out to 25 m, only where the lens can see.
ridges, plants = S.bmesh.new(), S.bmesh.new()
y = 0.2
while y < 60.0:
    S.add_box(ridges, (0.0, y, 0.06), (80.0, 0.35, 0.12))
    if y < 25.0:
        half_w = (y - Y0) * math.tan(HALF_H) + 1.0
        x = -half_w
        while x < half_w:
            S.add_icosphere(plants, (x, y, 0.20), 0.09)
            x += 0.35
    y += 0.8
S.outline(S._new_object('ridges', ridges), S.COL_SET, S.PX_SET)
S.outline(S._new_object('plants', plants), S.COL_SET, S.PX_SET)

# Hero palm at ~40% from frame left on the horizon, plus a seeded line of palms along the far edge.
hero_x = -60.0 * 0.2 * math.tan(HALF_H)
bm = S.bmesh.new()
S.palm(bm, (hero_x, 60.0, 0.0), 12.0)
rng = S.random.Random(S.SEED)
for k in range(14):
    S.palm(bm, (-45.0 + k * 7.0 + rng.uniform(-2, 2), 75.0 + rng.uniform(0, 20), 0.0),
           rng.uniform(8.0, 12.0), rng.uniform(0, 5), rng.uniform(0, 360), rng)
S.outline(S._new_object('palms', bm), S.COL_SET, S.PX_SET)

rig, cam = S.camera_rig('cam_t2_field', LENS)
for f, y_cam in ((1, Y0), (100, Y0 + 0.6)):
    S.key_rig(rig, f, (0.0, y_cam, CAM_Z), (0.0, y_cam + math.cos(PITCH), CAM_Z - math.sin(PITCH)))
S.set_interp(rig, 'BEZIER')

S.key_outlines(scene, cam, [1, 50, 100])
S.save_blend(__file__, 't2_field')
