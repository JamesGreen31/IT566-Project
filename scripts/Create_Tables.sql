USE `sensors_and_gateways`;

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
-- Table `sensors_and_gateways`.`SensorsGatewaysXref`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sensors_and_gateways`.`SensorsGatewaysXref` (
  `idSensorsGatewayXref` INT NOT NULL AUTO_INCREMENT,
  `idSensor` INT NOT NULL,
  `idGateway` INT NOT NULL,
  PRIMARY KEY (`idSensorsGatewayXref`),
  INDEX `SensorsGatewayXref_SensorId_idx` (`idSensor` ASC) VISIBLE,
  INDEX `SensorsGatewayXref_GatewayId_idx` (`idGateway` ASC) VISIBLE,
  CONSTRAINT `FK_SGX_Sensors_idSensor`
    FOREIGN KEY (`idSensor`)
    REFERENCES `sensors_and_gateways`.`Sensors` (`idSensor`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_SGX_Gateways_idGateway`
    FOREIGN KEY (`idGateway`)
    REFERENCES `sensors_and_gateways`.`Gateways` (`idGateway`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
