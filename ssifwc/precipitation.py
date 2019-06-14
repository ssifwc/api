import requests
from datetime import datetime


months_lookup = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}


class Precipitation:

    def __init__(self, url):

        self._url = url

    def get_data(self, min_date, max_date):

        precipitation_2019 = self._get_precipitation_for_year('2019', min_date, max_date)
        precipitation_2018 = self._get_precipitation_for_year('2018', min_date, max_date)

        return precipitation_2018 + precipitation_2019

    def _get_precipitation_for_year(self, year, min_date, max_date):

        response = requests.get(f'{self._url}/data/{year}/raintotal_year_0121_{year}.csv')

        rows = response.text.split('\n')
        months = rows[1].split(',')[1:]

        weather = []
        for i, month in enumerate(months):

            for row in rows[2:]:

                try:
                    day = row.split(',')[0].strip()
                    if len(day) == 1:
                        day = f'0{day}'
                    value = float(row.split(',')[i + 1].strip())
                    if value == -99:
                        value = None
                except IndexError:
                    continue
                try:
                    date = datetime.strptime(f'{day}/{months_lookup[month]}/{year}', '%d/%m/%Y')
                except ValueError:
                    continue

                if date >= min_date and date <= max_date:
                    weather.append({'name': date, 'value': value})

        return weather
