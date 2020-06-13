import unittest

import datetime

from ssifwc.precipitation import Precipitation


class PrecipitationTest(unittest.TestCase):

    def test_get_precipitation(self):
        data = Precipitation().get_data(datetime.datetime(2018, 1, 1), datetime.datetime(2020, 12, 31))
        self.assertTrue(data)


if __name__ == '__main__':
    unittest.main()
