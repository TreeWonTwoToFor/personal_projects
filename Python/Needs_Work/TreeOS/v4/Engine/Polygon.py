class Polygon:
    def __init__(self, point_a, point_b, point_c):
        point_list = [point_a, point_b, point_c]

    def __str__(self):
        return self.point_list

def points_to_polygons(point_list):
    if len(point_list) % 3 == 0:
        poly_list = []
        for i in range(0, len(point_list), 3):
            poly_list.append(Polygon(point_list[i], point_list[i+1], point_list[i+2]))
        return poly_list
    else:
        raise ValueError("Point list is of incorrect size.")