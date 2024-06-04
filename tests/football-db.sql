CREATE DATABASE football;

USE football;

CREATE TABLE countries( 
	country_id    INT, 
	country_name     VARCHAR(50) NOT NULL, 
	PRIMARY KEY  (country_id)
    );
    
INSERT INTO countries
VALUES (
	1,
	'India'
	);
    
INSERT INTO countries
VALUES (
	2,
	'Turkey'
	);  
    
INSERT INTO countries
VALUES (
	3,
	'Usa'
	);  
    
INSERT INTO countries
VALUES (
	4,
	'Germany'
	);
    
INSERT INTO countries
VALUES (
	5,
	'France'
	);  
    
INSERT INTO countries
VALUES (
	6,
	'Brazil'
	); 
    
    INSERT INTO countries
VALUES (
	7,
	'Argentina'
	);
    
INSERT INTO countries
VALUES (
	8,
	'The Netherlands'
	);  
    
INSERT INTO countries
VALUES (
	9,
	'Azerbaijan'
	); 
    
INSERT INTO countries
VALUES (
	10,
	'Italy'
	); 
    


CREATE TABLE leagues( 
	league_id INT, 
	league_name     VARCHAR(50) NOT NULL, 
	country_id INT,
	FOREIGN KEY (country_id) 
		REFERENCES countries (country_id), 
	PRIMARY KEY  (league_id)
    );


INSERT INTO leagues
VALUES (
	1,
	'Indian Super League ',
	1
	); 
INSERT INTO leagues
VALUES (
	2,
	'I-League ',
	1
	);     
INSERT INTO leagues
VALUES (
	3,
	'Turkey Super League ',
	2
	); 
INSERT INTO leagues
VALUES (
	4,
	'U-League ',
	3
	); 
INSERT INTO leagues
VALUES (
	5,
	'American Super League ',
	3
	); 
INSERT INTO leagues
VALUES (
	6,
	'G-League ',
	4
	); 
    
INSERT INTO leagues
VALUES (
	7,
	'France Super League ',
	 5
	); 
INSERT INTO leagues
VALUES (
	8,
	'F-League ',
	5
	); 
INSERT INTO leagues
VALUES (
	9,
	'Brazilian Super League ',
	6
	); 
INSERT INTO leagues
VALUES (
	10,
	'A-League ',
    7
	); 
    
INSERT INTO leagues
VALUES (
	11,
	'Argentian Super League ',
    7
	); 
INSERT INTO leagues
VALUES (
	12,
	'N-League ',
    8
	);  
    
INSERT INTO leagues
VALUES (
	13, 
	'Azerbaijan Super League ',
    9
	); 
    
INSERT INTO leagues
VALUES (
	14,
	'Italian Super League ',
    10
	); 
    
CREATE TABLE players( 
	player_id    INT, 
	first_name     VARCHAR(50) NOT NULL, 
	last_name      VARCHAR(55), 
    country_id INT NOT NULL,
	FOREIGN KEY (country_id) 
		REFERENCES countries (country_id), 
	PRIMARY KEY  (player_id),
    UNIQUE (player_id)
    );
    
    INSERT INTO players
    VALUES (
		1,
        'Sunil',
        'Chhetri',
        1
        );

INSERT INTO players
    VALUES (
		2,
        'Bhaichung ',
        'Bhutia',
        1
        );
INSERT INTO players
    VALUES (
		3,
        'Shabbir',
        'Ali',
        1
        );
        
INSERT INTO players
    VALUES (
		4,
        'Climax',
        'Lawrence',
        1
        );
	
INSERT INTO players
    VALUES (
		5,
        'Hakan',
        'Calhanoglu',
        2
        );

INSERT INTO players
    VALUES (
		6,
        'Volkan',
        'Babacan',
        2
        );
        
    INSERT INTO players
    VALUES (
		7,
        'Hakan',
        'Balta',
        2
        );
        
	INSERT INTO players
    VALUES (
		8,
        'Matt ',
        'Turner',
        3
        );
        
	INSERT INTO players
    VALUES (
		9,
        'Tim',
        'Ream',
        3
        );
         
         
	INSERT INTO players
    VALUES (
		10,
        'Weston',
        'McKennie',
        3
        );
        
	INSERT INTO players
    VALUES (
		11,
        'Manuel',
        'Neuer',
        4
        );
        
	INSERT INTO players
    VALUES (
		12,
        'David',
        'Raum',
        4
        );
        
	INSERT INTO players
    VALUES (
		13,
        'Jamal',
        'Musiala',
        4
        );  
        
	
    INSERT INTO players
    VALUES (
		14,
        'Hugo',
        'Lloris',
        5
        );
        
       
    INSERT INTO players
    VALUES (
		15,
        'Victor',
        'Hugo',
        5
        );    
	
    INSERT INTO players
    VALUES (
		16,
        'Didier',
        'Deschamps',
        5
        );
	
    INSERT INTO players
    VALUES (
		17,
        'Neymar',
        '',
        6
        );
        
	INSERT INTO players
    VALUES (
		18,
        'Thiago',
        'Silva',
         6
        );
        
	INSERT INTO players
    VALUES (
		19,
        'Danilo',
        '',
        6
        );
        
	INSERT INTO players
    VALUES (
		20,
        'Lionel',
        'Messi',
        7
        );
	
    INSERT INTO players
    VALUES (
		21,
        'Juan',
        'Foyth',
        7
        );

	INSERT INTO players
    VALUES (
		22,
        'Remko',
        'Pasveer',
        8
        );
	
    INSERT INTO players
    VALUES (
		23,
        'Shahrudin',
        'Mahammadaliye',
        9
        );
        
	INSERT INTO players
    VALUES (
		24,
        'Leonardo',
        'Bonucci',
        10
        );
        
	INSERT INTO players
    VALUES (
		25,
        'Nicolo',
        'Barella',
        10
        );
        
    CREATE TABLE teams( 
    team_id INT,
    team_name VARCHAR(60),
    country_id INT,
    FOREIGN KEY (country_id) 
		REFERENCES countries (country_id),
	PRIMARY KEY  (team_id)
    );

INSERT INTO teams
VALUES (
	1,
	'Indian team ',
    1
	);  

INSERT INTO teams
VALUES (
	2,
	'Indian team-2 ',
    1
	);  

INSERT INTO teams
VALUES (
	3,
	'Turkish team ',
    2
	);  

INSERT INTO teams
VALUES (
	4,
	'USA team ',
    3
	); 
    
    INSERT INTO teams
VALUES (
	5,
	'USA team-2',
    3
	); 
    
    INSERT INTO teams
VALUES (
	6,
	'German team',
    4
	); 
    INSERT INTO teams
VALUES (
	7,
	'France team',
    5
	); 
    INSERT INTO teams
VALUES (
	8,
	'France team-2',
    5
	); 
    INSERT INTO teams
VALUES (
	9,
	'Brazilian team',
    6
	); 
    
    INSERT INTO teams
VALUES (
	10,
	'Argentian team',
    7
	); 
    INSERT INTO teams
VALUES (
	11,
	'Argentian team-2',
    7
	); 
     INSERT INTO teams
VALUES (
	12,
	'Dutch team',
    8
	); 
    INSERT INTO teams
VALUES (
	13,
	'Azerbaijani team',
    9
	); 
    INSERT INTO teams
VALUES (
	14,
	'Italian team',
    10
	); 
    
   CREATE TABLE seasons (
   season_id INT,
   season_year INT,
   PRIMARY KEY (season_id)
   );
   
   INSERT INTO seasons
VALUES (
	05,
	2005
	); 
   
     INSERT INTO seasons
VALUES (
	13,
	2013
	); 
    
      INSERT INTO seasons
VALUES (
	14,
	2014
	); 
    
      INSERT INTO seasons
VALUES (
	15,
	2015
	); 
    
      INSERT INTO seasons
VALUES (
	16,
	2016
	); 
    
      INSERT INTO seasons
VALUES (
	17,
	2017
	); 
    
      INSERT INTO seasons
VALUES (
	18,
	2018
	); 
    
      INSERT INTO seasons
VALUES (
	19,
	2019
	); 
    
      INSERT INTO seasons
VALUES (
	20,
	2020
	); 
    
      INSERT INTO seasons
VALUES (
	21,
	2021
	); 
    
      INSERT INTO seasons
VALUES (
	22,
	2022
	); 
    

   
    CREATE TABLE champions( 
    algmt_number INT,
	season_id    INT,
	league_id INT, 
    champion_id INT,
	FOREIGN KEY (league_id) 
		REFERENCES leagues(league_id), 
    FOREIGN KEY (champion_id) 
		REFERENCES teams(team_id), 
	FOREIGN KEY (season_id)
		REFERENCES seasons(season_id),
	PRIMARY KEY  (algmt_number)
    );
    
     INSERT INTO champions
VALUES (
	1,
    05,
    1,
    1
    );
    
     INSERT INTO champions
VALUES (
	2,
    05,
    3,
    3
    );
    
	INSERT INTO champions
VALUES (
	3,
    13,
    2,
    1
    );

 INSERT INTO champions
VALUES (
	4,
    13,
    14,
    14
    );
    
     INSERT INTO champions
VALUES (
	5,
    14,
	6,
    6
    );
    
      INSERT INTO champions
VALUES (
	6,
    14,
	12,
    12
    );
    
    INSERT INTO champions
VALUES (
	7,
    14,
	9,
    9
    );
    
	INSERT INTO champions
VALUES (
	8,
    15,
	10,
    11
    );
	
    INSERT INTO champions
VALUES (
	9,
    15,
	3,
    3
    );
    
	INSERT INTO champions
VALUES (
	10,
    16,
	5,
    4
    );
    
    INSERT INTO champions
VALUES (
	11,
    16,
	12,
    12
    );
    
    INSERT INTO champions
VALUES (
	12,
    16,
	4,
    5
    );
    
      INSERT INTO champions
VALUES (
	13,
    17,
	11,
    10
    );
   
   INSERT INTO champions
VALUES (
	14,
    17,
	10,
    11
    );
    
    INSERT INTO champions
VALUES (
	15,
    17,
	13,
    13
    );
    
    INSERT INTO champions
VALUES (
	16,
    17,
	8,
    7
    );
    
     INSERT INTO champions
VALUES (
	17,
    18,
	2,
    2
    );
    
    INSERT INTO champions
VALUES (
	18,
    18,
	7,
    8
    );
    
    INSERT INTO champions
VALUES (
	19,
    19,
	6,
    6
    );
    
     INSERT INTO champions
VALUES (
	20,
    19,
	4,
    4
    );
     INSERT INTO champions
VALUES (
	21,
    20,
	8,
    7
    );
    
     INSERT INTO champions
VALUES (
	22,
    20,
	5,
    5
    );
     INSERT INTO champions
VALUES (
	23,
    20,
	13,
    13
    );
    
    INSERT INTO champions
VALUES (
	24,
    21,
	3,
    3
    );
    
    INSERT INTO champions
VALUES (
	25,
    21,
	14,
    14
    );
    
     INSERT INTO champions
VALUES (
	26,
    22,
	9,
    9
    );
    
    INSERT INTO champions
VALUES (
	27,
    22,
	6,
    6
    );
    
    INSERT INTO champions
VALUES (
	28,
    22,
	1,
    1
    );
    INSERT INTO champions
VALUES (
	29,
    22,
	12,
    12
    );
    
    INSERT INTO champions
VALUES (
	30,
    22,
	11,
    11
    );
    
    CREATE TABLE player_team( 
    team_player_id INT,
	player_id INT, 
	team_id INT, 
	start_date   DATE  NOT NULL, 
    end_date   DATE, 
    income DECIMAL(8,2),
    CHECK (income>0),
	FOREIGN KEY (player_id) 
		REFERENCES players(player_id), 
    FOREIGN KEY (team_id) 
		REFERENCES teams(team_id),
	PRIMARY KEY (team_player_id)
    );
    
INSERT INTO player_team
VALUES (
	1,
	1,
    5,
    STR_TO_DATE('01-JAN-2016', '%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2018','%d-%M-%Y'),
    50000
	);  
    
INSERT INTO player_team
VALUES (
	2,
	1,
    8,
    STR_TO_DATE('01-JAN-2018', '%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    80000
	);  
    
INSERT INTO player_team
VALUES (
	3,
	2,
    2,
    STR_TO_DATE('01-JAN-2018', '%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    68000
	);  
    
INSERT INTO player_team
VALUES (
	4,
	2,
    1,
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
    70000
	);  
    
INSERT INTO player_team
VALUES (
	5,
	2,
    2,
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    59000
	);  
    
INSERT INTO player_team
VALUES (
	6,
	3,
    8,
    STR_TO_DATE('01-JAN-2016', '%d-%M-%Y'),
	STR_TO_DATE('%d-%M-%Y', null),
    62000
	);  
    
INSERT INTO player_team
VALUES (
	7,
	4,
    5,
    STR_TO_DATE('01-JAN-2017', '%d-%M-%Y'),
	STR_TO_DATE('%d-%M-%Y', null),
    90000
	);  
    
INSERT INTO player_team
VALUES (
	8,
	5,
    3,
    STR_TO_DATE('01-JAN-2015', '%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    49000
	);  
    
INSERT INTO player_team
VALUES (
	9,
	5,
    7,
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
    39000
	);  
    
INSERT INTO player_team
VALUES (
	10,
	6,
    3,
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
	STR_TO_DATE('%d-%M-%Y', null),
    53000
	); 
    
INSERT INTO player_team
VALUES (
	11,
	7,
    4,
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
    72000
	); 
    
INSERT INTO player_team
VALUES (
	12,
	7,
    10,
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
	STR_TO_DATE('%d-%M-%Y', null),
    55000
	); 
    
    INSERT INTO player_team
VALUES (
	13,
	8,
    5,
    STR_TO_DATE('01-JAN-2018','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    83000
	); 
    
      INSERT INTO player_team
VALUES (
	14,
	9,
    4,
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2020','%d-%M-%Y'),
    79000
	); 
    
      INSERT INTO player_team
VALUES (
	15,
	9,
    5,
    STR_TO_DATE('01-JAN-2020','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    76000
	); 
    
     INSERT INTO player_team
VALUES (
	16,
	10,
    5,
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2020','%d-%M-%Y'),
    48000
	); 
    
     INSERT INTO player_team
VALUES (
	17,
	10,
    6,
    STR_TO_DATE('01-JAN-2020','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2022','%d-%M-%Y'),
    53000
	); 
    
INSERT INTO player_team
VALUES (
	18,
	11,
    7,
    STR_TO_DATE('01-JAN-2005','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    61000
	); 
    
INSERT INTO player_team
VALUES (
	19,
	11,
    8,
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    73000
	); 
    
    INSERT INTO player_team
VALUES (
	20,
	11,
    12,
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    84000
	); 
    
INSERT INTO player_team
VALUES (
	21,
	12,
    3,
    STR_TO_DATE('01-JAN-2005','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2018','%d-%M-%Y'),
    46000
	); 
    
INSERT INTO player_team
VALUES (
	22,
	13,
    4,
    STR_TO_DATE('01-JAN-2018','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    56000
	); 
    
    INSERT INTO player_team
VALUES (
	23,
	14,
    7,
    STR_TO_DATE('01-JAN-2015','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    57000
	); 
    
    INSERT INTO player_team
VALUES (
	24,
	15,
    8,
    STR_TO_DATE('01-JAN-2005','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2015','%d-%M-%Y'),
    66000
	); 
    
INSERT INTO player_team
VALUES (
	25,
	15,
    1,
    STR_TO_DATE('01-JAN-2015','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    68000
	); 
    
    INSERT INTO player_team
VALUES (
	26,
	16,
    6,
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    94000
	); 
    
     INSERT INTO player_team
VALUES (
	27,
	16,
    13,
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    87000
	); 
        
INSERT INTO player_team
VALUES (
	28,
	17,
    10,
    STR_TO_DATE('01-JAN-2020','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    74000
	); 
    
    INSERT INTO player_team
VALUES (
	29,
	18,
    3,
    STR_TO_DATE('01-JAN-2005','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2018','%d-%M-%Y'),
    77000
	); 
    
    INSERT INTO player_team
VALUES (
	30,
	18,
    10,
    STR_TO_DATE('01-JAN-2018','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    89000
	); 
    
INSERT INTO player_team
VALUES (
	31,
	19,
    11,
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    64000
	); 
    
    INSERT INTO player_team
VALUES (
	32,
	20,
    11,
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    61000
	); 
    
     INSERT INTO player_team
VALUES (
	33,
	21,
    9,
    STR_TO_DATE('01-JAN-2014','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    42000
	); 
    
    INSERT INTO player_team
VALUES (
	34,
	22,
    12,
    STR_TO_DATE('01-JAN-2014','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
    51000
	); 
    
INSERT INTO player_team
VALUES (
	35,
	22,
    9,
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    67000
	); 
    
    INSERT INTO player_team
VALUES (
	36,
	23,
    13,
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2020','%d-%M-%Y'),
    75000
	); 
    
     INSERT INTO player_team
VALUES (
	37,
	23,
    3,
    STR_TO_DATE('01-JAN-2020','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
    77000
	); 
    
        INSERT INTO player_team
VALUES (
	38,
	24,
    14,
    STR_TO_DATE('01-JAN-2015','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2018','%d-%M-%Y'),
    82000
	); 
    
     INSERT INTO player_team
VALUES (
	39,
	25,
    6,
    STR_TO_DATE('01-JAN-2014','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2015','%d-%M-%Y'),
    47000
	); 
    
      INSERT INTO player_team
VALUES (
	40,
	25,
    14,
    STR_TO_DATE('01-JAN-2015','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    50000
	); 
    
      INSERT INTO player_team
VALUES (
	41,
	25,
    7,
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
    86000
	); 
    
    
    
 CREATE TABLE team_season_league( 
    tsl_id INT,
	team_id    INT, 
    start_season DATE NOT NULL, 
    end_season DATE, 
    league_id INT, 
	FOREIGN KEY (league_id) 
		REFERENCES leagues (league_id), 
    FOREIGN KEY (team_id) 
		REFERENCES teams (team_id), 
	PRIMARY KEY  (tsl_id)
    );    
    
    INSERT INTO team_season_league
    VALUES (
    1,
    1,
    STR_TO_DATE('01-JAN-2005','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2013','%d-%M-%Y'),
	1    
    );
    
     INSERT INTO team_season_league
    VALUES (
    2,
    1,
    STR_TO_DATE('01-JAN-2013','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
	2    
    );
    
     INSERT INTO team_season_league
    VALUES (
    3,
    1,
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
   STR_TO_DATE('%d-%M-%Y', null),
	1    
    );
    
     INSERT INTO team_season_league
    VALUES (
    4,
    2,
    STR_TO_DATE('01-JAN-2018','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
	2    
    );
    
     INSERT INTO team_season_league
    VALUES (
    5,
    2,
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
	STR_TO_DATE('%d-%M-%Y', null),
	1       
    );
    
    INSERT INTO team_season_league
    VALUES (
    6,
    3,
    STR_TO_DATE('01-JAN-2005','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	3    
    );
    
    
    INSERT INTO team_season_league
    VALUES (
    7,
    4,
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
	5   
    );
    
    INSERT INTO team_season_league
    VALUES (
    8,
    4,
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
	4   
    );
    
    INSERT INTO team_season_league
    VALUES (
    9,
    4,
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	5   
    );
    
    INSERT INTO team_season_league
    VALUES (
    10,
    5,
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
	4   
    );
    
    INSERT INTO team_season_league
    VALUES (
    11,
    5,
    STR_TO_DATE('01-JAN-2019','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	5   
    );
    
    
     INSERT INTO team_season_league
    VALUES (
    12,
    6,
    STR_TO_DATE('01-JAN-2014','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	6   
    );
    
    
     INSERT INTO team_season_league
    VALUES (
    13,
    7,
    STR_TO_DATE('01-JAN-2005','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
	7   
    );
    
     INSERT INTO team_season_league
    VALUES (
    14,
    7,
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	8   
    );
    
    
     INSERT INTO team_season_league
    VALUES (
    15,
    8,
    STR_TO_DATE('01-JAN-2005','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	7  
    );
    
     
    INSERT INTO team_season_league
    VALUES (
    16,
    9,
    STR_TO_DATE('01-JAN-2014','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	9  
    );
    
    
    INSERT INTO team_season_league
    VALUES (
    17,
    10,
    STR_TO_DATE('01-JAN-2017','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	11  
    );
    
    
    INSERT INTO team_season_league
    VALUES (
    18,
    11,
    STR_TO_DATE('01-JAN-2015','%d-%M-%Y'),
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
	10  
    );
    
     INSERT INTO team_season_league
    VALUES (
    19,
    11,
    STR_TO_DATE('01-JAN-2021','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	11  
    );
    
    
    INSERT INTO team_season_league
    VALUES (
    20,
    12,
    STR_TO_DATE('01-JAN-2014','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	12  
    );
    
    
    INSERT INTO team_season_league
    VALUES (
    21,
    13,
    STR_TO_DATE('01-JAN-2016','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	13  
    );
    
    INSERT INTO team_season_league
    VALUES (
    22,
    14,
    STR_TO_DATE('01-JAN-2013','%d-%M-%Y'),
    STR_TO_DATE('%d-%M-%Y', null),
	14
    );
    
/*
#question 7, team with most champions in each country
  
select t.team_name, COUNT(t.team_id) as counter
from teams t join champions ch
on (t.team_id = ch.champion_id)
join leagues l
on (l.league_id = ch.league_id)
join countries c
on (c.country_id = l.country_id)
group by t.team_id
having MAX(t.team_id = ch.champion_id)
    

#question 8 Find out which teams each player plays for.

SELECT  DISTINCT p.first_name, p.last_name, t.team_name
from player_team pt join players p
on p.player_id=pt.player_id
join teams t
on t.team_id=pt.team_id
order by p.first_name

# question 9, Find the total income earned by each player during his career. 

SELECT player_id, SUM(income)
from player_team
group by player_id
order by player_id;



#question 10, Find out how many foreign players currently play in each team. 

SELECT t.team_name, COUNT(p.player_id)
from player_team pt join teams t
on pt.team_id=t.team_id
join players p
on p.player_id=pt.player_id
where end_date IS NULL and t.country_id!=p.country_id
group by t.team_name;


# question 11, Find out how many foreign players played for each team in the past. 

SELECT t.team_name, COUNT(p.player_id)
from player_team pt join teams t
on pt.team_id=t.team_id
join players p
on p.player_id=pt.player_id
where end_date IS  NOT NULL and t.country_id!=p.country_id
group by t.team_name;


#question 12, Find current league of each team. 

SELECT t.team_name, l.league_name
from team_season_league tsl join teams t
on tsl.team_id=t.team_id
join leagues l
on tsl.league_id=l.league_id
where end_season IS NULL;



#question 13, Find out in which league each team was in the 5 years after January 1, 2000 

SELECT t.team_name, l.league_name, tsl.start_season, tsl.end_season
from team_season_league tsl join teams t
on tsl.team_id=t.team_id
join leagues l
on l.league_id=tsl.league_id
where (tsl.end_season>=str_to_date('01-JAN-2000','%d-%M-%Y') AND tsl.end_season<=date_add(str_to_date('01-JAN-2000','%d-%M-%Y'), INTERVAL 5 YEAR ))
OR(tsl.start_season>=str_to_date('01-JAN-2000','%d-%M-%Y') AND tsl.start_season<=date_add(str_to_date('01-JAN-2000','%d-%M-%Y'), INTERVAL 5 YEAR ));



#question 14, Find all players who played in league 1 but never played in team 1 in league 1 (

SELECT  p.first_name, t.team_id, tsl.league_id,pt.start_date,pt.end_date
from player_team pt join  players p
on (p.player_id = pt.player_id)
join teams t
on (pt.team_id = t.team_id)
join team_season_league tsl
on (t.team_id = tsl.team_id)
join leagues l
on (tsl.league_id = l.league_id) 
where tsl.league_id = 1 
and tsl.team_id <> 1
and (tsl.start_season<=pt.start_date OR pt.start_date<=tsl.end_season OR tsl.start_season<=pt.end_date OR pt.end_date<=tsl.end_season);



#question 15, Find players who played in country India and Turkey

SELECT p.first_name, p.last_name
from  player_team pt join players p
on p.player_id = pt.player_id
where pt.player_id IN(SELECT pt.player_id FROM player_team pt  join players p
on p.player_id = pt.player_id
join teams t
on pt.team_id = t.team_id
join countries c
on c.country_id = t.country_id WHERE c.country_name='India') 
AND p.player_id IN(SELECT pt.player_id FROM player_team pt  join players p
on p.player_id = pt.player_id
join teams t
on pt.team_id = t.team_id
join countries c
on c.country_id = t.country_id WHERE c.country_name='Turkey')



#question 16, Find teams that have been in league L1 but have never been champions in that league 

SELECT t.team_id, t.team_name, tsl.start_season, tsl.end_season,tsl.league_id,ch.champion_id,s.season_year
from team_season_league tsl join champions ch
on ch.league_id=tsl.league_id
join teams t
on t.team_id= tsl.team_id
join seasons s
on s.season_id=ch.season_id
where tsl.league_id=1 and ch.champion_id!=tsl.team_id and ((season_year>=date_format(start_season,'%Y')) and (season_year<=date_format(end_season,'%Y') OR end_season IS NULL ))    
*/
