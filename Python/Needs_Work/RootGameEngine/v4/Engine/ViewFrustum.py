import math
import numpy

def get(screen, camera):
    screen_resolution = screen.get_size()
    pitch, yaw, roll = camera.angle[0], camera.angle[1], camera.angle[2]
    # calculate camera's forward, right, and up vectors for view matrix
    forward = [math.cos(pitch) * math.sin(yaw)]
    forward.append(math.sin(pitch))
    forward.append(math.cos(pitch) * math.cos(yaw))
    forward = numpy.array(forward)
    forward = forward/numpy.linalg.norm(forward)
    right = numpy.cross(numpy.array([0,1,0]), forward)
    right = right/numpy.linalg.norm(right)
    up = numpy.cross(forward, right)
    up = up/numpy.linalg.norm(up)
    
    # perspective projection matrix
    near = 0.1
    far = 1000.0
    aspect = screen_resolution[0]/screen_resolution[1]
    fovX = math.pi/2.25
    fovY = 2 * math.atan(math.tan(fovX/2)/aspect)
    f = 1 / math.tan(fovY/2)
    
    # matrix construction
    eye = numpy.array([camera.point[0], -camera.point[1], camera.point[2]])
    view = numpy.array([
        [right[0], right[1], right[2], -numpy.dot(right, eye)],
        [up[0], up[1], up[2], -numpy.dot(up,eye)],
        [-forward[0], -forward[1], -forward[2], numpy.dot(forward, eye)],
        [0,0,0,1]
    ])
    projection = numpy.array([
        [f/aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, -(far+near)/(far-near), -(2*far*near)/(far-near)],
        [0, 0, -1, 0]
    ])
    VP = projection @ view
    
    # plane extraction
    planes = []
    planes.append(VP[3] + VP[0])   # left
    planes.append(VP[3] - VP[0])   # right
    planes.append(VP[3] + VP[1])   # bottom
    planes.append(VP[3] - VP[1])   # top
    planes.append(VP[3] + VP[2])   # far
    planes.append(VP[3] - VP[2])   # near
    
    # normalize the planes
    for i in range(len(planes)):
        n = planes[i][:3]
        mag = numpy.linalg.norm(n)
    
    return planes

def aabb_outside_plane(plane, aabb_min, aabb_max):
    normal = plane[:3]
    positive_vertex = numpy.where(normal >= 0, aabb_max, aabb_min)
    distance = numpy.dot(normal, positive_vertex) + plane[3]
    return distance < 0
