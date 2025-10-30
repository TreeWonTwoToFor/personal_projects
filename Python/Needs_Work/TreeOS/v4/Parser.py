import numpy

def read_blender_file(file_name):
    try:
        file = open(file_name)
        return file.read()
    except:
        raise FileNotFoundError("Could not find the file.")


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


# each data point in the model has a list of vertices, as well as the face normal
def get_model(file_name):
    text = read_blender_file(file_name)
    file_dict = get_file_dictionary(text)
    vertex_list = []
    face_normal_list = []
    face_list = []
    for vertex in get_data(file_dict, 'v'):
        final_vertex = []
        for number in vertex.split()[1:]:
            final_vertex.append(float(number))
        vertex_list.append(final_vertex)
    for face in get_data(file_dict, 'f'):
        final_face = []
        for point in face.split()[1:]:
            final_face.append(int(point.split('/')[0]))
        face_list.append(final_face)
    model = []
    # collects all vertecies in a face
    for i in range(len(face_list)):
        face = face_list[i]
        polygon = []
        face_points = []
        for j in range(len(face)):
            vertex_index = face[j]-1
            face_points.append(vertex_list[vertex_index])
        polygon.append(face_points)
        vector_a, vector_b = [], []
        for i in range(3):
            vector_a.append(round(face_points[0][i] - face_points[1][i], 4))
            vector_b.append(round(face_points[0][i] - face_points[2][i], 4))
        vector_a = numpy.array(vector_a)
        vector_b = numpy.array(vector_b)
        cp = numpy.cross(vector_a, vector_b)
        polygon.append(cp)
        model.append(polygon)
    return model


if __name__ == '__main__':
    model_face = get_model("./blender_files/monkey_face.obj")
    model = get_model("./blender_files/monkey.obj")
    for i in range(4):
        print(f"{i}:\n\t{model_face[i]}\n\t{model[i]}")
