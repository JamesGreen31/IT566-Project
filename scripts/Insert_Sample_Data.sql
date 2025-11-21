USE `sensors_and_gateways` ;

-- --------------------------------------------------------------------------
--                             CREATE SAMPLE DATA                           -
-- --------------------------------------------------------------------------

-- Create Gateways
INSERT INTO Gateways (GatewayName) VALUES ("Gateway 1");
INSERT INTO Gateways (GatewayName) VALUES ("Gateway 2");
INSERT INTO Gateways (GatewayName) VALUES ("Gateway 3");

-- Create Sensors
INSERT INTO Sensors (SensorName) VALUES ("Sensor 1.1");
INSERT INTO Sensors (SensorName) VALUES ("Sensor 1.2");
INSERT INTO Sensors (SensorName) VALUES ("Sensor 1.3");

INSERT INTO Sensors (SensorName) VALUES ("Sensor 2.1");
INSERT INTO Sensors (SensorName) VALUES ("Sensor 2.2");

INSERT INTO Sensors (SensorName) VALUES ("Sensor 3.1");

-- ESTABOLISH RELATNSHIPS

INSERT INTO SensorsGatewaysXref (idGateway, idSensor) VALUES (1,1);
INSERT INTO SensorsGatewaysXref (idGateway, idSensor) VALUES (1,2);
INSERT INTO SensorsGatewaysXref (idGateway, idSensor) VALUES (1,3);
INSERT INTO SensorsGatewaysXref (idGateway, idSensor) VALUES (2,4);
INSERT INTO SensorsGatewaysXref (idGateway, idSensor) VALUES (2,5);
INSERT INTO SensorsGatewaysXref (idGateway, idSensor) 

SELECT idGateway, idSensor FROM Gateways JOIN Sensors WHERE
	GatewayName = "Gateway 3" AND
    SensorName = "Sensor 3.1";

CALL `Add_and_Autolink_Sensor`("Sensor X.4", "Gateway 1");
CALL `Link_Sensor`("Sensor X.4", "Gateway 3");
