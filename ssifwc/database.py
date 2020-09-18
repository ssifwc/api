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

    def select_watersheds(self):

        sql = """
        select id, geom coordinates, json_build_object('name', name) meta
        from watersheds_crd
        """

        return self._fetchall(sql)

    def select_waterwells(self):

        sql = """
        select id, geom point, 
        json_build_object('water_depth', water_depth, 'bedrock_depth', bedrock_depth, 'elevation', elevation, 
                          'general_remarks', general_remarks, 'yield_value', yield_value, 'url', url) meta
        from wells
        """
        return self._fetchall(sql)

    def select_springs(self):

        sql = """
        select id, geom point, 
        json_build_object('stream_name', stream_name, 'purpose', purpose, 'quantity', quantity, 'units', units) meta
        from spring 
        """

        return self._fetchall(sql)

    def select_parcels(self):

        sql = """
        select id, geom coordinates, json_build_object() meta
        from parcel
        """
        return self._fetchall(sql)

    def select_epicollect(self):

        sql = """
        SELECT uuid id, title, where_am_i point, ph, temperature, conductivity, '1' epicollect_version
        FROM epicollect_observations
        union
        select uuid id, title, coord point, cast(nullif(ph, '') as double precision), cast(nullif(temperature, '') as double precision), cast(nullif(conductivity, '') as double precision), '2' epicollect_version
        from epicollect_observations_v2
        """

        return self._fetchall(sql)

    def select_aquifers(self):

        sql = """
        select id, geom coordinates,
        json_build_object('materials', materials, 'productivity', productivity, 'vulnerability', vulnerability, 
        'demand', demand, 'location_description', location_description, 'url', url, 'type_of_water_use', type_of_water_use) meta
        from aquifers
        """

        return self._fetchall(sql)

    def select_faults(self):

        sql = "SELECT id, name, geom coordinates FROM faults"

        return self._fetchall(sql)

    def select_greenwood(self):

        sql = """
        select id, geom coordinates, json_build_object('name', name, 'description', description) meta
        from geology
        """

        return self._fetchall(sql)

    def select_epicollect_points_by_uuids(self, uuids):
        try:
            sql = """
            select
                uuid AS id,
                json_record ->> 'title' AS title,
                json_record ->> 'coordinates' AS point,
                json_record ->> 'monitor_location' AS named_location_if_known,
                null island_area,
                json_record ->> 'created_at' AS created_at,
                json_record ->> 'last_sign_precip' AS last_significant_precipitation_event,
                json_record ->> 'safe_to_work' AS safe_to_work_at_this_location,
                json_record ->> 'name' AS name_initials_or_nickname,
                json_record ->> 'visit_type' AS type_of_visit,
                json_record ->> 'water_body' AS water_body_type,
                json_record ->> 'rate_of_flow' AS rate_of_flow_qualitative,
                flow_rate AS flow_rate_average,
                json_record ->> 'ph_oakton' AS ph,
                array[json_record ->> 'photo_record', json_record ->> 'photo_pond', json_record ->> 'photo_ds', json_record ->> 'photo_us'] AS photos,
                json_record ->> 'temperature' AS temperature,
                json_record ->> 'conductivity' AS conductivity,
                json_record ->> 'other_comments' AS other_comments
            from field_observations
            where uuid::text = any(%s)
            """

            self._cursor.execute(sql, (uuids,))
            return self._cursor.fetchall()
        except:
            self.rollback()

    def select_metrics(self, uuid, radius):
        try:
            sql = """
                with buffer as (
                    select ST_Transform(ST_Buffer(ST_Transform(ST_SetSRID(where_am_i, 4326), 3857), %s), 4326) geom
                    from v_all_points
                    where uuid = %s
                )
                select
                    array_agg(created_at) created_at,
                    array_agg(temperature) temperature,
                    array_agg(conductivity) conductivity,
                    array_agg(ph) ph,
                    array_agg(flow_rate) flow_rate,
                    array_agg(alkalinity) alkalinity,
                    array_agg(hardness) hardness,
                    array_agg(dissolved_oxygen) dissolved_oxygen
                from (
                    select created_at, temperature, conductivity, ph, flow_rate, alkalinity, hardness, dissolved_oxygen
                    from buffer, v_all_points points
                    where ST_Within(ST_SetSRID(points.where_am_i, 4326), buffer.geom)
                    order by created_at
                ) v
            """
            self._cursor.execute(sql, (radius, uuid,))
            return self._cursor.fetchone()
        except:
            self.rollback()

    def rollback(self):
        if self._cursor is not None:
            self._cursor.close()
        if self._connection is not None:
            self._connection.rollback()

    def _fetchall(self, sql):
        try:
            self._cursor.execute(sql)
            return self._cursor.fetchall()
        except:
            self.rollback()
