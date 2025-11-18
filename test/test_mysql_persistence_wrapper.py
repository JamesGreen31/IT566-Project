import sys
from pathlib import Path

# Add the src directory to sys.path
root = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(root))

import unittest
from Sensor_Networks_and_Gateways.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
from unittest.mock import MagicMock, patch

@patch('src.Sensor_Networks_and_Gateways.persistence_layer.mysql_persistence_wrapper.connector')  # patch the MySQL connector import in
class TestMySQLPersistenceWrapper(unittest.TestCase):

    def test_execute_query(self, mock_connector):
        # Mock configuration
        fake_config = {
            "meta": {"log_prefix": "TEST"},
            "database": {
                "connection": {
                    "config": {
                        "database": "test_db",
                        "user": "root",
                        "password": "password",
                        "host": "localhost",
                        "port": 3306
                    }
                },
                "pool": {
                    "name": "test_pool",
                    "size": 1,
                    "reset_session": True
                }
            }
        }

        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'Alice'}]
        mock_connection.cursor.return_value = mock_cursor
        mock_connector.connect.return_value = mock_connection

        # Mock your class with _connection_pool and _logger
        obj = MySQLPersistenceWrapper(fake_config)
        obj._connection_pool = MagicMock()
        obj._connection_pool.get_connection.return_value = mock_connection
        obj._logger = MagicMock()

        # Act
        result = obj.execute_query("SELECT * FROM users")

        # Assert
        self.assertEqual(result, [{'id': 1, 'name': 'Alice'}])
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users", ())
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        obj._logger.log_debug.assert_called()  # ensure debug logging happened

if __name__ == "__main__":
    unittest.main()