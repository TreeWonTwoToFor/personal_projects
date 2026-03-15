import math

import Parser

class Object:
    def __init__(self, model):
        self.model = remove_reference(model)
        self.update()
        self.move_to_origin()

    def update(self):
        self.center_point = get_center_point_wireframe(self.model)
        self.collision_box = get_bounding_box_wireframe(self.model)
        self.collision_values = get_bounding_box_values(self.model)

    def move_to_origin(self):
        cp = self.center_point
        self.translate(-cp[0], -cp[1], -cp[2])
        self.update()
        
    def translate(self, x, y, z):
        scalar_list = [x,y,z]
        for point_pair in self.model:
            for point in point_pair:
                for i in range(3):
                    point[i] = point[i] + scalar_list[i]
        self.update()
    
    def scale(self, x, y, z):
        scalar_list = [x,y,z]
        for point_pair in self.model:
            for point in point_pair:
                for i in range(3):
                    point[i] = (point[i] - self.center_point[i]
                      ) * scalar_list[i] + self.center_point[i]
        self.update()

    def rotate(self, x, y, z):
        rotate_list = [x,y,z]
        for point_pair in self.model:
            for point in point_pair:
                for i in range(3):
                    point[i] = point[i] * math.cos(rotate_list[i])
        self.update()


def remove_reference(model):
    return [
        [[p1[0], p1[1], p1[2]], [p2[0], p2[1], p2[2]]]
        for p1, p2 in model
    ]

def get_center_point_wireframe(model):
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

    for point_pair in model:
        for point in point_pair:
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

def scale_wireframe(og_model, x, y, z):
    model = remove_reference(og_model)
    cp = get_center_point_wireframe(model)
    scalar_list = [x,y,z]
    for point_pair in model:
        for point in point_pair:
            for i in range(3):
                point[i] = (point[i] - cp[i]) * scalar_list[i] + cp[i]
    return model

def translate_wireframe(og_model, x, y, z):
    model = remove_reference(og_model)
    scalar_list = [x,y,z]
    for point_pair in model:
        for point in point_pair:
            for i in range(3):
                point[i] = point[i] + scalar_list[i]
    return model

# x y and z should be in radians
def rotate_wireframe(og_model, x, y, z):
    model = remove_reference(og_model)
    rotate_list = [x,y,z]
    for point_pair in model:
        for point in point_pair:
            for i in range(3):
                point[i] = point[i] * math.cos(rotate_list[i])
    return model

def get_bounding_box_wireframe(model):
    max_x, max_y, max_z = model[0][0][0], model[0][0][1], model[0][0][2]
    low_x, low_y, low_z = model[0][0][0], model[0][0][1], model[0][0][2]
    for point_pair in model:
        for point in point_pair:
            if point[0] > max_x: max_x = point[0]
            if point[0] < low_x: low_x = point[0]
            if point[1] > max_y: max_y = point[1]
            if point[1] < low_y: low_y = point[1]
            if point[2] > max_z: max_z = point[2]
            if point[2] < low_z: low_z = point[2]
    x_size = math.sqrt((max_x - low_x)**2)/2
    y_size = math.sqrt((max_y - low_y)**2)/2
    z_size = math.sqrt((max_z - low_z)**2)/2
    box_model = Parser.get_model_wireframe("./blender_files/cube.obj")
    box_model = scale_wireframe(box_model, x_size, y_size, z_size)
    cp_box = get_center_point_wireframe(box_model)
    box_model = translate_wireframe(box_model, -cp_box[0], -cp_box[1], -cp_box[2])
    cp_full = get_center_point_wireframe(model)
    return translate_wireframe(box_model, cp_full[0], cp_full[1], cp_full[2])

def get_bounding_box_values(model):
    max_x, max_y, max_z = model[0][0][0], model[0][0][1], model[0][0][2]
    low_x, low_y, low_z = model[0][0][0], model[0][0][1], model[0][0][2]
    for point_pair in model:
        for point in point_pair:
            if point[0] > max_x: max_x = point[0]
            if point[0] < low_x: low_x = point[0]
            if point[1] > max_y: max_y = point[1]
            if point[1] < low_y: low_y = point[1]
            if point[2] > max_z: max_z = point[2]
            if point[2] < low_z: low_z = point[2]
    return (low_x, low_y,low_z, max_x, max_y, max_z)