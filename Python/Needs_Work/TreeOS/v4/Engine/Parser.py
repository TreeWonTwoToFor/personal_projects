import numpy

# needed for winding ordering
from Engine import Draw
from Engine import Camera

def read_blender_file(file_name):
    try:
        file = open(file_name)
        return file.read()
    except:
        raise FileNotFoundError(f"Could not find '{file_name}'")

def get_file_dictionary(file_text):
    line_list = file_text.split('\n')
    line_dictionary = {}
    for i in range(len(line_list)):
        line_dictionary[i+1] = line_list[i]
    return line_dictionary

def get_data(file_dict, data_type):
    data_list = []
    line_number = 1
    start_found = False
    while not start_found:
        try:
            if file_dict[line_number].split()[0] == data_type:
                start_found = True
            else:
                line_number += 1
        except:
            line_number += 1
    looking = True
    while looking:
        if file_dict[line_number] == "":
            looking = False
        elif file_dict[line_number].split()[0] == data_type:
            data_list.append(file_dict[line_number])
        else:
            looking = False
        line_number += 1
    return data_list

def file_dict_to_list(file_dict):
    file_list = []
    data_types = ['v', 'vn', 'vt', 'f']
    for data in data_types:
        data_list = []
        for val in get_data(file_dict, data):
            if val[0] != 'f':
                final_val = []
                for num in val.split()[1:]:
                    final_val.append(float(num))
                data_list.append(final_val)
            else:
                final_face = []
                for point in val.split()[1:]:
                    face_data = point.split('/')
                    for i in range(len(face_data)):
                        face_data[i] = int(face_data[i])
                    final_face.append(face_data)
                data_list.append(final_face)
        file_list.append(data_list)
    return file_list

# each data point in the model has a list of vertices, as well as the face normal
def get_model(file_name):
    text = read_blender_file(file_name)
    file_dict = get_file_dictionary(text)
    file_list = file_dict_to_list(file_dict)
    vertex_list = file_list[0]
    vertex_normal_list = file_list[1]
    uv_list = file_list[2]
    face_list = file_list[3]
    model = []
    # collects all vertecies in a face
    for i in range(len(face_list)):
        face = face_list[i]
        poly_vertices = [0, 1, 2]
        # if a face isn't a tri, split it into tris using the fan algo
        for j in range(len(face)-2):
            #print(poly_vertices)
            polygon = []
            face_points = []
            uv_points = []
            # this needs to be offset based on k and j, maybe a list of vertex indexes?
            for k in range(3):
                vertex_index = face[poly_vertices[k]][0]-1
                face_points.append(vertex_list[vertex_index])
                uv_points.append(uv_list[vertex_index])
            polygon.append(face_points)
            normal = vertex_normal_list[face[0][2]-1]
            polygon.append(normal)
            polygon.append(uv_points)
            model.append(polygon)
            poly_vertices.pop(1)
            poly_vertices.append(poly_vertices[-1]+1)
    # format: points, normal vector, uv_points
    #for poly in model:
    #    print(poly)
    return model
