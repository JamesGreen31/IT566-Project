-- -----------------------------------------------------
-- PROCEDURE and VIEW Creation script
-- -----------------------------------------------------
USE `sensors_and_gateways`;



-- -----------------------------------------------------
-- Placeholder table for view `sensors_and_gateways`.`SensorGatewayPairs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensors_and_gateways`.`SensorGatewayPairs` (`Gateway Name` INT, `Sensor Name` INT);

-- -----------------------------------------------------
-- Placeholder table for view `sensors_and_gateways`.`SummaryView`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensors_and_gateways`.`SummaryView` (`Gateway Name` INT, `"Linked Sensors"` INT);

-- -----------------------------------------------------
-- Placeholder table for view `sensors_and_gateways`.`SensorGatewayPairsExtended`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensors_and_gateways`.`SensorGatewayPairsExtended` (`"Gateway ID"` INT, `"Gateway Name"` INT, `"Sensor ID"` INT, `"Sensor Name"` INT);

-- -----------------------------------------------------
-- Placeholder table for view `sensors_and_gateways`.`SensorGatewayPairsExtendedSummary`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensors_and_gateways`.`SensorGatewayPairsExtendedSummary` (`Gateway ID` INT, `Gateway Name` INT, `"Linked Sensor IDs"` INT, `"Linked Sensor Names"` INT);

-- -----------------------------------------------------
-- procedure Add_and_Autolink_Sensor
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Add_and_Autolink_Sensor` (
	IN new_sensor_name VARCHAR(45),
    IN existing_gateway_name VARCHAR(45))
BEGIN
	DECLARE gateway_id INT;
    DECLARE sensor_id INT;
    SELECT idGateway INTO gateway_id FROM Gateways WHERE
		GatewayName = existing_gateway_name;
	
    IF gateway_id IS NULL THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = "Unable to Create create and auto-link sensor -- gateway does not exist";
    END IF;
    
    INSERT INTO Sensors (SensorName) VALUES (new_sensor_name);
    SET sensor_id = LAST_INSERT_ID();
    
    INSERT INTO SensorsGatewaysXref (idGateway, idSensor) VALUES (gateway_id, sensor_id);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure Link_Sensor
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Link_Sensor` (
	IN p_sensor_name VARCHAR(45),
    IN p_existing_gateway_name VARCHAR(45)
)
BEGIN
	DECLARE sensor_id INT;
    DECLARE gateway_id INT;
    DECLARE xc_link INT;
	
    SELECT idSensor INTO sensor_id FROM Sensors WHERE
		SensorName = p_sensor_name;
        
	IF sensor_id IS NULL THEN
		SIGNAL SQLSTATE '45000' 
			SET MESSAGE_TEXT = "Specified Sensor Name does not exist";
    END IF;
        
    SELECT idGateway INTO gateway_id FROM Gateways WHERE
		GatewayName = p_existing_gateway_name;
	
	IF gateway_id IS NULL THEN
		SIGNAL SQLSTATE '45000' 
			SET MESSAGE_TEXT = "Specified Gateway Name does not exist";
    END IF;
	
	SELECT idSensor INTO xc_link FROM SensorsGatewaysXref xc WHERE
		xc.idSensor = sensor_id AND
        xc.idGateway = gateway_id;
	
    IF xc_link IS NOT NULL THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = "Sensor already linked to gateway";
    END IF;
    
    INSERT INTO SensorsGatewaysXref (idGateway, idSensor) VALUES(gateway_id, sensor_id);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure Create_Sensor
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Create_Sensor` (
	IN p_sensor_name VARCHAR(45)
)
BEGIN
	INSERT INTO Sensors (SensorName) VALUES (p_sensor_name);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure Create_Gateway
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Create_Gateway` (
	IN p_gateway_name VARCHAR(45)
)
BEGIN
	INSERT INTO Gateways (GatewayName) VALUES (p_gateway_name);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure Delete_Gateway
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Delete_Gateway` (
	IN p_existing_gateway VARCHAR(45)
)
BEGIN
	DECLARE gateway_id INT;
    
    -- Convert Gateway name into gateway ID (Note: We don't explicitly have to do this because Gateway name is unqiue
    -- but for the sake of sanity and consistency, we will do so anyway.
    SELECT idGateway INTO gateway_id FROM Gateways;
    
    -- If the gateway name was not present in the database, throw an error.
    IF gateway_id IS NULL THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = "Cannot delete gateway -- gateway not present";
	END IF;
    
    -- Delete the gateway. Cascade will resolve linking table.
    DELETE FROM Gateways WHERE
		idGateway = gateway_id;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure Delete_Sensor
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Delete_Sensor` (
	IN p_existing_sensor VARCHAR(45)
)
BEGIN
	-- Since sensor name is unique, we do not have to filter it by key
    DELETE FROM Sensor WHERE
		SensorName = p_existing_sensor;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure Change_Sensor_Name
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Change_Sensor_Name` (
	IN p_old_sensor_name VARCHAR(45),
	   p_new_sensor_name VARCHAR(45)
)
BEGIN
	DECLARE o_sensor_id INT;
    DECLARE n_sensor_id INT;
    SELECT idSensor INTO o_sensor_id FROM
    Sensors WHERE
    SensorName = p_new_sensor_name;
    
	SELECT idSensor INTO n_sensor_id FROM
    Sensors WHERE
    SensorName = p_new_sensor_name;
    
    IF NOT (o_sensor_id IS NOT NULL AND n_sensor_id IS NULL) THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = "Either the old sensor name does not exist, or the new sensor already exists.";
    END IF;
    
	UPDATE Sensors
		SET SensorName = p_new_sensor_name
		WHERE SensorName = p_old_sensor_name;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure Change_Gateway_Name
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Change_Gateway_Name` (
	IN p_old_Gateway_name VARCHAR(45),
	   p_new_Gateway_name VARCHAR(45)
)
BEGIN
	DECLARE o_Gateway_id INT;
    DECLARE n_Gateway_id INT;
    SELECT idGateway INTO o_Gateway_id FROM
    Gateways WHERE
    GatewayName = p_new_Gateway_name;
    
	SELECT idGateway INTO n_Gateway_id FROM
    Gateways WHERE
    GatewayName = p_new_Gateway_name;
    
    IF NOT (o_Gateway_id IS NOT NULL AND n_Gateway_id IS NULL) THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = "Either the old Gateway name does not exist, or the new Gateway already exists.";
    END IF;
    
	UPDATE Gateways
		SET GatewayName = p_new_Gateway_name
		WHERE GatewayName = p_old_Gateway_name;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure Unlink_Sensor
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Unlink_Sensor` (
    IN p_sensor_name VARCHAR(45),
    IN p_gateway_name VARCHAR(45)  -- can be NULL if you want to unlink from all gateways
)
BEGIN
    DECLARE sensor_id INT;
    DECLARE gateway_id INT;

    -- Find sensor ID
    SELECT idSensor INTO sensor_id 
    FROM Sensors 
    WHERE SensorName = p_sensor_name;

    IF sensor_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Specified sensor name does not exist';
    END IF;

    -- If gateway name was given, find its ID
    IF p_gateway_name IS NOT NULL THEN
        SELECT idGateway INTO gateway_id
        FROM Gateways
        WHERE GatewayName = p_gateway_name;

        IF gateway_id IS NULL THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Specified gateway name does not exist';
        END IF;

        -- Delete only that specific link
        DELETE FROM SensorsGatewaysXref
        WHERE idSensor = sensor_id
          AND idGateway = gateway_id;

        IF ROW_COUNT() = 0 THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'No link found between given sensor and gateway';
        END IF;

    ELSE
        -- No gateway name provided, unlink from all gateways
        DELETE FROM SensorsGatewaysXref
        WHERE idSensor = sensor_id;

        IF ROW_COUNT() = 0 THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'No links found for the given sensor';
        END IF;
    END IF;

END$$

DELIMITER ;

-- -----------------------------------------------------
-- View `sensors_and_gateways`.`SensorGatewayPairs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sensors_and_gateways`.`SensorGatewayPairs`;
USE `sensors_and_gateways`;
CREATE  OR REPLACE VIEW `SensorGatewayPairs` AS
SELECT gw.GatewayName as `Gateway Name`, s.SensorName as `Sensor Name` FROM Gateways gw JOIN Sensors s JOIN SensorsGatewaysXref AS xc ON
	gw.idGateway = xc.idGateway AND
    s.idSensor = xc.idSensor;

-- -----------------------------------------------------
-- View `sensors_and_gateways`.`SummaryView`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sensors_and_gateways`.`SummaryView`;
USE `sensors_and_gateways`;
CREATE  OR REPLACE VIEW `SummaryView` AS
SELECT `Gateway Name`, GROUP_CONCAT(`Sensor Name` ORDER BY `Sensor Name` SEPARATOR ", ") AS "Linked Sensors" FROM SensorGatewayPairs GROUP BY `Gateway Name`;

-- -----------------------------------------------------
-- View `sensors_and_gateways`.`SensorGatewayPairsExtended`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sensors_and_gateways`.`SensorGatewayPairsExtended`;
USE `sensors_and_gateways`;
CREATE  OR REPLACE VIEW `SensorGatewayPairsExtended` AS
SELECT gw.idGateway AS "Gateway ID", gw.GatewayName AS "Gateway Name", s.idSensor AS "Sensor ID", s.SensorName AS "Sensor Name" FROM Gateways gw JOIN Sensors s JOIN SensorsGatewaysXref xc
	ON 
		gw.idGateway = xc.idGateway AND
        s.idSensor = xc.idSensor;

-- -----------------------------------------------------
-- View `sensors_and_gateways`.`SensorGatewayPairsExtendedSummary`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sensors_and_gateways`.`SensorGatewayPairsExtendedSummary`;
USE `sensors_and_gateways`;
CREATE  OR REPLACE VIEW `SensorGatewayPairsExtendedSummary` AS
SELECT `Gateway ID`, `Gateway Name`, GROUP_CONCAT(`Sensor ID` ORDER BY `Sensor ID` SEPARATOR ", ") AS "Linked Sensor IDs", GROUP_CONCAT(`Sensor Name` ORDER BY `Sensor Name` SEPARATOR ", ") AS "Linked Sensor Names" FROM SensorGatewayPairsExtended GROUP BY `Gateway ID`, `Gateway Name`;
