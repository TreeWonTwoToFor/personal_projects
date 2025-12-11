FPS = 60
resolution = (800, 600)
debug = True
# normal, render, testing
mode = "normal"
scene_name = "farlands_solar_system.txt"
#scene_name = "test_scene.txt"
frame_count = 100
mouse_control = False
mouse_sensitivity = 0.5

def get_settings():
    return [FPS, resolution, debug, mode, scene_name, frame_count, mouse_control, mouse_sensitivity]
