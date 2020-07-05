create database face_recognition default character set utf8 default collate utf8_unicode_520_ci;
use face_recognition;
create table building(
	id int primary key auto_increment,
    name nvarchar(50) not null unique,
    location nvarchar(1000),
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
    foreign key (type_of_floor) references type_of_floor(id) on delete cascade,
    unique(name, building)
);

create table role_door(
	id int primary key auto_increment,
    name nvarchar(50) not null unique,
    description nvarchar(2000)
);

create table door(
	id int primary key auto_increment,
    name int,
    floor int,
    role int,
    foreign key (floor) references floor(id) on delete cascade,
    foreign key (role) references role_door(id) on delete cascade,
    unique(name, floor)
);

create table permission(
	id int primary key auto_increment,
    name nvarchar(50) not null unique,
    description nvarchar(2000)
);
/*-------------------------------------------------------------------------------*/
create table guest(
	id int primary key auto_increment,
    person int,
    foreign key (person) references person(id)
);
create table person(
	id int primary key auto_increment,
    name nvarchar(255) not null,
    birthday date,
    id_card varchar(12) not null,
    gender int,
    village nvarchar(255),
    current_accommodation text,
    is_delete int
);

alter table person
add name_en varchar(50) unique after name;
create table apartment(
	id int primary key auto_increment,
    name nvarchar(50) not null,
    floor int,
    foreign key (floor) references floor(id) on delete cascade
);
alter table apartment
add status int;

alter table apartment
add unique(name, floor);

create table resident_apartment(
	id int primary key auto_increment,
    resident int,
    apartment int,
    foreign key(resident) references person(id) on delete cascade,
    foreign key (apartment) references apartment(id) on delete cascade
);

/*
create table door_permission(
	id int primary key auto_increment,
    door int,
    permission int,
    foreign key (door) references door(id) on delete cascade,
    foreign key (permission) references permission(id) on delete cascade
);
*/
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
    apartment int,
    time_in datetime,
    time_out datetime,
    reason text,
    foreign key (guest) references person(id) on delete cascade,
    foreign key(apartment) references person(id) on delete cascade
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
    password nvarchar(255) not null,
    role int,
    foreign key (role) references role(id)
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
    phone varchar(10),
    apartment int,
    foreign key (apartment) references apartment(id)
);
alter table company
add unique(name, apartment);
create table company_staff(
	id int primary key auto_increment,
    company int,
    staff int,
    foreign key (company) references company(id),
    foreign key (staff) references person(id)
);

create table role(
	id int primary key auto_increment,
    name varchar(10) unique
);
drop procedure if exists insert_door_from_file;
delimiter #
create procedure insert_door_from_file(in floor_id int, in door_id int, in role_name nvarchar(50))
begin
	declare role_id int;
	select r.id into role_id from role_door as r where r.name = role_name limit 1;
    insert into door(name, floor, role) value (door_id, floor_id, role_id);
end#
delimiter ;

call insert_door_from_file(1, 1, 'PUBLIC');


drop procedure if exists insert_office_from_file;
delimiter #
create procedure insert_office_from_file(in building_name nvarchar(50),  floor_name int, in name_in nvarchar(50), in status_in nvarchar(50))
begin
	declare building_id int;
    declare floor_id int;
    declare status_int int;
    set status_int = if (status_in = 'Available', 0, 1);
    select b.id into building_id from building as b where b.name = building_name limit 1;
    select f.id into floor_id from building as b join floor as f on f.building = b.id where b.id = building_id and f.name = floor_name limit 1;
    insert into apartment(name, floor, status) value (name_in, floor_id, status_int);
end#
delimiter ;

call insert_office_from_file('B', 1, 'B1012','Not Available');

drop procedure if exists insert_company;
delimiter #
create procedure insert_company(in name_in nvarchar(255),in phone_in nvarchar(10),in office_in int)
begin
	update apartment set status = 1 where id = office_in;
    insert into company(name, phone, apartment) value (name_in, phone_in, office_in);
end#
delimiter ;

call insert_company('Test1', '0964092612', 5);

drop procedure if exists update_company;
delimiter #
create procedure update_company(in id_in int, in name_in nvarchar(255),in phone_in nvarchar(10),in office_in_cur int, in office_in_new int)
begin
    update apartment set status = 0 where id = office_in_cur;
	update apartment set status = 1 where id = office_in_new;
    update company set name = name_in, phone = phone_in, apartment = office_in_new where id = id_in;
end#
delimiter ;

call update_company(10,'Test1', '0964092613', 5, 10);

drop procedure if exists insert_company_from_file;
delimiter #
create procedure insert_company_from_file(in building_name nvarchar(50),in floor_name int ,in office_name nvarchar(50), in name_company nvarchar(255),in phone_in nvarchar(10))
begin
	declare building_id int;
    declare floor_id int;
    declare office_id int;
    select id into building_id from building where name = building_name limit 1;
    select f.id into floor_id from floor as f join building as b on f.building = b.id where f.name = floor_name and b.id = building_id limit 1;
    select a.id into office_id from apartment as a join floor as f on a.floor = f.id where f.id = floor_id and a.name = office_name limit 1;
    call insert_company(name_company, phone_in, office_id);
end#
delimiter ;

call insert_company_from_file('B', '1', 'B1003', 'Test5', '0965892179');