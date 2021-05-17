CREATE TABLE profs ( 
	spec_id              text     ,
	name                 text     ,
	spec_data            text     ,
	legend               text     ,
	photoWay             text     ,
	CONSTRAINT Unq_profs_spec_id UNIQUE ( spec_id ) 
 );
;
CREATE TABLE users ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	login                text     ,
	password             text     ,
	rules                text NOT NULL DEFAULT '����������'   
 , email text);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE abiturients ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	userID               integer     ,
	fname                varchar(100) NOT NULL    ,
	sname                varchar(100) NOT NULL    ,
	tname                varchar(100)     ,
	birthday             date NOT NULL    ,
	birthplace           text     ,
	country              text     ,
	FOREIGN KEY ( userID ) REFERENCES users( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );
CREATE TABLE claims ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	abitID               integer NOT NULL    ,
	spec_id              text NOT NULL    ,
	schoolName           text NOT NULL    ,
	endDate              date NOT NULL    ,
	attestate            text NOT NULL    ,
	passPlace            text NOT NULL    ,
	livePlace            text     ,
	phone                text NOT NULL    ,
	army                 text  DEFAULT 'none'   ,
	lang                 text NOT NULL    ,
	healthGroup          text NOT NULL    ,
	needHostel           boolean NOT NULL    ,
	motherName           text     ,
	motherPhone          text     ,
	fatherName           text     ,
	fatherPhone          text     ,
	consents             boolean NOT NULL DEFAULT True   , 
	marksAverage 		 float not null default 2.0     ,
	FOREIGN KEY ( spec_id ) REFERENCES profs( spec_id ) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY ( abitID ) REFERENCES abiturients( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );
CREATE TABLE passports ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	abitID               integer NOT NULL    ,
	serial               integer NOT NULL    ,
	number               integer NOT NULL    ,
	date                 date NOT NULL    ,
	creator              text NOT NULL    ,
	FOREIGN KEY ( abitID ) REFERENCES abiturients( id ) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT unq UNIQUE (serial, number)
 );
;
