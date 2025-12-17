import struct

# Calculating the signed area of a triangled
def signed_area(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

# Check if a point is inside a triangle
def point_in_triangle(p, a, b, c):
    d1 = signed_area(p, a, b)
    d2 = signed_area(p, b, c)
    d3 = signed_area(p, c, a)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

# Check if ear is valid
def is_ear(points, poly, i):
    n = len(poly)
    prev_i = (i - 1) % n
    next_i = (i + 1) % n
    
    a = points[poly[prev_i]]
    b = points[poly[i]]
    c = points[poly[next_i]]
    
    # Check if triangle abc is convexe, for that no other point should be inside
    for j in range(n):
        if j == prev_i or j == i or j == next_i:
            continue
        
        p = points[poly[j]]
        if point_in_triangle(p, a, b, c):
            return False
    
    return True

def triangulate(data):
    """
    Use the ear clipping algorithm to triangulate a polygon defined by the given points.
    
    Args:
        data: Liste [n, (x1,y1), (x2,y2), ...] n is the number of points, (xi,yi) are the coordinates.
    
    Returns:
        bytes: Representation like in the yml or None if less than 3 points or if there are no data at all.
    """
    if len(data) < 1:
        return None
    
    n = data[0]
    
    # Check for correct lenghth
    if n < 3:
        return None
    
    points = list(data[1:n+1])

    # Ear clipping algorithm
    polygon = list(range(n))
    triangles = []
    
    while len(polygon) > 3:
        ear_found = False
        
        for i in range(len(polygon)):
            if is_ear(points, polygon, i):
                # Add triangle
                prev_i = (i - 1) % len(polygon)
                next_i = (i + 1) % len(polygon)
                
                triangles.append((
                    polygon[prev_i],
                    polygon[i],
                    polygon[next_i]
                ))
                
                # Remove vertex from ear
                polygon.pop(i)
                ear_found = True
                break
        
        if not ear_found:
            break
    
    # Add the last triangle
    if len(polygon) == 3:
        triangles.append((polygon[0], polygon[1], polygon[2]))
       
    ### OUTPUT FORMATTING ###
    result = bytearray()
    
    # Part 1: Vertices
    result.extend(struct.pack('<L', n))  # Number of verticices
    
    for point in points:
        result.extend(struct.pack('<f', point[0]))  # X
        result.extend(struct.pack('<f', point[1]))  # Y
    
    # Part 2: Triangles
    num_triangles = len(triangles)
    result.extend(struct.pack('<L', num_triangles))  # Number of triangles
    
    for tri in triangles:
        result.extend(struct.pack('<L', tri[0]))  # Index vertex 1
        result.extend(struct.pack('<L', tri[1]))  # Index vertex 2
        result.extend(struct.pack('<L', tri[2]))  # Index vertex 3
    
    return bytes(result)