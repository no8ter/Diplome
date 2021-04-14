from sqlite3 import connect

db = connect('database.db')
cur = db.cursor()

sql = '''
    Create table if not exists `users`(
        `login` text not null primary key,
        `password` text not null,
        `firstName` text DEFAULT " " NOT NULL,
        `secondName` text DEFAULT " " NOT NULL,
        `thridName` text DEFAULT " " NOT NULL,
        `birthday` text DEFAULT " " NOT NULL,
        `birthplace` text DEFAULT " " NOT NULL,
        `country` text DEFAULT " " NOT NULL,
        `passID` text DEFAULT " " NOT NULL,
        `passDate` text DEFAULT " " NOT NULL,
        `passCountry` text DEFAULT " " NOT NULL,
        `schoolName` text DEFAULT " " NOT NULL,
        `schoolDate` text DEFAULT " " NOT NULL,
        `schoolAttestate` text DEFAULT " " NOT NULL,
        `passportLivePlace` text DEFAULT " " NOT NULL,
        `currentLivePlace` text DEFAULT " " NOT NULL,
        `phoneNumber` text DEFAULT " " NOT NULL,
        `commissariat` text DEFAULT " " NOT NULL,
        `secondLanguage` text DEFAULT " " NOT NULL,
        `medicalGroup` text DEFAULT " " NOT NULL,
        `needHostelSelect` bool,
        `motherName` text DEFAULT " " NOT NULL,
        `motherPhone` text DEFAULT " " NOT NULL,
        `fatherName` text DEFAULT " " NOT NULL,
        `fatherPhone` text DEFAULT " " NOT NULL,
        `statement` text DEFAULT " " NOT NULL,
        `info` text DEFAULT " " NOT NULL
    );

    Create table if not exists `claims`(
        `userID` int not null,
        `specialID` int not null,
        `specEducationFirstTime` bool,
        `specLicense` bool,
        `specOriginalDocs` bool,
        `specPersonalData` bool
    );

    Create table if not exists `profs`(
        `spec_id` text not null primary key,
        `name` text not null,
        `spec_data` text
        `info` text,
        `legend` text,
        `photoWay` text
    );

    CREATE TABLE IF NOT EXISTS `settings`(
        `property` text PRIMARY KEY,
        `value` text DEFAULT "False"
    );

    Insert or ignore into `users`(`login`,`password`,`firstName`,`statement`,`info`) values(
        'admin', 'admin', 'Administrator', 'Администратор', 'default'
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

'''

Draft = '''

Create table `logs`(
        `login` text not null,
        `time` text
    );

'''
cur.executescript(sql)
db.commit()
