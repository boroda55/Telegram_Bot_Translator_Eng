create table if not exists Users(
	UserID serial primary key,
	name varchar(150) not null,
	number_user integer not null
);

create table if not exists Words(
	WordID serial primary key,
	Word varchar(40) not null
);


create table if not exists Studied_users(
	UserID integer NOT NULL REFERENCES Users(UserID),
	WordID integer NOT NULL REFERENCES Words(WordID)
);
