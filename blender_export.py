import math
import bpy

FRAME_RATE = 50 # ignore frame rate setting

scene = bpy.context.scene
robot_obj = bpy.context.active_object

markers = sorted(scene.timeline_markers, key=lambda m: m.frame)
marker_i = 0

def keyframe_data(obj):
    return "{} {} {} {}\n".format(scene.frame_current / FRAME_RATE,
        obj.location[0], obj.location[1],
        math.degrees(obj.rotation_euler[2]))

def marker_data(marker):
    return "{} {}\n".format(marker.frame / FRAME_RATE, marker.name)

filename = bpy.data.filepath.replace('.blend', '') + '.txt'
with open(filename, "w") as f:
    scene.frame_set(0)
    while True:
        scene.update()
        bpy.ops.object.paths_calculate()
        f.write(keyframe_data(robot_obj))
        if bpy.ops.screen.keyframe_jump(next=True) != {'FINISHED'}:
            break # no more keyframes
        # print all markers we passed after jumping
        while marker_i < len(markers) and scene.frame_current >= markers[marker_i].frame:
            f.write(marker_data(markers[marker_i]))
            marker_i += 1

    while marker_i < len(markers):
        f.write(marker_data(markers[marker_i]))
        marker_i += 1
