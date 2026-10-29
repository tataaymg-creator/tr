# Red stroke → stitched flag patch (storyboard 04 → 05)

Assets (rename uploads to these names, or swap the handles):
- `@shot_1` — real crayon macro, 1.64 s, 3840×2160, 25 fps
- `@shot_1_last` — last frame of `@shot_1` (`red_patch/shot_1_last.png`)
- `@stitch_macro` — frontal macro of vertical red satin-stitch columns
- `@patch_reveal` — low raking macro of the red bar with black merrowed edge, green/white/black soft in the distance, warm sun (Option A only)
- `@uniform_ref` — studio reference of the desert-camo uniform with the flag patch on the upper sleeve (Option B)
- `@sleeve_wide` — new wider still of the sleeve and shoulder with the patch (Option B, generate first)

---

## OPTION A — all in Seedance (continues straight out of the real crayon shot)

Edit: hard cut from the last frame of `@shot_1` to frame 1 of this clip. Start frame = `@shot_1_last`, end frame = `@patch_reveal`.

```
5-second 16:9 macro shot, one continuous camera move with no cuts: a red wax-crayon stroke on paper transforms in place into embroidered red thread on a flag patch, then the camera tilts up to reveal the patch is the UAE flag.
The clip continues directly from live footage: frame 0 is @shot_1_last exactly.

REFERENCES
@shot_1_last — THE VERY FIRST FRAME OF THE CLIP. Low raking macro across white paper covered in red wax-crayon strokes, the blunt red crayon tip in soft focus at screen left. Take its angle, lens, focus and texture exactly.
@shot_1 — motion and pace reference only: how slowly the crayon drags, how shallow the focus is. Take nothing else.
@stitch_macro — the middle state: frontal macro of tight vertical columns of twisted red thread with pale backing fabric showing in thin gaps between columns. Take thread structure and scale only; ignore its brick-red tint.
@patch_reveal — THE LAST FRAME OF THE CLIP. Take angle, framing, focus fall-off, black merrowed border, the soft green, white and black bands at the far end, and the deep crimson thread colour.

LOOK
Macro lens, very shallow depth of field, one focus plane that travels with the move. Clean modern digital cinema look, deep clean blacks, rich saturated crimson. Light begins soft and even like @shot_1 and turns into warm low golden sun raking from frame-top-right by the end, like @patch_reveal.

THE RED
One crimson for the whole clip — the deep crimson of @patch_reveal. The crayon wax, the thread and the flag bar are the same red.

SHOTS
0.0–0.7s — Exactly the angle of @shot_1_last, same lens, same focus. The crayon tip at screen left drags a short way along the paper at the same slow pace as @shot_1, then lifts and leaves frame left by 0.7s. Only paper and red wax remain. BACKGROUND: nothing but the stroked paper, soft at the top edge.
0.7–2.2s — Continuous slow push-in, never stopping. The camera eases from the low raking angle to straight-on over the surface while rolling about 15° so the diagonal strokes become vertical. As it moves, the texture transforms in place: each wax streak thickens and twists into a strand of red thread, the strands gather into tight vertical satin-stitch columns, and the white paper between them becomes the pale backing fabric showing through the thin gaps. Stray fibres lift off the threads. By 2.2s the frame is @stitch_macro: frontal, columns edge to edge, in the deep crimson.
2.2–2.7s — On @stitch_macro, a slow forward drift; the move barely slows. Fine fibres catch the light.
2.7–5.0s — The camera tilts up and drops low across the surface, pulling back slightly, so the stitched plane falls into perspective and the columns turn into diagonal rows running away from camera. The black merrowed border slides in at the left edge, in focus. Warm low sun rakes in from frame-top-right and makes the thread glint. At the far end, out of focus, the green band appears top-right, then white, then black below it. The move eases to a smooth stop at 5.0s on exactly @patch_reveal.

SOUND
No music, no voice, no whooshes. 0.0–0.7s soft dry crayon-on-paper scratch, stopping when the crayon lifts. Then quiet room tone only.

KEEP CONSISTENT
Opens on exactly @shot_1_last, never on the stitches or the flag.
One unbroken move: no cut, no dissolve, no flash, no blur-wipe.
The crayon is gone by 0.7s and never returns; no hand ever appears.
The transformation happens in place, on the same surface, under a moving camera.
Same crimson from first to last frame.
Ends on exactly @patch_reveal: black border left, red bar sharp in the foreground, green/white/black soft in the distance.
No text, no logos, no extra objects.
```

---

## OPTION B — Seedance only for the move; dissolve in the edit

Assets for this option:
- `@stitch_macro` — start frame
- `@uniform_ref` — the uniform reference (two-panel studio image)
- `@sleeve_wide` — the new wider still (generate it first with the prompt below); reference image only, not in the end-frame slot

### Still prompt — `@sleeve_wide`

```
Photoreal 16:9 close-up of the right upper arm and shoulder of a soldier wearing the desert digital camouflage uniform of @uniform_ref, standing still, arm relaxed at the side.

REFERENCES
@uniform_ref — the uniform only: desert digital camouflage pattern and colours, sleeve, shoulder seam, collar, chest pocket flap, and the flag patch position on the upper outer sleeve. Ignore the grey studio backdrop, the grey circle over the face, the boots and the flat studio light.
@stitch_macro — the thread of the patch's red bar: tight vertical satin-stitch columns.

CAMERA
85mm, at the outer side of the arm, angled about 20° toward the front, slightly above shoulder height and looking a little down, so the collar and upper chest sit behind the shoulder.

FRAMING
The upper sleeve with the patch fills the left and centre of the frame. The patch sits just left of centre in the upper third, about one fifth of the frame width, square to camera and pin-sharp. The shoulder seam crosses near the top edge. Behind the shoulder, the collar fills the top-right corner with the neck out of frame; the chest pocket flap sits at the right edge, softly out of focus. Every edge of the frame cuts through fabric: every pixel is the uniform.

THE PATCH
Embroidered UAE flag, rectangular: vertical red bar on the left, green, white and black horizontal stripes to its right, black merrowed border all round. The red bar is vertical satin-stitch columns in deep crimson.

LIGHT AND LOOK
Warm low golden sun from frame-left, slightly behind the arm, rim-lighting the top of the shoulder and catching the thread and the ripstop weave, soft shadows in the fabric folds. Shallow depth of field. Clean modern digital cinema look, rich colour, deep clean blacks.

No background, no sky, no room, no face, no skin, no hands, no rank insignia, no text.
```

### Edit prompt — `@sleeve_wide` fix (v1 shows background in the corners)

Use the v1 still as the input image.

```
Edit @sleeve_wide: keep the same soldier, uniform, camouflage pattern, patch, colours and warm light. Only the framing changes: the camera is about 20% closer to the arm, so the uniform fills the whole frame.

FRAMING
The upper sleeve fills the left half of the frame, its outer edge running past the left frame edge. The top of the shoulder runs past the top edge of the frame; the shoulder's outline is never seen against anything. The collar fills the top-right corner and runs past the top and right edges. The chest pocket flap with the tan name tape sits at the right, softly out of focus. The patch stays whole and pin-sharp, its centre about one third from the left and just above the middle, about 30% of the frame width.

Every edge and every corner of the frame cuts through uniform fabric. No background, no sky, no wall, no blur of a location in any corner. No face, neck, skin, hands, rank insignia or text.
```

### Video prompt — 6 s

Start frame = `@stitch_macro`. `@uniform_ref` and `@sleeve_wide` go in as reference images only.

```
6-second 16:9 shot, one continuous camera move: the camera travels up a column of red embroidered thread, then pulls straight back to reveal it is the red bar of a UAE flag patch sewn on the upper sleeve of a desert-camouflage military uniform.

REFERENCES
@stitch_macro — THE VERY FIRST FRAME OF THE CLIP. Frontal macro of tight vertical columns of twisted red thread with pale backing fabric showing in thin gaps. Take angle, scale and focus exactly; the thread colour is deep crimson.
@uniform_ref — the uniform only: desert digital camouflage pattern and colours, sleeve, shoulder seam, collar, chest pocket flap, and the flag patch position on the upper outer sleeve. Ignore the grey studio backdrop, the grey circle over the face, the boots and the flat studio light.
@sleeve_wide — the framing the camera reaches at 5.0s, not the last frame. Take framing, angle, light and focus.

LOOK
Macro at the start, very shallow depth of field, focus locked on the patch for the whole move. Clean modern digital cinema look, deep clean blacks, rich saturated crimson. Soft even light on the macro warms into low golden sun from frame-left, slightly behind the arm, as the sleeve appears, as in @sleeve_wide.

THE PATCH
Embroidered UAE flag, rectangular: vertical red bar on the screen-left side, green, white and black horizontal stripes to its right, black merrowed border all round. The satin-stitch columns of the red bar run vertically.

FRAME RULE
From the first frame to the last, every pixel is the uniform: thread, patch, camouflage fabric. The camera never sees past the uniform.

SHOTS
0.0–1.5s — Exactly the angle of @stitch_macro. The camera travels straight UP the frame along the vertical stitch columns of the red bar, at a slow steady speed, so the columns slide downward through the frame like rails. Columns vertical, filling the frame edge to edge, fibres catching the light. The camera never stops.
1.5–5.0s — Carrying the upward momentum with no pause, the move turns into a smooth continuous pull-back straight away from the patch. The reveal comes in this order: the black merrowed edge of the red bar at screen-left; the green, white and black stripes to its right; the whole patch; the camouflage ripstop weave around it; then the upper sleeve with the patch on the outer arm, the shoulder seam near the top edge, and the collar and chest pocket flap at screen-right behind the shoulder. During the pull-back the camera rises slightly and arcs about 20° toward the soldier's front, so the shoulder always has the collar and chest behind it. Focus stays on the patch the whole way. At 5.0s the frame matches @sleeve_wide.
5.0–6.0s — The pull-back slows to a crawl and continues only a few millimetres; framing stays essentially @sleeve_wide, the patch sharp. The soldier stands still; only a faint breathing rise of the shoulder. Still moving on the last frame.

SOUND
No music, no voice, no effects. Quiet room tone only.

KEEP CONSISTENT
Opens on exactly @stitch_macro.
First 1.5s the camera moves UP along the stitch columns, before any pull-back.
One unbroken move, no cuts, no stop at any point.
Every frame is uniform only: no background, no sky, no room, no face, no skin, no hands.
The patch is the same patch from macro to wide: red bar left, black merrowed border.
Same crimson from first to last frame.
@sleeve_wide framing at 5.0s, then one more second of slow drift.
The soldier never moves except breathing.
No text, no rank insignia, no logos.
```

Edit for Option B:
- Grade `@shot_1` out of its flat log look first, and match its red to the crimson of the generated clip.
- Cross-dissolve 12 frames (0.48 s at 25 fps), from 1.16 s to the end of `@shot_1` at 1.64 s, into frame 0 of the Seedance clip.
- The crayon strokes run diagonally and the stitches run vertically. If the dissolve reads as two textures crossing, rotate the first second of the Seedance clip about −15° (scale up about 110% to hide the corners) and ease it back to 0° by 1.0 s.
