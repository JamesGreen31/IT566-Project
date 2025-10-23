"""Implements AppServices Class."""

from Sensor_Networks_and_Gateways.application_base import ApplicationBase
from Sensor_Networks_and_Gateways.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import inspect

class AppServices(ApplicationBase):
    """AppServices Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.DB = MySQLPersistenceWrapper(config)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

    # Template Methods -- replace these methods with the designated view operations in the DB.
    def query_database(self, query:str, params:tuple=None)->list:
        """Queries the database and returns results."""
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Executing query: {query} with params: {params}')
        results = self.DB.execute_query(query, params)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Query returned {len(results)} results.')
        return results

    def execute_operation(self, operation:str, params:tuple=None)->bool:
        """Executes a database operation. While we can use insert, we have procedures for most things."""
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Executing operation: {operation} with params: {params}')
        success = self.DB.execute_operation(operation, params)
        if success:
            self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Operation executed successfully.')
        else:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Operation failed.')
        return success