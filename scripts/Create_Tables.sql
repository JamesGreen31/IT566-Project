-- -----------------------------------------------------
-- TABLES
-- -----------------------------------------------------

USE `sensors_and_gateways`;

CREATE TABLE IF NOT EXISTS Sensors (
  idSensor INT NOT NULL AUTO_INCREMENT,
  SensorName VARCHAR(45) NOT NULL,
  PRIMARY KEY (idSensor),
  UNIQUE INDEX SensorName_UNIQUE (SensorName ASC) VISIBLE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Gateways (
  idGateway INT NOT NULL AUTO_INCREMENT,
  GatewayName VARCHAR(45) NOT NULL,
  PRIMARY KEY (idGateway),
  UNIQUE INDEX GatewayName_UNIQUE (GatewayName ASC) VISIBLE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS SensorsGatewaysXref (
  idSensorsGatewayXref INT NOT NULL AUTO_INCREMENT,
  idSensor INT NOT NULL,
  idGateway INT NOT NULL,
  PRIMARY KEY (idSensorsGatewayXref),
  INDEX SensorsGatewayXref_SensorId_idx (idSensor ASC) VISIBLE,
  INDEX SensorsGatewayXref_GatewayId_idx (idGateway ASC) VISIBLE,
  CONSTRAINT FK_SGX_Sensors_idSensor FOREIGN KEY (idSensor)
      REFERENCES Sensors (idSensor) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT FK_SGX_Gateways_idGateway FOREIGN KEY (idGateway)
      REFERENCES Gateways (idGateway) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB;
