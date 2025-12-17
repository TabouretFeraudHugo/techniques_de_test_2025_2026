import struct
import pytest
import src.main as main


def _generate_point_set(num_points=3):
    """Create a binary PointSet with `num_points` points."""
    if num_points < 0:
        num_points = 0
    data = struct.pack('<I', num_points)
    for i in range(num_points):
        data += struct.pack('<ff', float(i + 0.1), float(i + 0.2))
    return data


@pytest.fixture()
def flask_ctx():
    """Push a Flask request context so `flask.jsonify` returns usable responses."""
    ctx = main.app.test_request_context()
    ctx.push()
    yield
    ctx.pop()


# Parametrized tests covering statuses: 200, 400, 404, 500, 503
# Each tuple: (index, data_list, connection_ok, expected_status, expected_code, expected_message)
# Better than just having separate function for each case with only one parameter different.
@pytest.mark.parametrize(
    "idx,data_list,connection_ok,expected_status,expected_code,expected_message",
    [
        # 200: connection ok, valid pointset, triangulate succeeds
        (0, [{"pointSet": _generate_point_set(3)}], True, 200, "triangulation successful", None),
        (1, [None,{"pointSet": _generate_point_set(5)}], True, 200, "triangulation successful", None),
        (2, [None, None, {"pointSet": _generate_point_set(100)}], True, 200, "triangulation successful", None),
        (3, [None, None, None,{"pointSet": _generate_point_set(1000)}], True, 200, "triangulation successful", None),
        # 400: connection ok, bad format -> force decode_point_set to return 0
        (4, [None, None, None, None, {"pointSet": b"bad-format-bytes"}], True, 400, "WRONG_FORMAT", "Invalid PointSetID format"),
        # 404: connection ok, pointset not found (falsy response)
        (5, [None, None, None, None, None, None], True, 404, "NOT_FOUND", "PointSetID not found"),
        # 500: connection ok, valid decode, triangulation fails
        (6, [None, None, None, None, None, None, {"pointSet": _generate_point_set(2)}], True, 500, "TRIANGULATION_FAILED", "Triangulation algorithm failed"),
        # 503: connection fails
        (7, [None, None, None, None, None, None, None, {"pointSet": _generate_point_set(4)}], False, 503, "SERVER_ERROR", "Cannot reach the PointSet server"),
    ],
)
def test_triangulation_status_codes(flask_ctx, monkeypatch, idx, data_list, connection_ok,expected_status, expected_code, expected_message):
    """Call `triangulationPointSetId` with mocked connection and fecthPointSet to emulate various scenarios."""

    monkeypatch.setattr(main, "connection", lambda: connection_ok)
    monkeypatch.setattr(main, "fetch_point_set", lambda pid: data_list[idx])

    # Get the function response and status from the server
    resp, status = main.triangulationPointSetId(str(idx))
    assert status == expected_status

    # Check for code 
    json_data = resp.get_json()
    if expected_code is not None:
        assert isinstance(json_data, dict)
        assert json_data.get("code") == expected_code

    # Check for message
    if expected_message is not None:
        assert isinstance(json_data, dict)
        assert json_data.get("message") == expected_message
