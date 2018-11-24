import os
import json

from ssifwc.database import Database
from ssifwc.routes import Router, Resource

database = Database.connect(os.environ['DATABASE_CONNECTION_URI'])
router = Router(database)

get_routes = {
    Resource.Watersheds.value: router.get_watersheds,
    Resource.Epicollect.value: router.get_epicollect,
    Resource.Aquifers.value: router.get_aquifers,
    Resource.Parcels.value: router.get_parcels,
    Resource.Faults.value: router.get_faults,
    Resource.Greenwood.value: router.get_greenwood,
    Resource.Springs.value: router.get_springs,
    Resource.Wells.value: router.get_waterwells
}

post_routes = {
    Resource.Epicollect.value: router.get_epicollect_points_by_uuids,
    Resource.Image.value: router.get_epicollect_image_by_id
}


def endpoint(event, _):

    resource = event['resource'].replace('/', '')
    method = event['httpMethod']

    if method == 'GET':
        return get_routes[resource]()
    elif method == 'POST':
        body = json.loads(event['body'])
        return post_routes[resource](body)
