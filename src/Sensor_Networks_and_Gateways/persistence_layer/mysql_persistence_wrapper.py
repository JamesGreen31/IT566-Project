"""Defines the MySQLPersistenceWrapper class."""

from Sensor_Networks_and_Gateways.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import (MySQLConnectionPool)
import inspect
import json
from typing import List

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
		

		# SQL String Constants -- These are used by the methods below to execute queries and operations and protect against SQL attacks.
		# READ Statements
		self.SELECT_ALL_SENSORS = f"SELECT `SensorName` AS \"Sensor Name\" FROM `Sensors`;"
		self.SELECT_ALL_GATEWAYS = f"SELECT `GatewayName` AS \"Gateway Name\" FROM `Gateways`;"
		self.SELECT_ALL_SUMMARY = f"SELECT `Gateway Name`, `Linked Sensors` FROM `SummaryView`;"
		self.SELECT_SPECIFIC_SENSOR = f"SELECT `SensorName` AS \"Sensor Name\" FROM `Sensors` WHERE `SensorName` = %s;"
		self.SELECT_SPECIFIC_GATEWAY = f"SELECT `GatewayName` AS \"Gateway Name\" FROM `Gateways` WHERE `GatewayName` = %s;"

		# CREATE Statements
		self.CALL_CREATE_SENSOR = f"CALL `Create_Sensor`(%s);"
		self.CALL_CREATE_GATEWAY = f"CALL `Create_Gateway`(%s);"
		self.CALL_ADD_AND_AUTOLINK_SENSOR = f"CALL `Add_and_Autolink_Sensor`(%s, %s);"

		# UPDATE Statements
		self.CALL_UNLINK_SENSOR = f"CALL `Unlink_Sensor`(%s, %s);"
		self.CALL_LINK_SENSOR = f"CALL `Link_Sensor`(%s, %s);"
		self.CALL_RESET_SENSOR = f"CALL `Reset_Sensor`(%s);"
		self.CALL_RESET_GATEWAY = f"CALL `Reset_Gateway`(%s);"
		self.CALL_UPDATE_SENSOR_NAME = f"CALL `Change_Sensor_Name`(%s, %s);"
		self.CALL_UPDATE_GATEWAY_NAME = f"CALL `Change_Gateway_Name`(%s, %s);"

		# DELETE Statements
		self.CALL_DELETE_SENSOR = f"CALL `Delete_Sensor`(%s);"
		self.CALL_DELETE_GATEWAY = f"CALL `Delete_Gateway`(%s);"

	# MySQLPersistenceWrapper Methods

	# READ Methods
	def get_all_sensors(self)->List[dict]:
		"""Returns all sensors in the database using execute query."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Getting all sensors')
		results = self._execute_query(self.SELECT_ALL_SENSORS)
		return results
	
	def get_all_gateways(self)->List[dict]:
		"""Returns all gateways in the database using execute query."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Getting all gateways')
		results = self._execute_query(self.SELECT_ALL_GATEWAYS)
		return results

	def get_summary(self)->List[dict]:
		"""Returns all sensors in the database using execute query."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Getting summary of all gateways and linked sensors')
		results = self._execute_query(self.SELECT_ALL_SUMMARY)
		return results
	
	def get_specific_sensor(self, sensor_name:str)->List[dict]:
		"""Checks if a sensor exists in the database."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Checking if sensor "{sensor_name}" exists')
		results = self._execute_query(self.SELECT_SPECIFIC_SENSOR, (sensor_name,))
		return results

	def get_specific_gateway(self, gateway_name:str)->List[dict]:
		"""Checks if a gateway exists in the database."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Checking if gateway "{gateway_name}" exists')
		results = self._execute_query(self.SELECT_SPECIFIC_GATEWAY, (gateway_name,))
		return results

	# CREATE Methods
	def create_sensor(self, sensor_name:str)->int:
		"""Creates a new sensor in the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Creating sensor with name: "{sensor_name}"')
		return self._execute_operation(self.CALL_CREATE_SENSOR, (sensor_name,))
	
	def create_gateway(self, gateway_name:str)->int:
		"""Creates a new gateway in the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Creating gateway with name: "{gateway_name}"')
		return self._execute_operation(self.CALL_CREATE_GATEWAY, (gateway_name,))
	
	def add_and_autolink_sensor(self, sensor_name:str, gateway_name:int)->int:
		"""Adds a new sensor and links it to a gateway in the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Adding sensor "{sensor_name}" and linking to gateway with ID: {gateway_name}')
		return self._execute_operation(self.CALL_ADD_AND_AUTOLINK_SENSOR, (sensor_name, gateway_name))
	
	# UPDATE Methods
	def unlink_sensor(self, sensor_name:int, gateway_name:int)->int:
		"""Unlinks a sensor from a gateway in the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Unlinking sensor with ID: {sensor_name} from gateway with ID: {gateway_name}')	
		return self._execute_operation(self.CALL_UNLINK_SENSOR, (sensor_name, gateway_name))
	
	def link_sensor(self, sensor_name:int, gateway_name:int)->int:
		"""Links a sensor to a gateway in the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Linking sensor with ID: {sensor_name} to gateway with ID: {gateway_name}')
		return self._execute_operation(self.CALL_LINK_SENSOR, (sensor_name, gateway_name))
	
	def reset_sensor(self, sensor_name:int)->int:
		"""Resets a sensor in the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Resetting sensor with ID: {sensor_name}')
		return self._execute_operation(self.CALL_RESET_SENSOR, (sensor_name,))
	
	def reset_gateway(self, gateway_name:int)->int:
		"""Resets a gateway in the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Resetting gateway with ID: {gateway_name}')
		return self._execute_operation(self.CALL_RESET_GATEWAY, (gateway_name,))
	
	def update_sensor_name(self, sensor_name:int, new_name:str)->int:
		"""Updates a sensor's name in the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Updating sensor name for ID: {sensor_name} to "{new_name}"')
		return self._execute_operation(self.CALL_UPDATE_SENSOR_NAME, (sensor_name, new_name))
	
	def update_gateway_name(self, gateway_name:int, new_name:str)->int:
		"""Updates a gateway's name in the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Updating gateway name for ID: {gateway_name} to "{new_name}"')
		return self._execute_operation(self.CALL_UPDATE_GATEWAY_NAME, (gateway_name, new_name))
	
	# DELETE Methods
	def delete_sensor(self, sensor_name:int)->int:
		"""Deletes a sensor from the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Deleting sensor with ID: {sensor_name}')
		return self._execute_operation(self.CALL_DELETE_SENSOR, (sensor_name,))
	
	def delete_gateway(self, gateway_name:int)->int:
		"""Deletes a gateway from the database using execute operation."""
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Deleting gateway with ID: {gateway_name}')
		return self._execute_operation(self.CALL_DELETE_GATEWAY, (gateway_name,))	
	
	# Private Methods
	def _execute_query(self, query:str, params:tuple=None)->list:
		"""Executes a query and returns all results as a list of dictionaries."""
		try:
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Running query: {query}')
			connection = self._connection_pool.get_connection()
			db_cursor = connection.cursor(dictionary=False)
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

	def _execute_operation(self, query:str, params:tuple=None)->int:
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
