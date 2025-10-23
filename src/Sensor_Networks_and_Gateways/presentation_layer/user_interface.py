"""Implements the applicatin user interface."""

from Sensor_Networks_and_Gateways.application_base import ApplicationBase
from Sensor_Networks_and_Gateways.service_layer.app_services import AppServices
import inspect
import json

class UserInterface(ApplicationBase):
    """UserInterface Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.DB = AppServices(config)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')
        
    # Template Start -- Create a user interface here. This just estabolishes the basic connection to db.
    def start(self):
        """Start main user interface."""
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User interface started!')
        query = 'CALL `Add_and_Autolink_Sensor`("Sensor X.7", "Gateway 1");'
        results = self.DB.execute_operation(query)
       
        query2 = 'SELECT * FROM summaryview;'
        results2 = self.DB.query_database(query2)
        if results2:
            for row in results2:
                self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Row: {row}')
        else:
            self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: No results found.')