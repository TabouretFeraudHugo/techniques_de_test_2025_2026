import pytest

# Test for the function well catchs
def test_PointManager_communication():
    # Test the well communication with the other API, if not, triggers a 503 error

def test_PointSetID_format():
    # Test for the right format for the pointsetid first catch, if not triggers a 400 error (invalid PoinSetID format)
    # Structure of point set:
    #   - 4 bytes (unsigned_long) for the numbers of points in the figure
    #   - 2 x 4 bytes (unsigned long) for each vertice of the set, the first 4 is a float for the X coodinate, then it's Y coordinate

def test_PointSetID_exists():
    # Test if the pointSet given exists, if not, returns a 404 error



# Tests for the function well doing
def test_Triangle_value():
    # Set of tests with the insert value, and awaited values

def test_Triangle_responses():
    # Set of test that sends values and check if the return are the right ones
    # responses checked are : 200 (sucessful), 500 (triangulation failed)



# Tests for the function well returns
def test_Triangles_format():
    # Test for the right structured format of the answer
    # Structure of triangles:
    #   - 4 bytes (unsigned_long) for the numbers of points in the figure
    #   - 3 x 4 bytes (unsigned long) for each vertice of the triangle, wich is the id of the vertex

