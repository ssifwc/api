import requests


class Precipitation:

    def __init__(self, url):

        self._url = url

    def get_data(self):

        precipitation_2018 = self._get_precipitation_for_year('2018')
        precipitation_2019 = self._get_precipitation_for_year('2019')

        return [
            {'name': precip_2018['name'],
             '2018': precip_2018['value'],
             '2019': precip_2019['value']}
            for precip_2018, precip_2019 in zip(precipitation_2018, precipitation_2019)
        ]

    def _get_precipitation_for_year(self, year):

        response = requests.get(f'{self._url}/data/{year}/raintotal_year_0121_{year}.csv')

        rows = response.text.split('\n')
        months = rows[1].split(',')[1:]

        weather = []
        for i, month in enumerate(months):

            precipitation = 0
            for row in rows[2:]:

                try:
                    value = float(row.split(',')[i + 1].strip())
                    if value == -99:
                        value = 0
                    precipitation = precipitation + value
                except IndexError:
                    continue

            weather.append({'name': month, 'value': precipitation})

        return weather
