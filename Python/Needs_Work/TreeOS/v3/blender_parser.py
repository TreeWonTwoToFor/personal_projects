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
        if file_dict[line_number].split()[0] == data_type:
            start_found = True
        else:
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

def get_model(file_name):
    text = read_blender_file(file_name)
    file_dict = get_file_dictionary(text)
    vertex_list = []
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
    for face in face_list:
        face_points = []
        for i in range(len(face)):
            vertex_index = face[i]-1
            face_points.append(vertex_list[vertex_index])
        model.append(face_points)
    return model

if __name__ == '__main__':
    file_name = input("Enter file name: ")
    file_extension = file_name.split('.')[-1]
    if file_extension == "obj":
        text = read_blender_file(file_name)
        file_dict = get_file_dictionary(text)
        for vertex in get_data(file_dict, 'v'):
            print("v: " + str(vertex.split()[1:]))
        print()
        for face in get_data(file_dict, 'f'):
            print("f: ", end = "")
            for point in face.split()[1:]:
                print(point[0], end = " ")
            print()
    else:
        print("This program only supports obj files.")
