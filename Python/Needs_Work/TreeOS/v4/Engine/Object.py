import math
import numpy

from Engine import Parser

class Object:
    def __init__(self, model, color, model_type="poly"):
        self.model = remove_reference(model)
        self.color = color
        if model_type == "poly":
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
        self.update()
        cp = self.center_point
        if cp != [0,0,0]:
            self.translate(-cp[0], -cp[1], -cp[2])
            self.update()

    def recalculate_normals(self):
        polys = numpy.array([poly[0] for poly in self.model], dtype=float)
        v1 = polys[:, 1] - polys[:, 0]
        v2 = polys[:, 2] - polys[:, 0]
        normals = numpy.cross(v1, v2)
        normals /= numpy.linalg.norm(normals, axis=1)[:, None]  # normalize
        for poly, normal in zip(self.model, normals):
            poly[1] = normal
        
    def translate(self, x, y, z):
        scalar_list = [x,y,z]
        for poly in self.model:
            for point in poly[0]:
                for i in range(3):
                    point[i] = point[i] + scalar_list[i]
        self.update()
    
    def scale(self, x, y, z):
        scalar_list = [x,y,z]
        for poly in self.model:
            for point in poly[0]:
                for i in range(3):
                    point[i] = (point[i] - self.center_point[i]
                      ) * scalar_list[i] + self.center_point[i]
        self.update()

    def rotate(self, rx, ry, rz, angle):
        axis = numpy.array([rx, ry, rz], dtype=float)
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
        # translate to origin before rotation
        centered = all_points - self.center_point
        rotated = centered @ R.T + self.center_point
        # put all the rotated points back into the model structure
        idx = 0
        for poly in self.model:
            n = len(poly[0])
            poly[0][:] = rotated[idx:idx+n].tolist()
            idx += n
        self.update()

    def orbit(self, rx, ry, rz, angle, ox=0, oy=0, oz=0):
        old_center = self.center_point
        self.center_point = [ox,oy,oz] # rotate tries to move to origin initially.
        self.rotate(rx, ry, rz, angle)
        self.center_point = old_center
        # undoes the rotation on the object. could likely be condenced into one, smart call?
        self.rotate(rx, ry, rz, -angle)


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

def translate_old(og_model, x, y, z):
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
    box_model = Parser.get_model("./Assets/Objects/cube.obj")
    box_model = scale(box_model, x_size, y_size, z_size)
    cp_box = get_center_point(box_model)
    box_model = translate_old(box_model, -cp_box[0], -cp_box[1], -cp_box[2])
    cp_full = get_center_point(model)
    return translate_old(box_model, cp_full[0], cp_full[1], cp_full[2])

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
