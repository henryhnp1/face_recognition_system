use face_recognition;
insert into permission(name, description)
values
('ACCEPT', 'Cho phép qua cửa'),
('BAN', 'Cấm qua cửa'),
('PUBLIC', 'Cho phép tất cả mọi người qua cửa'),
('RESTRICT', 'Chỉ cho phép các cá nhân nhất định qua cửa');

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
(5, 2, 2, 40);
