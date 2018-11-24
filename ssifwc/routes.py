import os
import json
from enum import Enum

from ssifwc.epicollect import Epicollect
from ssifwc.helpers import serialise_polygons, serialise_points, serialise_lines, json_serial


class Resource(Enum):

    Epicollect = 'epicollect'
    Watersheds = 'watersheds'
    Aquifers = 'aquifers'
    Culverts = 'culverts'
    Faults = 'faults'
    Greenwood = 'greenwood'
    Image = 'image'


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

    def get_epicollect_image_by_id(self, body):

        epicollect = Epicollect(
            base_url=os.environ['EPICOLLECT_BASE_URL'],
            project_name=os.environ['EPICOLLECT_PROJECT_NAME'],
            client_id=os.environ['EPICOLLECT_CLIENT_ID'],
            client_secret=os.environ['EPICOLLECT_CLIENT_SECRET']
        )

        url, access_token = epicollect.get_media_url(image_id=body['id'])

        return self._create_response({'url': url, 'access_token': access_token})

    def _create_response(self, body):

        return {
            "statusCode": 200,
            "body": json.dumps(body, default=json_serial),
            "headers": self._get_headers()
        }

    @staticmethod
    def _get_headers():
        return {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        }
