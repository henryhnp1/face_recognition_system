create database face_recognition default character set utf8 default collate utf8_unicode_520_ci;
use face_recognition;
create table building(
	id int primary key auto_increment,
    name nvarchar(50) not null,
    location nvarchar(255),
    number_of_floor int,
    acreage float
);
create table type_of_floor(
	id int primary key auto_increment,
    name nvarchar(50) not null unique,
    description nvarchar(2000)
);
create table floor(
	id int primary key auto_increment,
    name int not null,
    building int,
    type_of_floor int,
    number_of_apartment int,
    foreign key (building) references building(id) on delete cascade,
    foreign key (type_of_floor) references type_of_floor(id) on delete cascade
);
create table type_of_person(
	id int primary key auto_increment,
    name nvarchar(50) not null unique,
    description nvarchar(2000)
);
create table person(
	id int primary key auto_increment,
    name nvarchar(255) not null,
    birthday date,
    id_card varchar(12) not null,
    gender int,
    email nvarchar(255) unique,
    village nvarchar(255),
    current_accommodation text,
    type_of_person int,
    is_delete int,
    foreign key (type_of_person) references type_of_person(id) on delete cascade
);
create table apartment(
	id int primary key auto_increment,
    name nvarchar(50) not null,
    floor int,
    owner int,
    foreign key (floor) references floor(id) on delete cascade,
    foreign key (owner) references person(id) on delete cascade
);
create table apartment_resident(
	id int primary key auto_increment,
    resident int,
    apartment int,
    foreign key(resident) references person(id) on delete cascade,
    foreign key (apartment) references apartment(id) on delete cascade
);
create table permission(
	id int primary key auto_increment,
    name nvarchar(50) not null unique,
    description nvarchar(2000)
);
create table door(
	id int primary key auto_increment,
    name nvarchar(50),
    floor int,
    foreign key (floor) references floor(id) on delete cascade
);
create table door_permission(
	id int primary key auto_increment,
    door int,
    permission int,
    foreign key (door) references door(id) on delete cascade,
    foreign key (permission) references permission(id) on delete cascade
);
create table image(
	id int primary key auto_increment,
    url text not null,
    owner int,
    is_delete int,
    foreign key (owner) references person(id) on delete set null
);
create table person_door_permission(
	id int primary key auto_increment,
    person int,
    door int, 
    permission int,
	foreign key (person) references person(id) on delete cascade,
    foreign key(permission) references permission(id) on delete cascade,
    foreign key(door) references door(id) on delete cascade
);
create table out_in_of_guest(
	id int primary key auto_increment,
    guest int,
    resident int,
    time_in datetime,
    time_out datetime,
    reason text,
    foreign key (guest) references person(id) on delete cascade,
    foreign key(resident) references person(id) on delete cascade
);
create table history_out_int(
	id int primary key auto_increment,
    person int,
    time datetime,
    door int,
    permission int,
    foreign key (person) references person(id) on delete cascade,
    foreign key(door) references door(id) on delete cascade,
    foreign key (permission) references permission(id)
);
create table warning(
	id int primary key auto_increment,
    history_out_int int,
    foreign key (history_out_int) references history_out_int(id) on delete cascade
);
create table role_sys(
	id int primary key auto_increment,
    name nvarchar(255),
    view_role int,
    add_role int,
    update_role int,
    delete_role int
);
create table user(
	id int primary key auto_increment,
    username nvarchar(250) not null,
    password nvarchar(255) not null
);
create table user_role_sys(
	id int primary key auto_increment,
    user int,
    role_sys int,
    foreign key (user) references user(id) on delete cascade,
    foreign key (role_sys) references role_sys(id) on delete cascade
);
create table company(
	id int primary key auto_increment,
    name nvarchar(255),
    apartment int,
    foreign key (apartment) references apartment(id)
);
