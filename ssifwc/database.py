import psycopg2
from psycopg2.extras import RealDictCursor


class Database:

    def __init__(self, connection, cursor):
        """
        :type connection: psycopg2.extensions.connection
        :type cursor: psycopg2.extensions.cursor
        """

        self._connection = connection
        self._cursor = cursor

    @classmethod
    def connect(cls, connection_uri):
        """"
        :type connection_uri: str
        :rtype: epicollect_migrator.database.Database
        """

        connection = psycopg2.connect(connection_uri)
        return cls(connection, connection.cursor(cursor_factory=RealDictCursor))

    def close(self):
        self._connection.commit()
        self._cursor.close()
        self._connection.close()

    def select_watersheds(self):

        sql = "SELECT id, 'watershed' AS name, geom coordinates FROM watersheds"

        return self._fetchall(sql)

    def select_epicollect(self):

        sql = 'SELECT uuid id, title, where_am_i point, ph, temperature, conductivity FROM epicollect_observations'

        return self._fetchall(sql)

    def select_aquifers(self):

        sql = 'SELECT id, name, geom coordinates FROM aquifers'

        return self._fetchall(sql)

    def select_culverts(self):

        sql = "SELECT id, name, geom coordinates FROM culverts"

        return self._fetchall(sql)

    def select_faults(self):

        sql = "SELECT id, name, geom coordinates FROM faults"

        return self._fetchall(sql)

    def select_greenwood(self):

        sql = "SELECT id, 'greenwood' AS name, geom coordinates FROM greenwood"

        return self._fetchall(sql)

    def select_epicollect_points_by_uuids(self, uuids):

        sql = """
            SELECT 
                uuid id, 
                title, 
                where_am_i point, 
                named_location_if_known, 
                water_matters, 
                watershed, 
                created_at,
                last_significant_precipitation_event, 
                safe_to_work_at_this_location, 
                name_initials_or_nickname,
                type_of_visit, 
                water_body_type, 
                likely_permenance, 
                rate_of_flow_qualitative, 
                flow_rate_quantity_1,
                flow_rate_quantity_2, 
                flow_rate_quantity_3, 
                ph, 
                temperature, 
                conductivity, 
                other_comments
            FROM epicollect_observations
            WHERE uuid::text = ANY(%s)
        """
        self._cursor.execute(sql, (uuids,))
        return self._cursor.fetchall()

    def _fetchall(self, sql):

        self._cursor.execute(sql)
        return self._cursor.fetchall()
