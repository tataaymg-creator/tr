# UAE Flag Day – blocking v1 (AI transition shots)

Geometry only: who is where, which way they face, where the camera is, and how it moves. Look, faces, wardrobe and light come from the image references.

All shots are 16:9, 1280×720, **25 fps** (matching the live-action crayon plates), with a 36 mm horizontal sensor. Units are metres, Z is up, and the floor is at Z = 0.

| File | Shot | Length | Lens | Camera |
|---|---|---|---|---|
| **`blocking_t1_patch_to_salute_v1.blend`** | **T1 as one shot: red crayon → flag patch on soldier A's sleeve → pull straight back out to the salute. Replaces the bridge + hard cut.** | 6.0 s / 150 f | 100 → 35 mm | f1–40: macro filled by the red hoist bar, drifting up 6 mm along the bar (matches the crayon move). f40–110: one continuous pull-back straight out of the sleeve along the line to the salute camera, lens widening to 35 mm, landing exactly on the locked salute frame. f110–150: holds that frame; gentle handheld blends in. No cut. |
| `blocking_t1_patch_pullback_v1.blend` | Superseded by the one-shot. T1 bridge: red crayon → flag patch → pull-back | 3.0 s / 75 f | 100 mm | f1–40: low raking macro holding on the red hoist bar, 6 mm upward drift. f40–75: continuous pull-back with a slight rise to a medium close-up of the patch and shoulder. Slider, no handheld. |
| `blocking_t1_salute_v1.blend` | T1 world: four soldiers salute the flag. Frame 1 is the composition the director locked. | 4.0 s / 100 f | 35 mm | From behind, three-quarter right, low (1.0 m), slow push-in of about 0.9 m, gentle handheld |
| `blocking_t2_field_v1.blend` | T2 world: green crayon rows → crop rows | 4.0 s / 100 f | 35 mm | 0.30 m above the soil, looking across the rows, horizon 8% from the top edge, slow 0.6 m forward glide. Slider. |

## Colour key

| Outline | Who |
|---|---|
| Terracotta | Soldier A: the patch soldier, rightmost in the salute row (nearest camera) |
| Blue | Soldier B |
| Green | Soldier C |
| Violet | Soldier D (leftmost) |
| Light grey | Set: ground, crop ridges and plants, palms, flagpole, flag |

The patch takes soldier A's colour. On screen in the salute shot, left to right: D, C, B, A.

## Run

```
blender -b -P blocking_t1_patch_to_salute_v1.py
blender -b -P blocking_t1_patch_pullback_v1.py
blender -b -P blocking_t1_salute_v1.py
blender -b -P blocking_t2_field_v1.py
```

Each script rebuilds its `.blend` next to itself. `uae_set.py` is the shared module (set pieces, mannequins, poses, camera rig, outline look). The scripts were tested on Blender 4.5 LTS and 5.2. The shipped `.blend` files were saved from 4.5 and open in 5.x.

## Decisions and deviations

- **Salute composition is locked** (`SALUTE_CAM` / `SALUTE_AIM` / 35 mm in `uae_set.py`, frame 1 of the salute shot). The one-shot lands on it exactly at f110; checked numerically, head positions match to three decimals.
- **One-shot patch: soldier A's RIGHT upper sleeve (the saluting arm), on the side facing the camera.** From behind-right his left arm is hidden by his body. The rule "left sleeve, verify against a reference" still applies to the old bridge file only.
- **One-shot lens: 100 → 35 mm during the pull-back**, eased together with the dolly. The move only widens; it is never a dolly-zoom. The red bar fills the whole frame from f1 to f40 (checked numerically).
- **One-shot handheld only from f110** (blended in over 1 s): the macro and the pull-back stay smooth.

- **25 fps instead of 24**, to match the 4K 25p crayon footage the bridges cut against.
- **Patch on the LEFT upper sleeve, hoist (red bar) toward the front.** This is not verified yet: swap `side='l'` in the patch script once there is a real uniform reference. The red bar is a quarter of the patch width, following the UAE flag proportion.
- **The opening frame of T1 is closer than real 1:1 macro** (frame about 2 cm wide at 5.5 cm) so that only red thread is in frame, like the end of the red crayon plate. Within the visible frame, red covers about 92–100% of the width; at most a soft sliver of green touches the top-right corner.
- **The T1 pull-back ends on a medium close-up** (frame 0.45 × 0.25 m: patch below centre, top of the shoulder in frame), not on a patch filling two-thirds of the frame. This follows "the flag on the shoulder, then cut". The T1-B end-frame still prompt should be reframed to match.
- **The salute shot uses 35 mm, not the 50 mm in the image prompt.** At 50 mm the row and a 7 m flag can't share the frame from a low camera. The soldiers are framed from the knees up. The flag is in the upper middle of the frame, against the sky.
- **T2 hero palm** stands on the horizon at about 40% from frame left, where the green crayon tip sits in shot_2. The crayon lifts out during the bridge, and the palm is the shape left behind.
- **No handheld on the macro or field shots.** At 5.5 cm, any noise reads as shake, and the brief is dreamy and smooth. The salute shot has gentle handheld (1.5 cm / 0.3° / 1.5 s).
- Seeded randomness (seed 7) for the palms, so every rebuild matches.
