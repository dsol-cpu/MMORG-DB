CREATE TABLE player 
	(player_ID	varchar(8),
	 username 	varchar(20),
	 primary key (player_ID)
	);

CREATE TABLE ability
	(ability_name varchar(20),
	 effect varchar(100),
	 primary key (ability_name)
	);

CREATE TABLE race
	(race_name varchar(12),
	base_ATK numeric(99,1),
	base_DEF numeric(99,1),
	base_STR numeric(99,1),
	base_DEX numeric(99,1),
	base_MAG numeric(99,1),
	base_CHA numeric(99,1),
	base_SPD numeric(99,1),
	base_LCK numeric(99,1),
	ability_name varchar(20),
	primary key (race_name),
	foreign key (ability_name) references ability on delete set null
	);	

CREATE TABLE class
	(class_name varchar(15),
	ability_name varchar(20),
	primary key (class_name),
	foreign key (ability_name) references ability on delete set null
	);

CREATE TABLE region
	(region_name varchar(20),
	 spawn_x numeric(4,0),
	 spawn_y numeric (4,0),
	 primary key (region_name)
	);

CREATE TABLE __character
	(num_char numeric(1,0) check (num_char <= 4),
	 player_ID varchar(8),
	 name varchar (20),
	 __level numeric(3,0) CHECK (__level >= 1),
	 race_name varchar(12),
	 class_name varchar(15),
	 region_name varchar(20),
	 primary key (num_char, player_ID),
	 foreign key (race_name) references race on delete cascade,
	 foreign key (class_name) references class on delete cascade,
	 foreign key (region_name) references region on delete set null,
	 foreign key (player_ID) references player on delete cascade
	);
