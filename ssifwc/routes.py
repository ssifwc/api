import os
import json
from enum import Enum

from ssifwc.epicollect import Epicollect
from ssifwc.precipitation import Precipitation
from ssifwc.helpers import serialise_polygons, serialise_points, serialise_lines, json_serial

precipitation = Precipitation('http://www.victoriaweather.ca')


class Resource(Enum):

    Epicollect = 'epicollect'
    Watersheds = 'watersheds'
    Wells = 'wells'
    Springs = 'springs'
    Parcels = 'parcels'
    Aquifers = 'aquifers'
    Faults = 'faults'
    Greenwood = 'greenwood'
    Metrics = 'metrics'


class Router:

    def __init__(self, database):

        self._database = database

    def get_watersheds(self):

        watersheds = self._database.select_watersheds()
        polygons = serialise_polygons(watersheds)

        return self._create_response(polygons)

    def get_waterwells(self):

        water_wells = self._database.select_waterwells()
        points = serialise_points(water_wells)

        return self._create_response(points)

    def get_springs(self):

        springs = self._database.select_springs()
        points = serialise_points(springs)

        return self._create_response(points)

    def get_epicollect(self):

        epicollect = self._database.select_epicollect()
        points = serialise_points(epicollect)

        return self._create_response(points)

    def get_aquifers(self):

        aquifers = self._database.select_aquifers()
        polygons = serialise_polygons(aquifers)

        return self._create_response(polygons)

    def get_parcels(self):

        parcels = self._database.select_parcels()
        polygons = serialise_polygons(parcels)

        return self._create_response(polygons)

    def get_faults(self):

        faults = self._database.select_faults()
        lines = serialise_lines(faults)

        return self._create_response(lines)

    def get_greenwood(self):

        greenwood = self._database.select_greenwood()
        polygons = serialise_polygons(greenwood)

        return self._create_response(polygons)

    def get_epicollect_points_by_uuids(self, body):

        uuids = body['uuids']

        if body['version'] == "2":
            epicollect = self._database.select_epicollect_v2_points_by_uuids(uuids)
        else:
            epicollect = self._database.select_epicollect_points_by_uuids(uuids)

        points = serialise_points(epicollect)

        return self._create_response(points)

    def get_metrics_by_epicollect_uuid(self, body):

        metrics = self._database.select_metrics(uuid=body['uuid'], radius=body['radius'])
        created_at = metrics['created_at']

        temperature = [{'value': value, 'name': time} for (value, time) in zip(metrics['temperature'], created_at)]
        conductivity = [{'value': value, 'name': time} for (value, time) in zip(metrics['conductivity'], created_at)]
        ph = [{'value': value, 'name': time} for (value, time) in zip(metrics['ph'], created_at)]
        flow_rate = [{'value': value, 'name': time} for (value, time) in zip(metrics['flow_rate'], created_at)]
        alkalinity = [{'value': value, 'name': time} for (value, time) in zip(metrics['alkalinity'], created_at)]
        hardness = [{'value': value, 'name': time} for (value, time) in zip(metrics['hardness'], created_at)]
        dissolved_oxygen = [{'value': value, 'name': time} for (value, time) in zip(metrics['dissolved_oxygen'], created_at)]

        min_date, max_date = temperature[0]['name'], temperature[-1]['name']

        return self._create_response(
            {'temperature': temperature,
             'conductivity': conductivity,
             'ph': ph,
             'flow_rate': flow_rate,
             'precipitation': precipitation.get_data(min_date, max_date),
             'alkalinity': alkalinity,
             'hardness': hardness,
             'dissolved_oxygen': dissolved_oxygen
             })

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
