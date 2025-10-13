import psycopg2

"""
Dictionary indices:
- int: osmid
- float: x
- float: y
- highway: enum
"""

class data_insertion:
    def insert_node(self, node, db_name, db_user, db_pass, db_host, db_port):
        conn = psycopg2.connect(database=db_name,
                                user=db_user,
                                password=db_pass,
                                host=db_host,
                                port=db_port)
        params = (node['osmid'], node['x'], node['y'], node['highway'])
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nodes (osmid, x, y, highway)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (osmid) DO NOTHING;
            """,
            params
        )

