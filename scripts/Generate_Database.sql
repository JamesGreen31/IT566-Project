-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema sensors_and_gateways
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `sensors_and_gateways` ;

-- -----------------------------------------------------
-- Schema sensors_and_gateways
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sensors_and_gateways` DEFAULT CHARACTER SET utf8 ;
USE `sensors_and_gateways` ;

-- -----------------------------------------------------
-- Table `sensors_and_gateways`.`Sensors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensors_and_gateways`.`Sensors` (
  `idSensor` INT NOT NULL AUTO_INCREMENT,
  `SensorName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idSensor`),
  UNIQUE INDEX `idSensor_UNIQUE` (`idSensor` ASC) VISIBLE,
  UNIQUE INDEX `SensorName_UNIQUE` (`SensorName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sensors_and_gateways`.`Gateways`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensors_and_gateways`.`Gateways` (
  `idGateway` INT NOT NULL AUTO_INCREMENT,
  `GatewayName` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `idGateway_UNIQUE` (`idGateway` ASC) VISIBLE,
  PRIMARY KEY (`idGateway`),
  UNIQUE INDEX `GatewayName_UNIQUE` (`GatewayName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sensors_and_gateways`.`SensorsGatewayXref`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensors_and_gateways`.`SensorsGatewayXref` (
  `idSensorsGatewayXref` INT NOT NULL AUTO_INCREMENT,
  `SensorsGatewayXref_SensorId` INT NOT NULL,
  `SensorsGatewayXref_GatewayId` INT NOT NULL,
  PRIMARY KEY (`idSensorsGatewayXref`),
  INDEX `SensorsGatewayXref_SensorId_idx` (`SensorsGatewayXref_SensorId` ASC) VISIBLE,
  INDEX `SensorsGatewayXref_GatewayId_idx` (`SensorsGatewayXref_GatewayId` ASC) VISIBLE,
  CONSTRAINT `SensorsGatewayXref_SensorId`
    FOREIGN KEY (`SensorsGatewayXref_SensorId`)
    REFERENCES `sensors_and_gateways`.`Sensors` (`idSensor`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `SensorsGatewayXref_GatewayId`
    FOREIGN KEY (`SensorsGatewayXref_GatewayId`)
    REFERENCES `sensors_and_gateways`.`Gateways` (`idGateway`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `sensors_and_gateways` ;

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
    
    INSERT INTO SensorsGatewayXref (SensorsGatewayXref_GatewayId, SensorsGatewayXref_SensorId) VALUES (gateway_id, sensor_id);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure Link_Sensor
-- -----------------------------------------------------

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE PROCEDURE `Link_Sensor` (
	IN p_sensor_name VARCHAR(45),
    IN p_gateway_name VARCHAR(45)
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
		GatewayName = p_gateway_name;
	
	IF gateway_id IS NULL THEN
		SIGNAL SQLSTATE '45000' 
			SET MESSAGE_TEXT = "Specified Gateway Name does not exist";
    END IF;
	
	SELECT idSensorsGatewayXref INTO xc_link FROM SensorsGatewayXref xc WHERE
		xc.SensorsGatewayXref_SensorId = sensor_id AND
        xc.SensorsGatewayXref_GatewayId = gateway_id;
	
    IF xc_link IS NOT NULL THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = "Sensor already linked to gateway";
    END IF;
    
    INSERT INTO SensorsGatewayXref (SensorsGatewayXref_GatewayId, SensorsGatewayXref_SensorId) VALUES(gateway_id, sensor_id);
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
-- View `sensors_and_gateways`.`SensorGatewayPairs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sensors_and_gateways`.`SensorGatewayPairs`;
USE `sensors_and_gateways`;
CREATE  OR REPLACE VIEW `SensorGatewayPairs` AS
SELECT gw.GatewayName as `Gateway Name`, s.SensorName as `Sensor Name` FROM Gateways gw JOIN Sensors s JOIN SensorsGatewayXref AS xc ON
	gw.idGateway = xc.SensorsGatewayXref_GatewayId AND
    s.idSensor = xc.SensorsGatewayXref_SensorId;

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
SELECT gw.idGateway AS "Gateway ID", gw.GatewayName AS "Gateway Name", s.idSensor AS "Sensor ID", s.SensorName AS "Sensor Name" FROM Gateways gw JOIN Sensors s JOIN SensorsGatewayXref xc
	ON 
		gw.idGateway = xc.SensorsGatewayXref_GatewayId AND
        s.idSensor = xc.SensorsGatewayXref_SensorId;

-- -----------------------------------------------------
-- View `sensors_and_gateways`.`SensorGatewayPairsExtendedSummary`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `sensors_and_gateways`.`SensorGatewayPairsExtendedSummary`;
USE `sensors_and_gateways`;
CREATE  OR REPLACE VIEW `SensorGatewayPairsExtendedSummary` AS
SELECT `Gateway ID`, `Gateway Name`, GROUP_CONCAT(`Sensor ID` ORDER BY `Sensor ID` SEPARATOR ", ") AS "Linked Sensor IDs", GROUP_CONCAT(`Sensor Name` ORDER BY `Sensor Name` SEPARATOR ", ") AS "Linked Sensor Names" FROM SensorGatewayPairsExtended GROUP BY `Gateway ID`, `Gateway Name`;
USE `sensors_and_gateways`;

DELIMITER $$
USE `sensors_and_gateways`$$
CREATE DEFINER = CURRENT_USER TRIGGER `sensors_and_gateways`.`SensorsGatewayXref_BEFORE_INSERT` BEFORE INSERT ON `SensorsGatewayXref` FOR EACH ROW
BEGIN
	 DECLARE link_exists INT DEFAULT 0;

    SELECT COUNT(*) INTO link_exists
    FROM SensorsGatewayXref
    WHERE SensorsGatewayXref_GatewayId = NEW.SensorsGatewayXref_GatewayId
      AND SensorsGatewayXref_SensorId  = NEW.SensorsGatewayXref_SensorId;

    IF link_exists > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Duplicate link: this sensor is already linked to this gateway';
    END IF;
END$$

USE `sensors_and_gateways`$$
CREATE DEFINER = CURRENT_USER TRIGGER `sensors_and_gateways`.`SensorsGatewayXref_BEFORE_UPDATE` BEFORE UPDATE ON `SensorsGatewayXref` FOR EACH ROW
BEGIN
	 DECLARE link_exists INT DEFAULT 0;

    SELECT COUNT(*) INTO link_exists
    FROM SensorsGatewayXref
    WHERE SensorsGatewayXref_GatewayId = NEW.SensorsGatewayXref_GatewayId
      AND SensorsGatewayXref_SensorId  = NEW.SensorsGatewayXref_SensorId
      -- Unlike insert, we must exclude the current row being updated or it will always say it exists.
	  AND idSensorsGatewayXref  <> OLD.idSensorsGatewayXref ;
    IF link_exists > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Duplicate link: this sensor is already linked to this gateway';
    END IF;
END$$


DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
