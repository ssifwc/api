from shapely import wkb
from datetime import datetime, date


def serialise_points(points):

    return _serialise_geometries(points, 'point', _load_point)


def serialise_lines(lines):

    return _serialise_geometries(lines, 'coordinates', _load_line)


def serialise_polygons(polygons):

    return _serialise_geometries(polygons, 'coordinates', _load_polygon)


def _serialise_geometries(geometries, key_name, load_method):

    geometry_list = []
    for geometry in geometries:
        if geometry[key_name]:
            geometry[key_name] = load_method(geometry[key_name])
            geometry_list.append(geometry)

    return geometry_list


def _load_point(wkb_point):

    return list(wkb.loads(wkb_point, hex=True).coords)[0][::-1]


def _load_line(wkb_line):

    return _lng_lat_to_lat_lng(list(wkb.loads(wkb_line, hex=True).coords))


def _load_polygon(wkb_polygon):

    return _lng_lat_to_lat_lng(list(wkb.loads(wkb_polygon, hex=True).exterior.coords))


def _lng_lat_to_lat_lng(polygon):

    return [[point[1], point[0]] for point in polygon]


def json_serial(obj):

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
