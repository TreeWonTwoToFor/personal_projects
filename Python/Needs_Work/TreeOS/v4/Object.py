import math
import numpy
import quaternion

import Parser

class Object:
    def __init__(self, model, color, model_type="poly"):
        self.model = remove_reference(model)
        self.color = color
        if model_type == "poly":
            self.update()
            self.move_to_origin()
            for poly in self.model:
                poly.append(color)
        elif model_type == "wire":
            self.update_wireframe()
            self.move_to_origin_wireframe()

    def update(self):
        self.center_point = get_center_point(self.model)
        self.collision_box = get_bounding_box(self.model)
        self.collision_values = get_bounding_box_values(self.model)

    def move_to_origin(self):
        cp = self.center_point
        self.translate(-cp[0], -cp[1], -cp[2])
        self.update()
        
    def translate(self, x, y, z):
        scalar_list = [x,y,z]
        for point_pair in self.model:
            for point in point_pair[0]:
                for i in range(3):
                    point[i] = point[i] + scalar_list[i]
        self.update()
    
    def scale(self, x, y, z):
        scalar_list = [x,y,z]
        for point_pair in self.model:
            for point in point_pair[0]:
                for i in range(3):
                    point[i] = (point[i] - self.center_point[i]
                      ) * scalar_list[i] + self.center_point[i]
        self.update()

    def rotate(self, rx, ry, rz, angle):
        axis = numpy.array([rx, ry, rz])
        axis = axis / numpy.linalg.norm(axis)
        q = numpy.quaternion(numpy.cos(angle / 2), *(axis * numpy.sin(angle / 2)))
        for poly in self.model:
            for point in poly[0]:
                px = point[0]-self.center_point[0]
                py = point[1]-self.center_point[1]
                pz = point[2]-self.center_point[2]
                v = numpy.array([px, py, pz])
                v_q = numpy.quaternion(0, *v)
                v_rot = q * v_q * q.conj()
                point_list = v_rot.imag
                for i in range(3):
                    point[i] = point_list[i] + self.center_point[i]    
                #point[0], point[1], point[2] = v_rot.imag
        self.update()


def remove_reference(model):
    new_model = []
    for vertex_list, face in model:
        new_poly = []
        for vertex in vertex_list:
            new_poly.append(vertex)
        new_model.append([new_poly, face])
    return new_model

def get_center_point(model):
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

    for poly in model:
        for point in poly[0]:
            x, y, z = point
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            min_z = min(min_z, z)
            max_z = max(max_z, z)

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    center_z = (min_z + max_z) / 2

    return [center_x, center_y, center_z]

def scale(og_model, x, y, z):
    model = remove_reference(og_model)
    cp = get_center_point(model)
    scalar_list = [x,y,z]
    for point_pair in model:
        for point in point_pair[0]:
            for i in range(3):
                point[i] = (point[i] - cp[i]) * scalar_list[i] + cp[i]
    return model

def translate(og_model, x, y, z):
    model = remove_reference(og_model)
    scalar_list = [x,y,z]
    for poly in model:
        for point in poly[0]:
            for i in range(3):
                point[i] = point[i] + scalar_list[i]
    return model

def get_bounding_box(model):
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
    x_size = math.sqrt((max_x - low_x)**2)/2
    y_size = math.sqrt((max_y - low_y)**2)/2
    z_size = math.sqrt((max_z - low_z)**2)/2
    box_model = Parser.get_model("./blender_files/cube.obj")
    box_model = scale(box_model, x_size, y_size, z_size)
    cp_box = get_center_point(box_model)
    box_model = translate(box_model, -cp_box[0], -cp_box[1], -cp_box[2])
    cp_full = get_center_point(model)
    return translate(box_model, cp_full[0], cp_full[1], cp_full[2])

def get_bounding_box_values(model):
    max_x, max_y, max_z = model[0][0][0][0], model[0][0][0][1], model[0][0][0][2]
    low_x, low_y, low_z = model[0][0][0][0], model[0][0][0][1], model[0][0][0][2]
    for point_pair in model:
        for point in point_pair[0]:
            if point[0] > max_x: max_x = point[0]
            if point[0] < low_x: low_x = point[0]
            if point[1] > max_y: max_y = point[1]
            if point[1] < low_y: low_y = point[1]
            if point[2] > max_z: max_z = point[2]
            if point[2] < low_z: low_z = point[2]
    return (low_x, low_y,low_z, max_x, max_y, max_z)
