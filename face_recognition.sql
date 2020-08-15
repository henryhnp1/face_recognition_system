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

alter table person
add unique(id_card);

alter table person
add phone varchar(10) after gender;

alter table person
add unique (phone);

alter table person
add is_resident int;
create table guest(
	id int primary key auto_increment,
    person int,
    foreign key (person) references person(id)
);
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
    url varchar(1000),
    owner int,
    is_delete int,
    foreign key (owner) references person(id) on delete set null
);

alter table image
add unique (url, owner);
create table person_door_permission(
	id int primary key auto_increment,
    person int,
    door int, 
    permission int,
	foreign key (person) references person(id) on delete cascade,
    foreign key(permission) references permission(id) on delete cascade,
    foreign key(door) references door(id) on delete cascade
);
alter table person_door_permission
add unique (person, door, permission);
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
create table role(
	id int primary key auto_increment,
    name varchar(10) unique
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

drop procedure if exists insert_door_from_file;
delimiter #
create procedure insert_door_from_file(in floor_id int, in door_id int, in role_name nvarchar(50))
begin
	declare role_id int;
	select r.id into role_id from role_door as r where r.name = role_name limit 1;
    insert into door(name, floor, role) value (door_id, floor_id, role_id);
end#
delimiter ;

-- call insert_door_from_file(1, 1, 'PUBLIC');


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

-- call insert_office_from_file('B', 1, 'B1012','Not Available');

drop procedure if exists insert_company;
delimiter #
create procedure insert_company(in name_in nvarchar(255),in phone_in nvarchar(10),in office_in int)
begin
	update apartment set status = 1 where id = office_in;
    insert into company(name, phone, apartment) value (name_in, phone_in, office_in);
end#
delimiter ;

-- call insert_company('Test1', '0964092612', 5);

drop procedure if exists update_company;
delimiter #
create procedure update_company(in id_in int, in name_in nvarchar(255),in phone_in nvarchar(10),in office_in_cur int, in office_in_new int)
begin
    update apartment set status = 0 where id = office_in_cur;
	update apartment set status = 1 where id = office_in_new;
    update company set name = name_in, phone = phone_in, apartment = office_in_new where id = id_in;
end#
delimiter ;

-- call update_company(10,'Test1', '0964092613', 5, 10);

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

-- call insert_company_from_file('B', '1', 'B1003', 'Test5', '0965892179');

drop procedure if exists insert_apartment_from_file;
delimiter #
create procedure insert_apartment_from_file(in building_name nvarchar(50),in floor_name int ,in apartment_name nvarchar(50), in status_in nvarchar(50))
begin
	declare building_id int;
    declare floor_id int;
    declare status_int int;
    set status_int = if (status_in = 'Available', 0, 1);
    select b.id into building_id from building as b where b.name = building_name limit 1;
    select f.id into floor_id from building as b join floor as f on f.building = b.id where b.id = building_id and f.name = floor_name limit 1;
    insert into apartment(name, floor, status) value (apartment_name, floor_id, status_int);
end#
delimiter ;

-- call insert_apartment_from_file('A', '5', 'A5001', 'Available');



-- call insert_staff(2, 'Trần Đức Long', '1978-06-10', 1, '0986256817', '162780124', 'Nguyễn Trãi, Thanh Xuân, Hà Nội', 'Đốc Ngữ, Ba Đình, Hà Nội');

drop procedure if exists edit_staff;
delimiter #
create procedure edit_staff(in company_in int,in name_in nvarchar(255), in birthday_in date, in gender_in int, in phone_in varchar(10), in id_card_in varchar(12), in village_in nvarchar(255), in current_accommodation_in text, in cur_id_card varchar(12), in cur_company int)
begin
	declare person_id int;
    declare person_id_number nvarchar(12);
    select p.id_card into person_id_number from person as p where p.id_card = cur_id_card;
	update person set name = name_in, birthday= birthday_in, id_card = id_card_in, gender=gender_in, phone = phone_in, 
	village = village_in, current_accommodation=current_accommodation_in where id_card = cur_id_card;
	select p.id into person_id from person as p where p.id_card = id_card_in limit 1;
	update company_staff set company = company_in where staff = person_id and company = cur_company;

end#
delimiter ;
-- call edit_staff(3, 'Trần Đức Long', '1978-06-10', 1, '0986256817', '162780125', 'Nguyễn Trãi, Thanh Xuân, Hà Nội', 'Đốc Ngữ, Ba Đình, Hà Nội','162780124',2);
drop procedure if exists insert_staff;
delimiter #
create procedure insert_staff(in company_in int,in name_in nvarchar(255),in name_en_in varchar(50),in birthday_in date, in gender_in int, in phone_in varchar(10), in id_card_in varchar(12), in village_in nvarchar(255), in current_accommodation_in text)
begin
	declare person_id int;
    declare person_id_number nvarchar(12);
    declare company_id int;
    declare staff_id int;
    select p.id_card into person_id_number from person as p where p.id_card = id_card_in;
    if person_id_number is null then
		begin
			insert into person(name,name_en,birthday, id_card, gender, phone, village, current_accommodation, is_delete, is_resident)
			value (name_in,name_en_in ,birthday_in, id_card_in, gender_in, phone_in, village_in, current_accommodation_in, 0, 1);
			select p.id into person_id from person as p where p.id_card = id_card_in limit 1;
			insert into company_staff(company, staff) value (company_in, person_id);
		end;
	else
		begin
			select p.id into person_id from person as p where p.id_card = id_card_in limit 1;
            select s.company into company_id from company_staff as s where s.company = company_in and s.staff = person_id;
            select s.staff into staff_id from company_staff as s where s.company = company_in and s.staff = person_id;
            if company_id is null and staff_id is null then
				begin
					insert into company_staff(company, staff) value (company_in, person_id);
				end;
			end if;
        end;
	end if;
end#
delimiter ;

drop procedure if exists insert_staff_from_file;
delimiter #
create procedure insert_staff_from_file(in company_name nvarchar(255), in office_name nvarchar(50), in name_in nvarchar(255), in name_en_in varchar(50), in birthday_in date, in gender_in varchar(10),in phone_in varchar(10), in id_card_in varchar(12),in village_in nvarchar(255), in cur_accom text)
begin
	declare company_id int;
    declare office_id int;
    declare gender_new int;
    set gender_new = if(gender_in ='Male', 1, 0);
    select a.id into office_id from apartment as a where a.name = office_name limit 1;
    select c.id into company_id from company as c where c.name = company_name and c.apartment = office_id limit 1;
    call insert_staff(company_id, name_in, name_en_in, birthday_in, gender_new, phone_in, id_card_in, village_in, cur_accom);
end#
delimiter ;

call insert_staff_from_file('CTY ABC','A1001', 'Hoàng Mai Nghị', 'NghiHM0624_618_07_06','1996-06-24', 'Male', '163355618', '0964092612', 'Việt Hùng, Trực Ninh, Nam Định', 'Minh Khai, Bắc Từ Liêm, Hà Nội');

drop procedure if exists insert_resident;
delimiter #
create procedure insert_resident(in apartment_in int,in name_in nvarchar(255),in name_en_in varchar(50),in birthday_in date, in gender_in int, in phone_in varchar(10), in id_card_in varchar(12), in village_in nvarchar(255), in current_accommodation_in text)
begin
	declare person_id int;
    declare person_id_number nvarchar(12);
    declare apartment_id int;
    declare resident_id int;
    select p.id_card into person_id_number from person as p where p.id_card = id_card_in;
    if person_id_number is null then
		begin
			insert into person(name,name_en,birthday, id_card, gender, phone, village, current_accommodation, is_delete, is_resident)
			value (name_in,name_en_in ,birthday_in, id_card_in, gender_in, phone_in, village_in, current_accommodation_in, 0, 1);
			select p.id into person_id from person as p where p.id_card = id_card_in limit 1;
			insert into resident_apartment(resident, apartment) value (person_id, apartment_in);
		end;
	else
		begin
			select p.id into person_id from person as p where p.id_card = id_card_in limit 1;
            select r.apartment into apartment_id from resident_apartment as r where r.apartment = apartment_in and r.resident = person_id;
            select r.resident into resident_id from resident_apartment as r where r.resident = person_id and r.apartment = apartment;
            if company_id is null and staff_id is null then
				begin
					insert into resident_apartment(resident, apartment) value (person_id, apartment_in);
				end;
			end if;
        end;
	end if;
end#
delimiter ;

drop procedure if exists edit_resident;
delimiter #
create procedure edit_resident(in apartment_in int,in name_in nvarchar(255), in birthday_in date, in gender_in int, in phone_in varchar(10), in id_card_in varchar(12), in village_in nvarchar(255), in current_accommodation_in text, in cur_id_card varchar(12), in cur_apartment int)
begin
	declare person_id int;
	update person set name = name_in, birthday= birthday_in, id_card = id_card_in, gender=gender_in, phone = phone_in, 
	village = village_in, current_accommodation=current_accommodation_in where id_card = cur_id_card;
	select p.id into person_id from person as p where p.id_card = id_card_in limit 1;
	update resident_apartment set apartment = apartment_in where resident = person_id and apartment = cur_apartment;

end#
delimiter ;
call edit_resident(85,'Lê Thị Ánh', '2000-07-20', 0, '0974926411', '163355624', 'Kim Sơn, Ninh Bình', 'Thanh Xuân, Hà Nội', 'Female', 85);
drop procedure if exists insert_resident_from_file;
delimiter #
create procedure insert_resident_from_file(in apartment_name nvarchar(50), in name_in nvarchar(255), in name_en_in varchar(50), in birthday_in date, in gender_in varchar(10),in phone_in varchar(10), in id_card_in varchar(12),in village_in nvarchar(255), in cur_accom text)
begin
	declare apartment_id int;
    declare gender_new int;
    set gender_new = if(gender_in ='Male', 1, 0);
    select a.id into apartment_id from apartment as a where a.name = apartment_name limit 1;
    call insert_resident(apartment_id, name_in, name_en_in, birthday_in, gender_new, phone_in, id_card_in, village_in, cur_accom);
end#
delimiter ;

drop procedure if exists insert_grant_role_from_file;
delimiter #
create procedure insert_grant_role_from_file(in building_in nvarchar(50), in floor_in int, in door_in int, in id_card_in varchar(12), in permission_in nvarchar(50))
begin
	declare person_id int;
    declare door_id int;
    declare permission_id int;
    
    select d.id into door_id from door as d 
    join floor as f on f.id = d.floor 
    join building as b on b.id = f.building 
    where d.name = door_in and f.name = floor_in and b.name = building_in limit 1;
    
    select p.id into person_id from person as p where p.id_card = id_card_in limit 1;
    select p.id into permission_id from permission as p where p.name = permission_in limit 1;
    
    insert into person_door_permission(person, door, permission) value (person_id, door_id, permission_id);
end#
delimiter ;

call insert_grant_role_from_file('A', 3, 132, '163355618', 'ACCEPT');

select p.id from person as p where p.id_card = '163355618' limit 1;