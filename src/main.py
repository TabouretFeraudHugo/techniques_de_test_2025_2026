import flask
import struct
import requests
import src.triangles as triangles

app = flask.Flask(__name__)

@app.route('/triangulation')
def triangulation():
    """Base route for triangulation service."""
    return flask.jsonify({"triangulation up"}), 400

@app.route('/triangulation/{pointSetId}')
def triangulationPointSetId(pointSetID):
    """Connect to the PointSet server, fetch the PointSet, decode it, and perform triangulation."""
    # Check connection to PointSet server
    conn = connection()
    if not conn:
        return flask.jsonify({"code":"SERVER_ERROR","message":"Cannot reach the PointSet server"}), 503
    
    # Get the PointSet from the server
    response = fetch_point_set(pointSetID)
    if not response:
        return flask.jsonify({"code":"NOT_FOUND","message":"PointSetID not found"}), 404
    pointSetValues = decode_point_set(response["pointSet"])
    if pointSetValues == 0:
        return flask.jsonify({"code":"WRONG_FORMAT","message":"Invalid PointSetID format"}), 400
    
    # Here is be the triangulation algorithm call
    result = triangles.triangulate(pointSetValues)
    if not result: 
        return flask.jsonify({"code":"TRIANGULATION_FAILED","message":"Triangulation algorithm failed"}), 500
    return flask.jsonify({"code":"triangulation successful","value":"..."}), 200


def decode_point_set(pointSet) :
    """Decode the PointSet, if it's not the right format, return 0"""
    pointSetDecoded = []
    n = struct.unpack('<I', pointSet[:4])[0]
    if not(isinstance(n,int)):
        return 0
    
    pointSetDecoded.append(n)

    offset = 4
    for _ in range(n):
        if not (isinstance(pointSet[offset:offset+8],bytes)) or len(pointSet[offset:offset+8])<8:
            return 0
        x, y = struct.unpack('<ff', pointSet[offset:offset+8])
        if not(isinstance(x, float)):
            return 0
        if not(isinstance(y,float)):
            return 0

        pointSetDecoded.append((x,y))
        offset += 8
    return pointSetDecoded

def connection():
    """Make a test connection to the PointSet server on the base route."""
    response = requests.get("http://server/pointSetPointSetID/")
    return response
 
def fetch_point_set(point_set_id):
    """Fecth the PointSet data from the PointSet server."""
    response = requests.get(f"http://pointsetmanager/pointsets/{point_set_id}")
    if response.status_code == 200:
        return response.json()
    return None

def createApp():
    if __name__ == '__main__':
        app.run(debug=True, port=5000)
