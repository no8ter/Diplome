from sqlite3 import connect

db = connect('database.db')
c = db.cursor()


sql = """

CREATE TABLE profs ( 
	spec_id              text     ,
	name                 text     ,
	spec_data            text     ,
	legend               text     ,
	photoWay             text     ,
	CONSTRAINT Unq_profs_spec_id UNIQUE ( spec_id ) 
 );

CREATE TABLE users ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	login                text     ,
	password             text     ,
	email				 text     ,
	rules                text NOT NULL DEFAULT 'Абитуриент'   
 );

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


    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '08.02.09', 'Монтаж, наладка и эксплуатация электрооборудования промышленных и гражданских зданий', ''
    );
    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '11.01.01', 'Монтажник радиоэлектронной аппаратуры и приборов', ''
    );
    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '11.02.16', 'Монтаж, техническое обслуживание и ремонт электронных приборов и устройств', 'ТОП-50'
    );
    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '15.01.32', 'Оператор станков с программным управлением', ''
    );
    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '23.02.05', 'Эксплуатация транспортного электрооборудования и автоматики', ''
    );


    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '15.02.15', 'Технология металлообрабатывающего производства', 'ТОП-50'
    );
    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '35.02.03', 'Технология деревообработки', ''
    );
    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '43.02.12', 'Технология эстетических услуг', 'ТОП-50'
    );
    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '43.02.13', 'Технология парикмахерского искусства', 'ТОП-50'
    );


    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '09.02.07', 'Информационные системы и программирование', 'ТОП-50'
    );
    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '38.02.01', 'Экономика и бухгалтерский учет', ''
    );
    Insert or ignore into `profs` (`spec_id`, `name`, `spec_data`) values(
        '46.02.01', 'Документационное обеспечение управления и архивоведение', ''
    );

"""

c.executescript(sql)

db.commit()
db.close()
exit()