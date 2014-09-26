SET SESSION storage_engine = "InnoDB";

-- beijing time_zone
SET SESSION time_zone = "+8:00";
 
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS complainList;
CREATE TABLE complainList (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,    
    num INT NOT NULL,
    brand VARCHAR(50) NOT NULL,
    family VARCHAR(50) NOT NULL,
    version VARCHAR(50) NOT NULL,   
    abstract VARCHAR(100) NOT NULL,
	detailUrl VARCHAR(100) NOT NULL,
    failure VARCHAR(100) NOT NULL,
	published DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    collectTime TIMESTAMP NOT NULL,	
    KEY (id)
);


DROP TABLE IF EXISTS complainDetail;
CREATE TABLE complainDetail (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cnum INT NOT NULL,    
    published TIMESTAMP NOT NULL,
	img VARCHAR(100) DEFAULT NULL,
    content MEDIUMTEXT NOT NULL,	
    reply MEDIUMTEXT DEFAULT NULL,
	collectTime TIMESTAMP NOT NULL,
	KEY (id)
);