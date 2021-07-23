# import MySQLdb
import psycopg2
import psycopg2.extras
# import MySQLdb.cursors
# import _mysql_exceptions
import inspect
import queue
import backoff
from dashboard.utils import Timer

class PostgreSQLClient:

    def __init__(self, config, logger, pool_size=3):
        self.config = config
        self.logger = logger
        self.pool = queue.Queue()
        for _ in range(pool_size):
            self.pool.put(self.create_connection())

    def create_connection(self):
        # conn = MySQLdb.connect(
        conn = psycopg2.connect(
                host=self.config['AIRFLOW_DB_HOST'],
                user=self.config['AIRFLOW_USERNAME'],
                password=self.config['AIRFLOW_PASSWORD'],
                dbname=self.config['AIRFLOW_DATABASE'],
                # cursorclass=MySQLdb.cursors.DictCursor,
                cursor_factory=psycopg2.extras.DictCursor,
                connect_timeout=3
            )
        # conn.autocommit(True)
        # conn.execute()
        return conn

    # @backoff.on_exception(backoff.expo, _mysql_exceptions.OperationalError, max_tries=4)
    @backoff.on_exception(backoff.expo, psycopg2.OperationalError, max_tries=4)
    def query(self, query):
        cursor = None
        conn = self.pool.get(True)
        try:
            print(f"---Query is--- {query}")
            with Timer(self.logger, f"MySQL query {query}"):
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        # except _mysql_exceptions.OperationalError:
        except psycopg2.OperationalError as e:
            conn = self.create_connection() # recreate connection
            raise
        finally:
            if cursor is not None:
                cursor.close()
            self.pool.put(conn)

# class MySQLClient:
#
#     def __init__(self, config, logger, pool_size=3):
#         self.config = config
#         self.logger = logger
#         self.pool = queue.Queue()
#         for _ in range(pool_size):
#             self.pool.put(self.create_connection())
#
#     def create_connection(self):
#         conn = MySQLdb.connect(
#                 host=self.config['AIRFLOW_DB_HOST'],
#                 user=self.config['AIRFLOW_USERNAME'],
#                 password=self.config['AIRFLOW_PASSWORD'],
#                 db=self.config['AIRFLOW_DATABASE'],
#                 cursorclass=MySQLdb.cursors.DictCursor,
#                 connect_timeout=3
#             )
#         conn.autocommit(True)
#         return conn
#
#     @backoff.on_exception(backoff.expo, _mysql_exceptions.OperationalError, max_tries=4)
#     def query(self, query):
#         cursor = None
#         conn = self.pool.get(True)
#         try:
#             with Timer(self.logger, f"MySQL query {query}"):
#                 cursor = conn.cursor()
#                 cursor.execute(query)
#                 return cursor.fetchall()
#         except _mysql_exceptions.OperationalError:
#             conn = self.create_connection() # recreate connection
#             raise
#         finally:
#             if cursor is not None:
#                 cursor.close()
#             self.pool.put(conn)
