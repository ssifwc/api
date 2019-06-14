from shapely import wkb
from shapely.geometry.collection import GeometryCollection
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
        try:
            if geometry[key_name]:
                geometry[key_name] = load_method(geometry[key_name])
                geometry_list.append(geometry)
        except AttributeError:
            continue

    return geometry_list


def _load_point(wkb_point):

    return list(wkb.loads(wkb_point, hex=True).coords)[0][::-1]


def _load_line(wkb_line):

    return _lng_lat_to_lat_lng(list(wkb.loads(wkb_line, hex=True).coords))


def _load_polygon(wkb_polygon):

    geometry = wkb.loads(wkb_polygon, hex=True)

    if geometry.geom_type == 'MultiPolygon':
        return [_lng_lat_to_lat_lng(list(polygon.exterior.coords)) for polygon in geometry]
    else:
        return _lng_lat_to_lat_lng(list(geometry.exterior.coords))


def _lng_lat_to_lat_lng(polygon):

    return [[point[1], point[0]] for point in polygon]


def json_serial(obj):

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
