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


def triangulate(polygons):
    tris = []
    camera = Camera.Camera((0,0,0), (0,0,0), True)
    for poly in polygons:
        verts = poly[0]
        if len(verts) == 3:
            tris.append(poly)
        else:
            # order the vertecies based on their winding order
            projected_points = []
            angle_list = []
            centroid = [0,0]
            for point in verts:
                value = list(Draw.perspective_projection([100,100], point, camera))
                projected_points.append(value)
                #centroid[0] += value[0]
                #centroid[1] += value[1]
            centroid[0] /= len(verts)
            centroid[1] /= len(verts)
            for point in projected_points:
                for i in range(2): point[i] -= centroid[i]
                angle_list.append(numpy.arctan2(point[1], point[0]))
            zipped_list = zip(angle_list, verts)
            sorted_pairs = sorted(zipped_list)
            sorted_sorting_list, sorted_list_to_sort = zip(*sorted_pairs)
            s_verts = list(sorted_list_to_sort)
            #s_verts.reverse()
            # fan triangulation (simple for convex polygons)
            for i in range(1, len(s_verts)-1):
                tris.append([[s_verts[0], s_verts[i], s_verts[i+1]], poly[1]])
    return tris


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
    test_model = get_model("./blender_files/pentagon.obj")
    print(test_model)
    print()
    print(triangulate(test_model))
