from Sensor_Networks_and_Gateways.application_base import ApplicationBase
from Sensor_Networks_and_Gateways.service_layer.app_services import AppServices
import inspect
import json
import sys
from prettytable import PrettyTable


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
            self._print_main_menu()
            userin = input("Select an option: ")
            self._handle_main_menu_choice(userin)

    # ====== Menu + dispatcher ======
    def _print_main_menu(self) -> None:
        menu_text = (
            "Enter a command option:\n"
            "\t1) View Summary\n"
            "\t2) View All Sensors\n"
            "\t3) View All Gateways\n"
            "\t4) Add Sensor\n"
            "\t5) Add Gateway\n"
            "\t6) Quick Add Sensor\n"
            "\t7) Link Sensor to Gateway\n"
            "\t8) Delete Sensor\n"
            "\t9) Delete Gateway\n"
            "\t10) Update Sensor Name\n"
            "\t11) Update Gateway Name\n"
            "\tQ) Quit\n"
        )
        print(menu_text)

    def _handle_main_menu_choice(self, userin: str) -> None:
        choice = userin.strip().lower()
        if choice in {"q", "quit"}:
            self._exit_application()

        match choice:
            case "1":
                self._view_summary()
            case "2":
                self._view_all_sensors()
            case "3":
                self._view_all_gateways()
            case "4":
                self._add_sensor()
            case "5":
                self._add_gateway()
            case "6":
                self._quick_add_sensor()
            case "7":
                self._link_sensor_to_gateway()
            case "8":
                self._delete_sensor()
            case "9":
                self._delete_gateway()
            case "10":
                self._update_sensor_name()
            case "11":
                self._update_gateway_name()
            case _:
                self._logger.log_debug(
                    f'{inspect.currentframe().f_code.co_name}: '
                    f"User selected an invalid option: {userin}"
                )
                print("Invalid option. Please select one of the listed options.")
            
        self._hold_input()

    # ====== View operations ======
    def _view_summary(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 1: View Summary"
        )
        results = self.DB.get_summary()
        table = PrettyTable()
        table.field_names = ["Gateway Name", "Sensor Name"]
        for row in results:
            table.add_row(row)
        print(table)

    def _view_all_sensors(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 2: View All Sensors"
        )
        results = self.DB.get_all_sensors()
        table = PrettyTable()
        table.field_names = ["Sensor Name"]
        for row in results:
            table.add_row(row)
        print(table)

    def _view_all_gateways(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 3: View All Gateways"
        )
        results = self.DB.get_all_gateways()
        table = PrettyTable()
        table.field_names = ["Gateway Name"]
        for row in results:
            table.add_row(row)
        print(table)

    # ====== Add operations ======
    def _add_sensor(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 4: Add Sensor"
        )
        sensor_name = input("Enter the name of the sensor to add: ")
        result = self.DB.add_sensor(sensor_name)
        if result:
            print(f"Sensor '{sensor_name}' added successfully.")
        else:
            print(f"Failed to add sensor '{sensor_name}'.")

    def _add_gateway(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 5: Add Gateway"
        )
        gateway_name = input("Enter the name of the gateway to add: ")
        result = self.DB.add_gateway(gateway_name)
        if result:
            print(f"Gateway '{gateway_name}' added successfully.")
        else:
            print(f"Failed to add gateway '{gateway_name}'.")

    def _quick_add_sensor(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 6: Quick Add Sensor"
        )
        sensor_name = input("Enter the name of the sensor to add: ")
        results = self.DB.get_all_gateways()
        table = PrettyTable()
        table.field_names = ["Gateway Name"]
        for row in results:
            table.add_row(row)
        print(table)
        gateway_name = input("Enter the name of the gateway to link to: ")
        result = self.DB.quick_add_sensor(sensor_name, gateway_name)
        if result:
            print(
                f"Sensor '{sensor_name}' added and linked to gateway "
                f"'{gateway_name}' successfully."
            )
        else:
            print(
                f"Failed to add sensor '{sensor_name}' and link to gateway "
                f"'{gateway_name}'."
            )

    # ====== Link operations ======
    def _link_sensor_to_gateway(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 7: Link Sensor to Gateway"
        )
        results = self.DB.get_all_sensors()
        table = PrettyTable()
        table.field_names = ["Sensor Name"]
        for row in results:
            table.add_row(row)
        print(table) 
        sensor_name = input("Enter the name of the sensor to link: ")
        results = self.DB.get_all_gateways()
        table = PrettyTable()
        table.field_names = ["Gateway Name"]
        for row in results:
            table.add_row(row)
        print(table)
        gateway_name = input("Enter the name of the gateway to link to: ")
        result = self.DB.link_sensor(sensor_name, gateway_name)
        if result:
            print(
                f"Sensor '{sensor_name}' linked to gateway "
                f"'{gateway_name}' successfully."
            )
        else:
            print(
                f"Failed to link sensor '{sensor_name}' to gateway "
                f"'{gateway_name}'."
            )

    # ====== Delete operations ======
    def _delete_sensor(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 8: Delete Sensor"
        )
        results = self.DB.get_all_sensors()
        table = PrettyTable()
        table.field_names = ["Sensor Name"]
        for row in results:
            table.add_row(row)
        print(table) 
        sensor_name = input("Enter the name of the sensor to delete: ")
        temporary_result = self.DB.check_sensor_exists(sensor_name)
        if not temporary_result:
            print(f"Sensor '{sensor_name}' does not exist.")
            return

        print(
            f"Are you sure you want to delete {sensor_name}? "
            "This action cannot be undone. (y/n)"
        )
        confirmation = input()
        if confirmation.lower() != "y":
            print("Deletion cancelled.")
            return

        result = self.DB.delete_sensor(sensor_name)
        if result:
            print(f"Sensor '{sensor_name}' deleted successfully.")
        else:
            print(f"Failed to delete sensor '{sensor_name}'.")

    def _delete_gateway(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 9: Delete Gateway"
        )
        results = self.DB.get_all_gateways()
        table = PrettyTable()
        table.field_names = ["Gateway Name"]
        for row in results:
            table.add_row(row)
        print(table) 
        gateway_name = input("Enter the name of the gateway to delete: ")
        temporary_result = self.DB.check_gateway_exists(gateway_name)
        if not temporary_result:
            print(f"Gateway '{gateway_name}' does not exist.")
            return

        print(
            f"Are you sure you want to delete {gateway_name}? "
            "This action cannot be undone. (y/n)"
        )
        confirmation = input()
        if confirmation.lower() != "y":
            print("Deletion cancelled.")
            return

        result = self.DB.delete_gateway(gateway_name)
        if result:
            print(f"Gateway '{gateway_name}' deleted successfully.")
        else:
            print(f"Failed to delete gateway '{gateway_name}'.")

    # ====== Update operations ======
    def _update_sensor_name(self) -> None:
        """Rename an existing sensor."""
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 11: Update Sensor Name"
        )
        results = self.DB.get_all_sensors()
        table = PrettyTable()
        table.field_names = ["Sensor Name"]
        for row in results:
            table.add_row(row)
        print(table) 
        old_name = input("Enter the current sensor name: ")
        if not self.DB.check_sensor_exists(old_name):
            print(f"Sensor '{old_name}' does not exist.")
            return

        new_name = input("Enter the new sensor name: ")
        result = self.DB.update_sensor_name(old_name, new_name)
        if result:
            print(f"Sensor '{old_name}' renamed to '{new_name}' successfully.")
        else:
            print(
                f"Failed to rename sensor '{old_name}' to '{new_name}'."
            )

    def _update_gateway_name(self) -> None:
        """Rename an existing gateway."""
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 12: Update Gateway Name"
        )
        results = self.DB.get_all_gateways()
        table = PrettyTable()
        table.field_names = ["Gateway Name"]
        for row in results:
            table.add_row(row)
        print(table) 
        old_name = input("Enter the current gateway name: ")
        if not self.DB.check_gateway_exists(old_name):
            print(f"Gateway '{old_name}' does not exist.")
            return

        new_name = input("Enter the new gateway name: ")
        result = self.DB.update_gateway_name(old_name, new_name)
        if result:
            print(f"Gateway '{old_name}' renamed to '{new_name}' successfully.")
        else:
            print(
                f"Failed to rename gateway '{old_name}' to '{new_name}'."
            )

    # ====== Exit ======
    def _exit_application(self) -> None:
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: User selected option 10: Exit"
        )
        print("Exiting the application.")
        sys.exit(0)

    def _hold_input(self) -> None:
        input("Press Enter to return to the main screen...")