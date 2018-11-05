import json
from enum import Enum

from ssifwc.helpers import serialise_polygons, serialise_points, serialise_lines, json_serial


class Resource(Enum):

    Epicollect = 'epicollect'
    Watersheds = 'watersheds'
    Aquifers = 'aquifers'
    Culverts = 'culverts'
    Faults = 'faults'
    Greenwood = 'greenwood'


class Router:

    def __init__(self, database):

        self._database = database

    def get_watersheds(self):

        watersheds = self._database.select_watersheds()
        polygons = serialise_polygons(watersheds)

        return self._create_response(polygons)

    def get_epicollect(self):

        epicollect = self._database.select_epicollect()
        points = serialise_points(epicollect)

        return self._create_response(points)

    def get_aquifers(self):

        aquifers = self._database.select_aquifers()
        polygons = serialise_polygons(aquifers)

        return self._create_response(polygons)

    def get_culverts(self):

        culverts = self._database.select_culverts()
        points = serialise_points(culverts)

        return self._create_response(points)

    def get_faults(self):

        faults = self._database.select_faults()
        lines = serialise_lines(faults)

        return self._create_response(lines)

    def get_greenwood(self):

        greenwood = self._database.select_greenwood()
        points = serialise_points(greenwood)

        return self._create_response(points)

    def get_epicollect_points_by_uuids(self, body):

        epicollect = self._database.select_epicollect_points_by_uuids(uuids=body['uuids'])
        points = serialise_points(epicollect)

        return self._create_response(points)

    @staticmethod
    def _create_response(body):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body, default=json_serial),
            "headers": headers
        }

        return response
