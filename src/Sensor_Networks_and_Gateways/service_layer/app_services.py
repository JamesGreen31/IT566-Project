"""Implements AppServices Class."""

from Sensor_Networks_and_Gateways.application_base import ApplicationBase
from Sensor_Networks_and_Gateways.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import inspect


class AppServices(ApplicationBase):
    """AppServices Class Definition."""

    def __init__(self, config: dict) -> None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__,
                         logfile_prefix_name=self.META["log_prefix"])
        self.DB = MySQLPersistenceWrapper(config)
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}:It works!')

    # Data Gathering Functions
    def get_summary(self) -> list:
        """Returns all sensors in the database."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Getting summary of all sensors.')
        results = self.DB.get_summary()
        return results

    def get_all_sensors(self) -> list:
        """Returns all sensors in the database."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Getting all sensors.')
        results = self.DB.get_all_sensors()
        return results

    def get_all_gateways(self) -> list:
        """Returns all gateways in the database."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Getting all gateways.')
        results = self.DB.get_all_gateways()
        return results

    def check_sensor_exists(self, sensor_name: str) -> bool:
        """Checks if a sensor exists in the database."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Checking if sensor "{sensor_name}" exists.')
        result = self.DB.get_specific_sensor(sensor_name)
        return len(result) > 0

    def check_gateway_exists(self, gateway_name: str) -> bool:
        """Checks if a gateway exists in the database."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Checking if gateway "{gateway_name}" exists.')
        result = self.DB.get_specific_gateway(gateway_name)
        return len(result) > 0

    # Data Creation Functions
    def add_sensor(self, sensor_name: str) -> bool:
        """Adds a sensor to the database."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Adding sensor: {sensor_name}')
        result = self.DB.create_sensor(sensor_name)
        return result

    def add_gateway(self, gateway_name: str) -> bool:
        """Adds a gateway to the database."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Adding gateway: {gateway_name}')
        result = self.DB.create_gateway(gateway_name)
        return result

    def quick_add_sensor(self, sensor_name: str, gateway_name: str) -> bool:
        """Adds a sensor to the database and assigns it to a gateway."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Adding sensor: {sensor_name} to gateway: {gateway_name}')
        result = self.DB.add_and_autolink_sensor(sensor_name, gateway_name)
        return result

    # Data Update Functions
    def link_sensor(self, sensor_name: str, gateway_name: str) -> bool:
        """Links a sensor to a gateway."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Linking sensor: {sensor_name} to gateway: {gateway_name}')
        result = self.DB.link_sensor(sensor_name, gateway_name)
        return result

    def unlink_sensor(self, sensor_name: str) -> bool:
        """Unlinks a sensor from its gateway."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Unlinking sensor: {sensor_name} from its gateway.')
        result = self.DB.unlink_sensor(sensor_name)
        return result

    def reset_sensor(self, sensor_name: str) -> bool:
        """Resets a sensor's data."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Resetting sensor: {sensor_name}')
        result = self.DB.reset_sensor(sensor_name)
        return result

    def reset_gateway(self, gateway_name: str) -> bool:
        """Resets a gateway's data."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Resetting gateway: {gateway_name}')
        result = self.DB.reset_gateway(gateway_name)
        return result

    def update_sensor_name(self, old_name: str, new_name: str) -> bool:
        """Updates a sensor's name."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Updating sensor name from: {old_name} to: {new_name}')
        result = self.DB.update_sensor_name(old_name, new_name)
        return result

    def update_gateway_name(self, old_name: str, new_name: str) -> bool:
        """Updates a gateway's name."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Updating gateway name from: {old_name} to: {new_name}')
        result = self.DB.update_gateway_name(old_name, new_name)
        return result

    # Data Deletion Functions
    def delete_sensor(self, sensor_name: str) -> bool:
        """Deletes a sensor from the database."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Deleting sensor: {sensor_name}')
        result = self.DB.delete_sensor(sensor_name)
        return result

    def delete_gateway(self, gateway_name: str) -> bool:
        """Deletes a gateway from the database."""
        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: Deleting gateway: {gateway_name}')
        result = self.DB.delete_gateway(gateway_name)
        return result
