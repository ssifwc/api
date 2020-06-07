import unittest
import os
from test.support import EnvironmentVarGuard

from ssifwc.database import Database


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set('DATABASE_CONNECTION_URI', 'postgresql://postgres:password@localhost:5432/postgres')

    def test_metrics_fails_resets_db_connection(self):
        db = Database.connect(os.environ['DATABASE_CONNECTION_URI'])
        self.assertIsNotNone(db)
        try:
            print(db.select_metrics('invalid-uuid-will-crash-query', 10))
        except:
            db.select_metrics('1d688da7-2d2c-4f4d-8c9d-5eec4893ad3d', 10)
            self.assertIsNotNone(db)
            db.select_metrics('1d688da7-2d2c-4f4d-8c9d-5eec4893ad3d', 10)

    def test_select_epicollect_points_by_uuids_resets_db_connection(self):
        db = Database.connect(os.environ['DATABASE_CONNECTION_URI'])
        self.assertIsNotNone(db)
        try:
            print(db.select_epicollect_points_by_uuids({'invalid-uuid-will-crash-query'}))
        except:
            db.select_metrics({'1d688da7-2d2c-4f4d-8c9d-5eec4893ad3d'}, 10)
            self.assertIsNotNone(db)
            db.select_epicollect_points_by_uuids({'invalid-uuid-will-crash-query'})

    def test_select_epicollect_v2_points_by_uuids_resets_db_connection(self):
        db = Database.connect(os.environ['DATABASE_CONNECTION_URI'])
        self.assertIsNotNone(db)
        try:
            print(db.select_epicollect_v2_points_by_uuids({'invalid-uuid-will-crash-query'}))
        except:
            db.select_metrics({'1d688da7-2d2c-4f4d-8c9d-5eec4893ad3d'}, 10)
            self.assertIsNotNone(db)
            db.select_epicollect_v2_points_by_uuids({'invalid-uuid-will-crash-query'})


if __name__ == '__main__':
    unittest.main()
