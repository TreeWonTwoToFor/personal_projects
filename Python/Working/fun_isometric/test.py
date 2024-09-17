import pygame

focal_length = -10
camera_point = (0,focal_length)
vertex_point = (3,5)

def find_projected(x, z):
    x_projected = (focal_length * x) / (focal_length + z)
    return x_projected

print(find_projected(vertex_point[0], focal_length))