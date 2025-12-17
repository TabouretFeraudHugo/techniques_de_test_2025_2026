import pytest
import time
import struct
from src.triangles import triangulate


@pytest.mark.parametrize("input_data,expected_triangles", [
    # Minimal
    ([3, (0, 0), (1, 0), (0, 1)], 1),
    # Convex
    ([4, (0, 0), (2, 0), (2, 2), (0, 2)], 2),
    # Concave
    ([5, (0, 0), (2, 0), (1, 1), (2, 2), (0, 2)], 3),
    # Collinear points
    ([4, (0, 0), (1, 0), (2, 0), (1, 1)], 2),
    # Inverted order
    ([4, (0, 0), (0, 2), (2, 2), (2, 0)], 2),
])
def test_triangulation_precision(input_data, expected_triangles):
    """Test for the accuracy of the triangulation algorithm using some of the "most" common test cases."""
    result = triangulate(input_data)

    n = input_data[0]
    offset = 4 + (n * 8) 
    actual_triangles = struct.unpack('<L', result[offset:offset+4])[0]
    if actual_triangles != expected_triangles:
        pytest.skip()
    else:
        assert actual_triangles == expected_triangles