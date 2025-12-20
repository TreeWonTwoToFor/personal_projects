import math
import numpy

from Engine import Parser

class Object:
    def __init__(self, model, color_list, model_type="poly"):
        self.model = remove_reference(model)
        self.update(True)
        if model_type == "poly":
            self.move_to_origin()
            for i in range(len(self.model)):
                poly = self.model[i]
                color = color_list[i]
                poly.append(color)
        elif model_type == "wire":
            self.update_wireframe()
            self.move_to_origin_wireframe()

    def update(self, change_cp):
        aabb = get_bounding_box(self)
        if change_cp:
            avg_x = (aabb[1][0] + aabb[1][3]) / 2
            avg_y = (aabb[1][1] + aabb[1][4]) / 2
            avg_z = (aabb[1][2] + aabb[1][5]) / 2
            self.center_point = (avg_x, avg_y, avg_z)
        self.collision_box = aabb[0]
        self.collision_values = aabb[1]

    def move_to_origin(self):
        cp = self.center_point
        if cp != [0,0,0]:
            self.translate([-cp[0], -cp[1], -cp[2]])
        
    def translate(self, xyz):
        for poly in self.model:
            for point in poly[0]:
                for i in range(3):
                    point[i] = point[i] + xyz[i]
        self.update(True)
    
    def scale(self, xyz):
        for poly in self.model:
            for point in poly[0]:
                for i in range(3):
                    point[i] = (point[i] - self.center_point[i]
                      ) * xyz[i] + self.center_point[i]
        self.update(False)

    def rotate(self, xyz, angle):
        axis = numpy.array(xyz, dtype=float)
        axis /= numpy.linalg.norm(axis)
        c = numpy.cos(angle / 2.0)
        s = numpy.sin(angle / 2.0)
        x, y, z = axis * s
        # matrix based on quaternion math
        R = numpy.array([
            [1 - 2*(y*y + z*z), 2*(x*y - z*c),     2*(x*z + y*c)],
            [2*(x*y + z*c),     1 - 2*(x*x + z*z), 2*(y*z - x*c)],
            [2*(x*z - y*c),     2*(y*z + x*c),     1 - 2*(x*x + y*y)]
        ])
        all_points = numpy.array(
            [point for poly in self.model for point in poly[0]], dtype=float)
        all_normals= numpy.array(
            [poly[1] for poly in self.model], dtype=float)
        # translate to origin before rotation
        centered_points = all_points - self.center_point
        rotated_points = centered_points @ R.T + self.center_point
        rotated_normals = all_normals @ R.T
        # put all the rotated points back into the model structure
        idx_v = 0 # vertex
        idx_n = 0 # normal
        for poly in self.model:
            n = len(poly[0])
            poly[0][:] = rotated_points[idx_v:idx_v+n].tolist()
            poly[1] = rotated_normals[idx_n].tolist()
            idx_v += n
            idx_n += 1
        self.update(True)

    def orbit(self, xyz, angle, oxyz=[0,0,0]):
        self.center_point = oxyz # makes the object rotate around the new origin, aka orbit
        self.rotate(xyz, angle)
        # unseen step is that the center point is put back into the object
        self.rotate(xyz, -angle) # undoes the rotation on the object.


def remove_reference(model):
    new_model = []
    for vertex_list, face in model:
        new_poly = []
        for vertex in vertex_list:
            new_vertex = []
            for val in vertex:
                new_vertex.append(val)
            new_poly.append(new_vertex)
        new_model.append([new_poly, face])
    return new_model

def get_center_point(model):
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

    for poly in model:
        for point in poly[0]:
            x, y, z = point
            if min_x>x: min_x=x
            if max_x<x: max_x=x
            if min_y>y: min_y=y
            if max_y<y: max_y=y
            if min_z>z: min_z=z
            if max_z<z: max_z=z

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    center_z = (min_z + max_z) / 2

    return [center_x, center_y, center_z]

def scale_old(og_model, x, y, z):
    model = remove_reference(og_model)
    cp = get_center_point(model)
    scalar_list = [x,y,z]
    for point_pair in model:
        for point in point_pair[0]:
            for i in range(3):
                point[i] = (point[i] - cp[i]) * scalar_list[i] + cp[i]
    return model

def translate_old(og_model, x, y, z):
    model = remove_reference(og_model)
    scalar_list = [x,y,z]
    for poly in model:
        for point in poly[0]:
            for i in range(3):
                point[i] = point[i] + scalar_list[i]
    return model

def get_bounding_box(obj):
    model = obj.model
    max_x, max_y, max_z = model[0][0][0][0], model[0][0][0][1], model[0][0][0][2]
    low_x, low_y, low_z = model[0][0][0][0], model[0][0][0][1], model[0][0][0][2]
    for poly in model:
        for point in poly[0]:
            if point[0] > max_x: max_x = point[0]
            if point[0] < low_x: low_x = point[0]
            if point[1] > max_y: max_y = point[1]
            if point[1] < low_y: low_y = point[1]
            if point[2] > max_z: max_z = point[2]
            if point[2] < low_z: low_z = point[2]
    obj.aabb_min = (low_x, low_y, low_z)
    obj.aabb_max = (max_x, max_y, max_z)

    x_size = math.sqrt((max_x - low_x)**2)/2
    y_size = math.sqrt((max_y - low_y)**2)/2
    z_size = math.sqrt((max_z - low_z)**2)/2

    box_model = Parser.get_model("./Assets/Objects/cube.obj")
    box_model = scale_old(box_model, x_size, y_size, z_size)
    cp_box = get_center_point(box_model)
    box_model = translate_old(box_model, -cp_box[0], -cp_box[1], -cp_box[2])
    cp_full = get_center_point(model)

    bb_model = translate_old(box_model, cp_full[0], cp_full[1], cp_full[2])
    bb_values = (low_x, low_y,low_z, max_x, max_y, max_z)
    return (bb_model, bb_values)
