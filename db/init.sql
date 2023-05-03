DROP TABLE IF EXISTS country CASCADE;

CREATE TABLE country (
  code CHAR(3) NOT NULL,
  surface_area DECIMAL(10,2) NOT NULL DEFAULT 0,
  indep_year SMALLINT,
  population BIGINT NOT NULL DEFAULT 0,
  life_expectancy DECIMAL(3,1),
  gnp DECIMAL(10,2),
  gnp_old DECIMAL(10,2),
  capital DECIMAL(11),
  PRIMARY KEY (code)
);

DROP TABLE IF EXISTS city CASCADE;

CREATE TABLE city (
  id SERIAL,
  country_code CHAR(3) NOT NULL,
  population DECIMAL(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  CONSTRAINT city_ibfk_1 FOREIGN KEY (country_code) REFERENCES country (code)
);

COPY country FROM '/Users/trueshot/Downloads/Country.csv' DELIMITER ',' CSV HEADER;

COPY city FROM '/Users/trueshot/Downloads/City.csv' DELIMITER ',' CSV HEADER;
