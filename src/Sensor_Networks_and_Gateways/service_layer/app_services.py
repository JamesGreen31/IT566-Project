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

    
# CRUD Operations -- Sensor

def create_sensor():
    """
    Description: Creates a new sensor.
    Calls Procedure: Create_Sensor
    """
    pass


def get_sensor():
    """
    Description: Retrieves an existing sensor by name or ID.
    Calls Procedure: (direct SELECT on Sensors)
    """
    pass


def change_sensor_name():
    """
    Description: Renames an existing sensor.
    Calls Procedure: Change_Sensor_Name
    """
    pass


def delete_sensor():
    """
    Description: Deletes an existing sensor and all its links.
    Calls Procedure: Delete_Sensor
    """
    pass


# CRUD Operations -- Gateway


def create_gateway():
    """
    Description: Creates a new gateway.
    Calls Procedure: Create_Gateway
    """
    pass


def get_gateway():
    """
    Description: Retrieves an existing gateway by name or ID.
    Calls Procedure: (direct SELECT on Gateways)
    """
    pass


def change_gateway_name():
    """
    Description: Renames an existing gateway.
    Calls Procedure: Change_Gateway_Name
    """
    pass


def delete_gateway():
    """
    Description: Deletes an existing gateway and its linked sensors.
    Calls Procedure: Delete_Gateway
    """
    pass


# Additional Business Logic Operations

def quick_add():
    """
    Description: Creates a new sensor and automatically links it to an existing gateway.
    Calls Procedure: Add_and_Autolink_Sensor
    """
    pass

def link_sensor_to_gateway():
    """
    Description: Links an existing sensor to a gateway.
    Calls Procedure: Link_Sensor
    """
    pass


def unlink_sensor_from_gateway():
    """
    Description: Unlinks a sensor from a gateway or all gateways if none specified.
    Calls Procedure: Unlink_Sensor
    """
    pass


def get_sensors_for_gateway():
    """
    Description: Lists all sensors linked to a specific gateway.
    Calls Procedure: (SELECT from SensorGatewayPairs view)
    """
    pass


def get_gateways_for_sensor():
    """
    Description: Lists all gateways linked to a specific sensor.
    Calls Procedure: (SELECT from SensorGatewayPairs view)
    """
    pass


def get_all_sensors():
    """
    Description: Retrieves all sensors in the system.
    Calls Procedure: (SELECT * FROM Sensors)
    """
    pass


def get_all_gateways():
    """
    Description: Retrieves all gateways in the system.
    Calls Procedure: (SELECT * FROM Gateways)
    """
    pass


# User Interface Views

def get_summary():
    """
    Description: Returns a summary of gateways and their linked sensors.
    Calls Procedure: (SELECT * FROM SummaryView)
    """
    pass
