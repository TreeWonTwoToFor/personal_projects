from PIL import Image

def load_texture(file_name):
    img = Image.open(file_name)
    return (img.size, list(img.getdata()))

def draw_polygon(screen, points, texture, light_val):
    # get some basic information about the buffer and texture
    pygame_buffer = screen.get_buffer()
    buffer = memoryview(pygame_buffer)
    width, height = screen.get_size()
    tex_size, tex_data = texture
    tex_w, tex_h = tex_size
    # unpack triangle (we currently don't do any depth testing, so we ignore the 'z' values)
    (x0, y0, _, u0, v0) = points[0]
    (x1, y1, _, u1, v1) = points[1]
    (x2, y2, _, u2, v2) = points[2]
    # bounding box
    min_x = max(int(min(x0, x1, x2)), 0)
    max_x = min(int(max(x0, x1, x2)), width)
    min_y = max(int(min(y0, y1, y2)), 0)
    max_y = min(int(max(y0, y1, y2)), height)
    # edge function coefficients
    def edge_coeffs(xa, ya, xb, yb):
        A = ya - yb
        B = xb - xa
        C = xa * yb - xb * ya
        return A, B, C
    e0 = edge_coeffs(x1, y1, x2, y2)
    e1 = edge_coeffs(x2, y2, x0, y0)
    e2 = edge_coeffs(x0, y0, x1, y1)
    # triangle area (for barycentrics)
    area = (x1 - x0)*(y2 - y0) - (x2 - x0)*(y1 - y0)
    if area == 0:
        return
    inv_area = 1.0 / area
    # precompute UV gradients
    du_dx = ((u1 - u0)*(y2 - y0) - (u2 - u0)*(y1 - y0)) * inv_area
    du_dy = ((u2 - u0)*(x1 - x0) - (u1 - u0)*(x2 - x0)) * inv_area
    dv_dx = ((v1 - v0)*(y2 - y0) - (v2 - v0)*(y1 - y0)) * inv_area
    dv_dy = ((v2 - v0)*(x1 - x0) - (v1 - v0)*(x2 - x0)) * inv_area
    # starting values at (min_x, min_y)
    def edge_value(e, x, y):
        A, B, C = e
        return A * x + B * y + C
    row_e0 = edge_value(e0, min_x, min_y)
    row_e1 = edge_value(e1, min_x, min_y)
    row_e2 = edge_value(e2, min_x, min_y)
    # starting UV at (min_x, min_y)
    u_row = u0 + (min_x - x0) * du_dx + (min_y - y0) * du_dy
    v_row = v0 + (min_x - x0) * dv_dx + (min_y - y0) * dv_dy
    for y in range(min_y, max_y):
        # get the edge and UV values for our row
        e0_val = row_e0
        e1_val = row_e1
        e2_val = row_e2
        u = u_row
        v = v_row
        for x in range(min_x, max_x):
            # are we in the triangle?
            if e0_val >= 0 and e1_val >= 0 and e2_val >= 0:
                # sample texture
                px = int(u * (tex_w - 1))
                py = int((1 - v) * (tex_h - 1))
                # are we inside the texture?
                if 0 <= px < tex_w and 0 <= py < tex_h:
                    # index into our texture
                    idx_tex = py * tex_w + px
                    r, g, b = tex_data[idx_tex]
                    # change the RGB values based on our lighting
                    r = int(r * light_val)
                    g = int(g * light_val)
                    b = int(b * light_val)
                    # put values into the buffer
                    idx = (x + y * width) * 4
                    buffer[idx]     = b
                    buffer[idx + 1] = g
                    buffer[idx + 2] = r
                    buffer[idx + 3] = 0
            # step in x
            e0_val += e0[0]
            e1_val += e1[0]
            e2_val += e2[0]
            u += du_dx
            v += dv_dx
        # step in y
        row_e0 += e0[1]
        row_e1 += e1[1]
        row_e2 += e2[1]
        u_row += du_dy
        v_row += dv_dy
