"""Shared blocking module - UAE Flag Day film, AI transition shots.

Axes: metres, Z up, floor Z = 0. Figures are built in their own local frame
facing +Y with their own right at +X, then placed with location + Z rotation.
Output: 16:9, 1280x720, 25 fps (matches the live-action crayon plates), 36 mm sensor.

Geometry only. Colours identify figures, never wardrobe or light.
"""
import math
import os
import random

import bpy  # first: the pip bpy module only exposes bmesh/mathutils after this
import bmesh
from mathutils import Matrix, Vector

FPS = 25
RES = (1280, 720)
SENSOR = 36.0
SEED = 7

# Outline colour key (named figures get their own muted colour).
COL_A = (0.78, 0.40, 0.30)   # soldier A - the patch soldier, rightmost in the salute row
COL_B = (0.32, 0.50, 0.72)   # soldier B
COL_C = (0.40, 0.62, 0.40)   # soldier C
COL_D = (0.60, 0.46, 0.72)   # soldier D
COL_EXTRA = (0.84, 0.84, 0.84)
COL_SET = (0.78, 0.78, 0.78)

PX_FIGURE, PX_EXTRA, PX_SET = 2.6, 1.9, 1.3


# ---------------------------------------------------------------- scene / look

def reset_scene(frames):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.render.resolution_x, scene.render.resolution_y = RES
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 1, frames
    sh = scene.display.shading
    sh.light = 'FLAT'
    sh.color_type = 'MATERIAL'
    sh.show_backface_culling = True
    sh.show_cavity = False
    sh.show_shadows = False
    sh.show_object_outline = False
    scene.view_settings.view_transform = 'Standard'
    world = bpy.data.worlds.new('World')
    world.color = (1.0, 1.0, 1.0)
    scene.world = world
    return scene


def _mat(name, rgb):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
        m.diffuse_color = (*rgb, 1.0)
        m.use_backface_culling = True
    return m


def _new_object(name, bm):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def outline(ob, rgb, px):
    """Slot 0 white fill, slot 1 outline colour, inverted-hull Solidify."""
    ob.data.materials.clear()
    ob.data.materials.append(_mat('fill_white', (1.0, 1.0, 1.0)))
    ob.data.materials.append(_mat('outline_%02x%02x%02x' % tuple(int(c * 255) for c in rgb), rgb))
    for p in ob.data.polygons:
        p.material_index = 0
    mod = ob.modifiers.new('outline', 'SOLIDIFY')
    mod.offset = 1.0
    mod.use_flip_normals = True
    mod.use_rim = False
    mod.material_offset = 1
    mod.thickness = 0.01
    ob['outline_px'] = px
    return ob


def key_outlines(scene, cam, frames, constant=False):
    """Key outline thickness from the camera distance to each object's nearest surface."""
    obs = [o for o in scene.objects if 'outline_px' in o]
    for f in frames:
        scene.frame_set(f)
        cpos = cam.matrix_world.translation.copy()
        per_px = 2.0 * math.atan(SENSOR / 2.0 / cam.data.lens) / RES[0]
        for ob in obs:
            local = ob.matrix_world.inverted() @ cpos
            ok, loc, _n, _i = ob.closest_point_on_mesh(local)
            dist = (cpos - ob.matrix_world @ loc).length if ok else (cpos - ob.matrix_world.translation).length
            ob.modifiers['outline'].thickness = max(dist * per_px * ob['outline_px'], 1e-5)
            ob.keyframe_insert('modifiers["outline"].thickness', frame=f)
    for ob in obs:
        set_interp(ob, 'CONSTANT' if constant else 'LINEAR')
    scene.frame_set(scene.frame_start)


# ---------------------------------------------------------------- f-curves (4.x / 5.x)

def fcurves_of(idb):
    ad = idb.animation_data
    if ad is None or ad.action is None:
        return []
    try:
        from bpy_extras import anim_utils
        cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
        if cb is not None:
            return list(cb.fcurves)
    except (ImportError, AttributeError):
        pass
    return list(ad.action.fcurves)


def set_interp(idb, mode, prefix=None):
    for fc in fcurves_of(idb):
        if prefix and not fc.data_path.startswith(prefix):
            continue
        for kp in fc.keyframe_points:
            kp.interpolation = mode


# ---------------------------------------------------------------- bmesh primitives

def _apply(bm, verts, m):
    bmesh.ops.transform(bm, matrix=m, verts=verts)


def add_ellipsoid(bm, center, radii, m=Matrix.Identity(4), segs=16, rings=10):
    g = bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=1.0)
    _apply(bm, g['verts'], m @ Matrix.Translation(center) @ Matrix.Diagonal((*radii, 1.0)))


def add_capsule(bm, a, b, r, scale_xy=(1.0, 1.0), m=Matrix.Identity(4), segs=14):
    a, b = Vector(a), Vector(b)
    axis = b - a
    rot = axis.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    sc = Matrix.Diagonal((scale_xy[0], scale_xy[1], 1.0, 1.0))
    g = bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=axis.length)
    _apply(bm, g['verts'], m @ Matrix.Translation((a + b) / 2) @ rot @ sc)
    for end in (a, b):
        add_ellipsoid(bm, end, (r * scale_xy[0], r * scale_xy[1], r), m @ Matrix.Translation(end) @ rot
                      @ Matrix.Translation(-end), segs, 8)


def add_box(bm, center, size, m=Matrix.Identity(4)):
    g = bmesh.ops.create_cube(bm, size=1.0)
    _apply(bm, g['verts'], m @ Matrix.Translation(center) @ Matrix.Diagonal((*size, 1.0)))


def add_icosphere(bm, center, r, subdiv=1):
    g = bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=r)
    _apply(bm, g['verts'], Matrix.Translation(center))


# ---------------------------------------------------------------- mannequin

def solve_2bone(root, target, l1, l2, pole):
    root, target, pole = Vector(root), Vector(target), Vector(pole)
    d = target - root
    dist = min(max(d.length, abs(l1 - l2) + 1e-4), l1 + l2 - 1e-4)
    dn = d.normalized()
    a = (l1 * l1 + dist * dist - l2 * l2) / (2 * dist)
    h = math.sqrt(max(l1 * l1 - a * a, 0.0))
    p = pole - dn * pole.dot(dn)
    if p.length < 1e-6:
        p = dn.orthogonal()
    p.normalize()
    return root + dn * a + p * h, root + dn * dist


POSE_ATTENTION = dict(
    hip=(0.0, 0.0, 0.95), lean=0.0, yaw=0.0, roll=0.0,
    head_yaw=0.0, head_pitch=0.0, head_roll=0.0,
    hand_r=(0.24, 0.03, 0.88), hand_l=(-0.24, 0.03, 0.88),
    pole_r=(0.3, -1.0, 0.0), pole_l=(-0.3, -1.0, 0.0),
    foot_r=(0.11, 0.02, 0.08), foot_l=(-0.11, 0.02, 0.08),
)

# Right hand at the right brow, elbow out to the side at shoulder height, head up to the flag.
POSE_SALUTE = dict(POSE_ATTENTION, hand_r=(0.13, 0.10, 1.60), pole_r=(1.0, 0.25, -0.15), head_pitch=12.0)

L_UPPER_ARM, L_FOREARM, L_THIGH, L_SHIN = 0.29, 0.27, 0.44, 0.43
R_UPPER_ARM = 0.05


def build_figure(name, rgb, pose, loc=(0, 0, 0), yaw_deg=0.0, px=PX_FIGURE):
    """Mannequin in its local frame (faces +Y, right = +X). Returns (object, joints in world space)."""
    p = dict(POSE_ATTENTION, **pose)
    bm = bmesh.new()
    hip = Vector(p['hip'])
    # Upper body pivots at the hip. lean > 0 = forward (top toward +Y).
    up = (Matrix.Translation(hip) @ Matrix.Rotation(math.radians(p['yaw']), 4, 'Z')
          @ Matrix.Rotation(math.radians(-p['lean']), 4, 'X') @ Matrix.Rotation(math.radians(p['roll']), 4, 'Y'))
    j = {}
    # pelvis + torso
    add_ellipsoid(bm, hip, (0.17, 0.11, 0.11))
    add_capsule(bm, (0, 0, 0.10), (0, 0, 0.40), 0.15, (1.25, 0.75), up)
    neck = up @ Vector((0, 0, 0.50))
    j['neck'] = neck
    add_capsule(bm, (0, 0, 0.44), (0, 0, 0.56), 0.05, m=up)
    # head
    hm = (up @ Matrix.Translation((0, 0, 0.50)) @ Matrix.Rotation(math.radians(p['head_yaw']), 4, 'Z')
          @ Matrix.Rotation(math.radians(p['head_pitch']), 4, 'X') @ Matrix.Rotation(math.radians(p['head_roll']), 4, 'Y'))
    add_ellipsoid(bm, (0, 0.01, 0.13), (0.085, 0.10, 0.115), hm)
    add_ellipsoid(bm, (0, 0.105, 0.11), (0.018, 0.022, 0.026), hm, 10, 6)          # nose
    for sx in (-1, 1):
        add_ellipsoid(bm, (sx * 0.036, 0.092, 0.15), (0.014, 0.012, 0.012), hm, 8, 6)  # eye bumps
    j['head'] = hm @ Vector((0, 0.01, 0.13))
    # arms
    for side, sx in (('r', 1), ('l', -1)):
        sh = up @ Vector((sx * 0.20, 0.0, 0.46))
        elbow, wrist = solve_2bone(sh, p['hand_' + side], L_UPPER_ARM, L_FOREARM, p['pole_' + side])
        add_capsule(bm, sh, elbow, R_UPPER_ARM)
        add_capsule(bm, elbow, wrist, 0.042)
        add_ellipsoid(bm, wrist, (0.045, 0.045, 0.045), segs=10, rings=6)
        j['shoulder_' + side], j['elbow_' + side], j['hand_' + side] = sh, elbow, wrist
    # legs
    for side, sx in (('r', 1), ('l', -1)):
        hj = hip + Vector((sx * 0.095, 0.0, -0.03))
        knee, ankle = solve_2bone(hj, p['foot_' + side], L_THIGH, L_SHIN, (0, 1, 0))
        add_capsule(bm, hj, knee, 0.075)
        add_capsule(bm, knee, ankle, 0.055)
        add_ellipsoid(bm, ankle + Vector((0, 0.07, -0.04)), (0.05, 0.12, 0.045), segs=10, rings=6)
        j['knee_' + side], j['foot_' + side] = knee, ankle
    ob = _new_object(name, bm)
    ob.location = loc
    ob.rotation_euler = (0, 0, math.radians(yaw_deg))
    outline(ob, rgb, px)
    bpy.context.view_layer.update()
    mw = ob.matrix_world
    return ob, {k: mw @ v for k, v in j.items()}


def sleeve_patch(name, rgb, joints, side='l', along=0.30, size=(0.085, 0.055)):
    """Flag patch on the upper sleeve. Returns (object, centre, outward normal, front direction)."""
    sh, el = joints['shoulder_' + side], joints['elbow_' + side]
    down = (el - sh).normalized()
    body_out = (sh - joints['neck'])
    body_out.z = 0
    n = (body_out - down * body_out.dot(down)).normalized()
    front = down.cross(n).normalized()
    if front.y < 0:               # keep 'front' pointing the way the soldier faces (+Y here)
        front = -front
    centre = sh + down * (L_UPPER_ARM * along) + n * (R_UPPER_ARM + 0.003)
    basis = Matrix((front, n, -down)).transposed().to_4x4()
    bm = bmesh.new()
    add_box(bm, (0, 0, 0), (size[0], 0.006, size[1]), Matrix.Translation(centre) @ basis)
    ob = _new_object(name, bm)
    outline(ob, rgb, PX_FIGURE)
    return ob, centre, n, front


# ---------------------------------------------------------------- set pieces

def ground(size=400.0, name='ground'):
    bm = bmesh.new()
    add_box(bm, (0, 0, -0.05), (size, size, 0.1))
    return outline(_new_object(name, bm), COL_SET, PX_SET)


def palm(bm, base, height, lean_deg=0.0, lean_dir=0.0, rng=None):
    rng = rng or random.Random(SEED)
    base = Vector(base)
    tilt = Vector((math.sin(math.radians(lean_dir)), math.cos(math.radians(lean_dir)), 0)) * math.tan(math.radians(lean_deg))
    top = base + Vector((0, 0, height)) + tilt * height
    add_capsule(bm, base, top, 0.18, segs=10)
    for k in range(9):
        ang = k / 9 * math.tau + rng.uniform(-0.2, 0.2)
        d = Vector((math.cos(ang), math.sin(ang), 0))
        tip = top + d * 2.4 + Vector((0, 0, -1.0 + rng.uniform(-0.3, 0.3)))
        mid = top + d * 1.2 + Vector((0, 0, 0.35))
        add_capsule(bm, top, mid, 0.12, (1.0, 0.35), segs=8)
        add_capsule(bm, mid, tip, 0.09, (1.0, 0.35), segs=8)
    return top


# ---------------------------------------------------------------- camera

def camera_rig(name, lens):
    rig = bpy.data.objects.new(name + '_rig', None)
    bpy.context.scene.collection.objects.link(rig)
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = SENSOR
    cd.sensor_fit = 'HORIZONTAL'
    cd.clip_start = 0.01
    cd.clip_end = 1000.0
    cam = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(cam)
    cam.parent = rig
    bpy.context.scene.camera = cam
    return rig, cam


def key_rig(rig, frame, pos, aim):
    pos, aim = Vector(pos), Vector(aim)
    rig.location = pos
    prev = rig.rotation_euler.copy()
    rig.rotation_euler = (aim - pos).to_track_quat('-Z', 'Y').to_euler('XYZ', prev)
    rig.keyframe_insert('location', frame=frame)
    rig.keyframe_insert('rotation_euler', frame=frame)


def handheld(cam, amp_m=0.015, amp_deg=0.3, period_s=1.5, seed=SEED):
    """Gentle handheld = NOISE modifiers on the camera's own channels (strength = 4 x amplitude)."""
    cam.keyframe_insert('location', frame=1)
    cam.keyframe_insert('rotation_euler', frame=1)
    for i, fc in enumerate(fcurves_of(cam)):
        mod = fc.modifiers.new('NOISE')
        mod.scale = period_s * FPS
        mod.phase = seed * 3.1 + i * 17.3
        amp = amp_m if fc.data_path == 'location' else math.radians(amp_deg)
        mod.strength = 4.0 * amp


def save_blend(script_file, tag, version=1):
    path = os.path.join(os.path.dirname(os.path.abspath(script_file)), 'blocking_%s_v%d.blend' % (tag, version))
    bpy.ops.wm.save_as_mainfile(filepath=path, check_existing=False)
    print('saved', path)
    return path
