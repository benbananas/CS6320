-- Halfway modified, got lazy but this is only if we end up wanting the full DB

DROP TABLE IF EXISTS Country;

CREATE TABLE Country (
  Code char(3) NOT NULL  ,
  Name char(52) NOT NULL  ,
  Continent enum(Asia,Europe,North America,Africa,Oceania,Antarctica,South America) NOT NULL  Asia,
  Region char(26) NOT NULL  ,
  SurfaceArea float(10,2) NOT NULL  0.00,
  IndepYear smallint(6)  NULL,
  Population int(11) NOT NULL  0,
  LifeExpectancy float(3,1)  NULL,
  GNP float(10,2)  NULL,
  GNPOld float(10,2)  NULL,
  LocalName char(45) NOT NULL  ,
  GovernmentForm char(45) NOT NULL  ,
  HeadOfState char(60)  NULL,
  Capital int(11)  NULL,
  Code2 char(2) NOT NULL  ,
  PRIMARY KEY (Code)
) ENGINE=InnoDB  CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

COPY Country FROM /Users/trueshot/Downloads/Country.csv DELIMITER , CSV HEADER;

DROP TABLE IF EXISTS City;

CREATE TABLE City (
  ID int(11) NOT NULL AUTO_INCREMENT,
  Name char(35) NOT NULL  ,
  CountryCode char(3) NOT NULL  ,
  District char(20) NOT NULL  ,
  Population int(11) NOT NULL  0,
  PRIMARY KEY (ID),
  KEY City_CountryCode (CountryCode) USING BTREE,
  CONSTRAINT city_ibfk_1 FOREIGN KEY (CountryCode) REFERENCES Country (Code)
) ENGINE=InnoDB AUTO_INCREMENT=4080  CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

COPY City FROM /Users/trueshot/Downloads/City.csv DELIMITER , CSV HEADER;
