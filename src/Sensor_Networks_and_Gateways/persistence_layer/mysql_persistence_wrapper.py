"""Defines the MySQLPersistenceWrapper class."""

from Sensor_Networks_and_Gateways.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import (MySQLConnectionPool)
import inspect
import json

class MySQLPersistenceWrapper(ApplicationBase):
	"""Implements the MySQLPersistenceWrapper class."""

	def __init__(self, config:dict)->None:
		"""Initializes object. """
		self._config_dict = config
		self.META = config["meta"]
		self.DATABASE = config["database"]
		super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

		# Database Configuration Constants
		self.DB_CONFIG = {}
		self.DB_CONFIG['database'] = \
			self.DATABASE["connection"]["config"]["database"]
		self.DB_CONFIG['user'] = self.DATABASE["connection"]["config"]["user"]
		self.DB_CONFIG['password'] = self.DATABASE["connection"]["config"]["password"]
		self.DB_CONFIG['host'] = self.DATABASE["connection"]["config"]["host"]
		self.DB_CONFIG['port'] = self.DATABASE["connection"]["config"]["port"]

		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DB_CONFIG}')

		# Database Connection
		self._connection_pool = \
			self._initialize_database_connection_pool(self.DB_CONFIG)
		

		# SQL String Constants





	# MySQLPersistenceWrapper Methods

	def execute_query(self, query:str, params:tuple=None)->list:
		"""Executes a query and returns all results as a list of dictionaries."""
		try:
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Running query: {query}')
			connection = self._connection_pool.get_connection()
			db_cursor = connection.cursor(dictionary=True)
			db_cursor.execute(query, params or ())
			results = db_cursor.fetchall()
			db_cursor.close()
			connection.close()
			return results
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: MySQL error: {err}')
			return []
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: General error: {e}')
			return []

	def execute_operation(self, query:str, params:tuple=None)->int:
		"""Executes Database operations."""
		try:
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Executing operation: {query}')
			connection = self._connection_pool.get_connection()
			db_cursor = connection.cursor()
			db_cursor.execute(query, params or ())
			affected_rows = db_cursor.rowcount
			connection.commit()
			db_cursor.close()
			connection.close()
			return affected_rows
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: MySQL error: {err}')
			return []
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: General error: {e}')
			return []



		##### Private Utility Methods #####

	def _initialize_database_connection_pool(self, config:dict)->MySQLConnectionPool:
		"""Initializes database connection pool."""
		try:
			self._logger.log_debug(f'Creating connection pool...')
			cnx_pool = \
				MySQLConnectionPool(pool_name = self.DATABASE["pool"]["name"],
					pool_size=self.DATABASE["pool"]["size"],
					pool_reset_session=self.DATABASE["pool"]["reset_session"],
					**config)
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Connection pool successfully created!')
			return cnx_pool
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem creating connection pool: {err}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Check DB cnfg:\n{json.dumps(self.DATABASE)}')
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Problem creating connection pool: {e}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Check DB conf:\n{json.dumps(self.DATABASE)}')
