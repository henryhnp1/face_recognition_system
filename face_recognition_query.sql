use face_recognition;
insert into permission(name, description)
values
('ACCEPT', 'Cho phép qua cửa'),
('BAN', 'Cấm qua cửa');

insert into role_door(name, description)
values
('PUBLIC', 'Cho phép mọi người qua cửa'),
('RESTRICT', 'Chỉ những người có quyền mời được qua cửa');

insert into building(name, location, number_of_floor, acreage)
values
('A', 'Tòa nhà A, số 218 đường Trần Khát Chân, Hai Bà Trưng, Hà Nội', 29, 4900.0),
('B', 'Tòa nhà A, số 218 đường Trần Khát Chân, Hai Bà Trưng, Hà Nội', 29, 4900.0),
('C', 'Tòa nhà A, số 218 đường Trần Khát Chân, Hai Bà Trưng, Hà Nội', 29, 4900.0);

insert into type_of_floor(name, description)
values
('business', 'Cho phép các công ty, doanh nghiệp đặt cơ sở hoạt động tại đây'),
('resident', 'Sử dụng làm khu chung cư mục đích cư trú');

insert into floor(name, building, type_of_floor, number_of_apartment) values
(1, 1, 1, 20),
(2, 1, 1, 20),
(3, 1, 1, 20),
(4, 1, 1, 40),
(5, 1, 2, 20),
(1, 2, 1, 20),
(2, 2, 1, 20),
(3, 2, 1, 20),
(4, 2, 1, 20),
(5, 2, 2, 40),
(1, 3, 1, 20),
(2, 3, 1, 20),
(3, 3, 1, 20),
(4, 3, 1, 20),
(5, 3, 2, 20);

insert into floor(name, building, type_of_floor, number_of_apartment)
values
(6, 1, 2, 40),
(7, 1, 2, 40),
(8, 1, 2, 40),
(9, 1, 2, 40),
(10, 1, 2, 40),
(11, 1, 2, 40),
(12, 1, 2, 40),
(13, 1, 2, 40),
(14, 1, 2, 40),
(15, 1, 2, 40),
(16, 1, 2, 40),
(17, 1, 2, 40),
(18, 1, 2, 40),
(19, 1, 2, 40),
(20, 1, 2, 40),
(21, 1, 2, 40),
(22, 1, 2, 40),
(23, 1, 2, 40),
(24, 1, 2, 40),
(25, 1, 2, 40),
(26, 1, 2, 40),
(27, 1, 2, 40),
(28, 1, 2, 40),
(29, 1, 2, 30);

insert into floor(name, building, type_of_floor, number_of_apartment)
values
(6, 2, 2, 40),
(7, 2, 2, 40),
(8, 2, 2, 40),
(9, 2, 2, 40),
(10, 2, 2, 40),
(11, 2, 2, 40),
(12, 2, 2, 40),
(13, 2, 2, 40),
(14, 2, 2, 40),
(15, 2, 2, 40),
(16, 2, 2, 40),
(17, 2, 2, 40),
(18, 2, 2, 40),
(19, 2, 2, 40),
(20, 2, 2, 40),
(21, 2, 2, 40),
(22, 2, 2, 40),
(23, 2, 2, 40),
(24, 2, 2, 40),
(25, 2, 2, 40),
(26, 2, 2, 40),
(27, 2, 2, 40),
(28, 2, 2, 40),
(29, 2, 2, 30);

insert into floor(name, building, type_of_floor, number_of_apartment)
values
(6, 3, 2, 40),
(7, 3, 2, 40),
(8, 3, 2, 40),
(9, 3, 2, 40),
(10, 3, 2, 40),
(11, 3, 2, 40),
(12, 3, 2, 40),
(13, 3, 2, 40),
(14, 3, 2, 40),
(15, 3, 2, 40),
(16, 3, 2, 40),
(17, 3, 2, 40),
(18, 3, 2, 40),
(19, 3, 2, 40),
(20, 3, 2, 40),
(21, 3, 2, 40),
(22, 3, 2, 40),
(23, 3, 2, 40),
(24, 3, 2, 40),
(25, 3, 2, 40),
(26, 3, 2, 40),
(27, 3, 2, 40),
(28, 3, 2, 40),
(29, 3, 2, 30);

insert into door(name, floor, role) values
(111, 1, 1),
(112, 1, 1),
(113, 1, 2),
(121, 2, 1),
(122, 2, 2),
(123, 2, 2),
(131, 3, 1),
(132, 3, 2),
(133, 3, 2),
(141, 5, 1),
(142, 5, 2),
(143, 5, 2);

insert into door(name, floor, role) values
(211, 1, 1),
(212, 1, 1),
(213, 1, 2),
(221, 2, 1),
(222, 2, 2),
(223, 2, 2),
(231, 3, 1),
(232, 3, 2),
(233, 3, 2),
(241, 5, 1),
(242, 5, 2),
(243, 5, 2);

insert into door(name, floor, role) values
(311, 1, 1),
(312, 1, 1),
(313, 1, 2),
(321, 2, 1),
(322, 2, 2),
(323, 2, 2),
(331, 3, 1),
(332, 3, 2),
(333, 3, 2),
(341, 5, 1),
(342, 5, 2),
(343, 5, 2);

-- insert into door(name, floor, role) values
-- (1, 11, 1),
-- (2, 11, 4),
-- (3, 11, 2);


/*select query*/
select * from floor;
select * from permission;