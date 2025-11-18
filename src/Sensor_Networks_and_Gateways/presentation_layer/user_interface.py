"""Implements the applicatin user interface."""

from Sensor_Networks_and_Gateways.application_base import ApplicationBase
from Sensor_Networks_and_Gateways.service_layer.app_services import AppServices
import inspect
import json
import sys
from prettytable import PrettyTable;
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
        while True:
            userin = input("Enter a command option: \n\t1) View Summary  \n\t2) View All Sensors  \n\t3) View All Gateways  \n\t4) Add Sensor  \n\t5) Add Gateway  \n\t6) Quick Add Sensor \n\t7) Link Sensor to Gateway  \n\t8) Delete Sensor \n\t9) Delete Gateway \n\t10) Exit\n")
            match userin:
                case "1":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 1: View Summary')
                    results = self.DB.get_summary()
                    table = PrettyTable()
                    table.field_names = ["Gateway Name", "Sensor Name"]
                    for row in results:
                        table.add_row(row)
                    print(table)
                case "2":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 2: View All Sensors')
                    results = self.DB.get_all_sensors()
                    table = PrettyTable()
                    table.field_names = ["Sensor Name"]
                    for row in results:
                        table.add_row(row)  
                    print(table)
                case "3":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 3: View All Gateways')
                    results = self.DB.get_all_gateways()
                    table = PrettyTable()
                    table.field_names = ["Gateway Name"]
                    for row in results:
                        table.add_row(row)  
                    print(table)
                case "4":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 4: Add Sensor')
                    sensor_name = input("Enter the name of the sensor to add: ")    
                    result = self.DB.add_sensor(sensor_name)
                    if result:
                        print(f"Sensor '{sensor_name}' added successfully.")
                    else:
                        print(f"Failed to add sensor '{sensor_name}'.")
                case "5":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 5: Add Gateway')
                    gateway_name = input("Enter the name of the gateway to add: ")
                    result = self.DB.add_gateway(gateway_name)
                    if result:
                        print(f"Gateway '{gateway_name}' added successfully.")
                    else:
                        print(f"Failed to add gateway '{gateway_name}'.")
                case "6":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 6: Quick Add Sensor')
                    sensor_name = input("Enter the name of the sensor to add: ")
                    gateway_name = input("Enter the name of the gateway to link to: ")
                    result = self.DB.quick_add_sensor(sensor_name, gateway_name)
                    if result:
                        print(f"Sensor '{sensor_name}' added and linked to gateway '{gateway_name}' successfully.")
                    else:
                        print(f"Failed to add sensor '{sensor_name}' and link to gateway '{gateway_name}'.")
                case "7":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 7: Link Sensor to Gateway')
                    sensor_name = input("Enter the name of the sensor to link: ")
                    gateway_name = input("Enter the name of the gateway to link to: ")
                    result = self.DB.link_sensor(sensor_name, gateway_name)
                    if result:
                        print(f"Sensor '{sensor_name}' linked to gateway '{gateway_name}' successfully.")
                    else:
                        print(f"Failed to link sensor '{sensor_name}' to gateway '{gateway_name}'.")
                case "8":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 8: Delte Sensor')
                    sensor_name = input("Enter the name of the sensor to delete: ")
                    temporary_result = self.DB.check_sensor_exists(sensor_name)
                    if not temporary_result:
                        print(f"Sensor '{sensor_name}' does not exist.")
                        continue
                    else:
                        print(f"Are you sure you want to delete {sensor_name}? This action cannot be undone. (y/n)")
                        confirmation = input()
                        if confirmation.lower() != 'y':
                            print("Deletion cancelled.")
                            continue
                    result = self.DB.delete_sensor(sensor_name)
                    if result:
                        print(f"Sensor '{sensor_name}' deleted successfully.")
                    else:
                        print(f"Failed to delete sensor '{sensor_name}'.")
                case "9":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 9: Delete Gateway')
                    gateway_name = input("Enter the name of the gateway to delete: ")
                    temporary_result = self.DB.check_gateway_exists(gateway_name)
                    if not temporary_result:
                        print(f"Gateway '{gateway_name}' does not exist.")
                        continue
                    else:
                        print(f"Are you sure you want to delete {gateway_name}? This action cannot be undone. (y/n)")
                        confirmation = input()
                        if confirmation.lower() != 'y':
                            print("Deletion cancelled.")
                            continue
                    result = self.DB.delete_gateway(gateway_name)
                    if result:
                        print(f"Gateway '{gateway_name}' deleted successfully.")
                    else:
                        print(f"Failed to delete gateway '{gateway_name}'.")
                case "10":
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected option 10: Exit')
                    print("Exiting the application.")
                    sys.exit(0)
                case _:
                    self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User selected an invalid option: {userin}')
                    print("Invalid option. Please try again.")
