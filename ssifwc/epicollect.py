import requests


class Epicollect:

    def __init__(self, base_url, project_name, client_id, client_secret):
        self._base_url = base_url
        self._search_endpoint = f'{base_url}/api/export/entries/{project_name}'
        self._media_endpoint = f'{self._base_url}/api/export/media/{project_name}'
        self._client_id = client_id
        self._client_secret = client_secret

    def get_media_url(self, image_id):

        url = f'{self._media_endpoint}?type=photo&format=entry_original&name={image_id}'

        return url, self._get_token()

    def _get_token(self):
        params = {
            'grant_type': 'client_credentials',
            'client_id': self._client_id,
            'client_secret': self._client_secret
        }

        response = requests.post(f'{self._base_url}/api/oauth/token', data=params)

        return response.json()['access_token']
