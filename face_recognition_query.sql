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

insert into door(name, floor, role) values
(1, 1, 1);
-- (2, 11, 4),
-- (3, 11, 2);
insert into role_door(name,description) value
('ads', 'ads');

insert into user(username, password, role) values 
('admin', '25d55ad283aa400af464c76d713c07ad', 1), 
('henry', '25d55ad283aa400af464c76d713c07ad', 2);

insert into role(name) values
('ROOT'), ('MEMBER');

insert into apartment(name, floor) values
('A1001', 1),
('A1002', 1),
('A1003', 1),
('A1004', 1),
('A1005', 1),
('A2001', 2),
('A2002', 2),
('A2003', 2),
('A2004', 2),
('A2005', 2),
('A3001', 3),
('A3002', 3),
('A3003', 3),
('A3004', 3),
('A3005', 3),
('A6001', 16),
('A6002', 16),
('A6003', 16),
('A6004', 16),
('A6005', 16),
('A7001', 17),
('A7002', 17),
('A7003', 17),
('A7004', 17),
('A7005', 17),
('A8001', 18),
('A8002', 18),
('A8003', 18),
('A8004', 18),
('A8005', 18);

insert into apartment(name, floor) values
('B1001', 6),
('B1002', 6),
('B1003', 6),
('B1004', 6),
('B1005', 6),
('B2001', 1),
('B2002', 7),
('B2003', 7),
('B2004', 7),
('B2005', 7),
('B3001', 8),
('B3002', 8),
('B3003', 8),
('B3004', 8),
('B3005', 8),
('B6001', 40),
('B6002', 40),
('B6003', 40),
('B6004', 40),
('B6005', 40),
('B7001', 41),
('B7002', 41),
('B7003', 41),
('B7004', 41),
('B7005', 41),
('B8001', 42),
('B8002', 42),
('B8003', 42),
('B8004', 42),
('B8005', 42);

insert into apartment(name, floor) values
('C1001', 11),
('C1002', 11),
('C1003', 11),
('C1004', 11),
('C1005', 11),
('C2001', 12),
('C2002', 12),
('C2003', 12),
('C2004', 12),
('C2005', 12),
('C3001', 13),
('C3002', 13),
('C3003', 13),
('C3004', 13),
('C3005', 13),
('C6001', 61),
('C6002', 61),
('C6003', 61),
('C6004', 61),
('C6005', 61),
('C7001', 61),
('C7002', 62),
('C7003', 62),
('C7004', 62),
('C7005', 62),
('C8001', 63),
('C8002', 63),
('C8003', 63),
('C8004', 63),
('C8005', 63);

update apartment
set status = 0;

insert into company(name, phone, apartment) values
('CTY ABC', '0244092612', 1),
('CTY ABA', '0244092613', 6),
('CTY ABB', '0244092614', 11),
('CTY BAA', '0245092612', 31),
('CTY BAB', '0245092613', 36),
('CTY BAC', '0245092614', 41),
('CTY CAA', '0246092612', 121),
('CTY CAB', '0246092613', 126),
('CTY CAC', '0246092614', 131);

insert into person(name, name_en, birthday, id_card, gender, village, current_accommodation, is_delete) values
('Hoàng Mai Nghị', 'NghiHM2406_618_29_06_20','1996-06-24', '163355618',1, 'Việt Hùng, Trực Ninh, Nam Định', 'Minh Khai, Bắc Từ Liêm, Hà Nội', 0);
insert into person(name, name_en, birthday, id_card, gender, village, current_accommodation, is_delete) values
('Lê Thị Hồng Ngân', 'NganLH2509_619_29_06_20','1997-09-25', '163355619',0, 'Văn Miếu, Thanh Sơn, Phú Thọ', 'Hồ Tùng Mậu, Cầu Giấy, Hà Nội', 0),
('Trần Văn Vụ', 'VuTV1004_620_29_06_20','2000-04-10', '163355620',1, 'Trực Bình, Trực Ninh, Nam Định', 'Hồ Tùng Mậu, Cầu Giấy, Hà Nội', 0),
('Phạm Vũ Mạnh', 'ManhVP0207_621_29_06_20','1997-07-02', '163355621',1, 'Kim Bảng, Hà Nam', 'Trần Cung, Cầu Giấy, Hà Nội', 0),
('Bui Đức Sinh', 'SinhDB2210_622_29_06_20','2001-10-22', '163355622',1, 'Nam Sách, Hải Dương', 'Minh Khai, Bắc Từ Liêm, Hà Nội', 0),
('Bui Văn Trúc', 'TrucDB0208_623_29_06_20','1994-08-02', '163355623',1, 'Nam Sách, Hải Dương', 'Minh Khai, Bắc Từ Liêm, Hà Nội', 0),
('Lê Thị Ánh', 'AnhLT2007_624_29_06_20','2000-07-20', '163355624',0, 'Kim Sơn, Ninh Bình', 'Thanh Xuân, Hà Nội', 0);

insert into company_staff(company, staff) values
(10, 1), 
(10, 2),
(12, 3),
(14, 4);

insert into resident_apartment(resident, apartment) values
(1, 22),
(2, 22),
(1, 56),
(7, 146),
(4, 147);

insert into guest(person) values
(5), (6);
insert into person_door_permission(person, door, permission) values
(1, 1, 1),
(2, 1, 1),
(3, 1, 1),
(4, 1, 1),
(5, 1, 1),
(6, 1, 1),
(7, 1, 1),
(2, 1, 1),
(1, 2, 1),
(2, 2, 1),
(5, 2, 2),
(6, 2, 2);
insert into image(url, owner, is_delete)
values
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/2.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/3.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/4.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/5.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/6.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/7.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/8.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/9.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/10.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/11.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/12.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/13.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/14.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/15.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/16.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/17.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/18.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/19.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/20.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/21.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/22.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/23.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/24.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/25.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/26.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/27.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/28.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/29.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/30.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/31.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/32.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/33.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/34.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/35.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/36.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/37.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/38.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/39.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/40.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/41.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/42.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/43.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/44.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/45.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/46.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/47.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/48.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/49.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/50.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/51.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/52.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/53.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/54.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/55.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/56.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/57.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/58.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/59.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/60.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/61.jpg', 1, 0),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/62.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/63.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/64.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/65.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/66.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/67.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/68.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/69.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/70.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/71.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/72.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/73.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/74.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/75.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/76.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/77.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/78.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/79.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/80.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/81.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/82.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/83.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/84.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/85.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/86.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/87.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/88.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/89.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/90.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/91.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/92.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/93.jpg', 1, 1),
('/home/henry/FinalProject/face_recognition_system/core/data/dataset/raw/NghiHm2406_618_29_06_20/94.jpg', 1, 1);
insert into apartment(name, floor, status) value
('A1001', 1, 0);

insert into out_in_of_guest(guest, visit_to, apartment, time_in, time_out) values
(1, 1, 1, '2020-07-10 10:00:19', '2020-07-10 10:20:45'),
(1, 1, 1, '2020-07-15 09:45:50', '2020-07-15 10:30:03'),
(1, 1, 1, '2020-07-21 09:55:01', '2020-07-21 10:35:52'),
(1, 1, 1, '2020-07-27 08:25:50', '2020-07-27 18:10:03'),
(2, 1, 16, '2020-06-05 09:25:50', '2020-06-05 10:10:03');

insert into out_in_of_guest(guest, visit_to, apartment, time_in, time_out) values
(1, 1, 6, '2020-07-10 10:00:19', '2020-07-10 10:20:45');


delete from apartment where apartment.id > 90;
/*select query*/
use face_recognition;
select * from floor;
select * from permission;

select a.id, b.name, f.name, a.name, t.name  from apartment as a, floor as f, building as b, type_of_floor as t where a.floor = f.id and f.building = b.id and f.type_of_floor = t.id ;
select f.name as 'floor' , f.id, b.name as 'building' from floor as f, building as b where f.building = b.id and b.name = 'C';
select d.id, b.name as 'building', f.name as 'floor' , d.name as 'door', r.name as 'role' from door as d 
join floor as f on d.floor = f.id 
join building as b on f.building = b.id
join role_door as r on d.role = r.id;

select f.id, b.name as 'building', f.name as 'floor', t.name as 'type_of_floor', f.number_of_apartment as 'number_of_apartment' from floor as f
join building as b on f.building = b.id
join type_of_floor as t on f.type_of_floor = t.id;

select * from door as r where r.id like '%1%';

select a.id, a.name, if(a.status =0, 'Available', 'Not Available') as 'status', f.name as 'floor', b.name as 'building' from apartment as a join floor as f on a.floor = f.id
join building as b on b.id = f.building
join type_of_floor as t on t.id = f.type_of_floor
where t.name = 'business';

select c.id, b.name as 'building', f.name as 'floor', a.name as 'apartment' ,c.name, c.phone from company as c
join apartment as a on c.apartment = a.id
join floor as f on a.floor = f.id
join building as b on f.building = b.id;

select a.id, a.name, a.floor, a.status from apartment as a join floor as f on a.floor = f.id where a.floor = 1;

SHOW INDEX FROM company;
alter table company
drop index `name`;

select a.id, b.name, f.name, a.name, a.status from apartment as a 
join floor as f on f.id = a.floor
join building as b on b.id = f.building
join type_of_floor as t on f.type_of_floor = t.id
where t.id = 2;

select s.id, c.name as 'company', a.name as 'office', p.name, p.birthday, if(p.gender=1,'Male', 'Female') as 'gender' , p.id_card, p.phone, p.village, p.current_accommodation from company_staff as s
join person as p on s.staff = p.id
join company as c on s.company = c.id
join apartment as a on a.id = c.apartment
where p.is_delete = 0;

select c.id, c.name, c.phone, c.apartment, a.name as 'office'from company as c
join apartment as a on c.apartment = a.id
join floor as f on a.floor = f.id
join building as b on b.id = f.building
join type_of_floor as t on t.id = f.type_of_floor
where t.name = 'business' and b.id = 1 and f.id = 1;

select c.id, c.name, a.id as 'office_id', a.name as 'office', f.id as 'floor_id', 
f.name as 'floor', b.id as 'building_id', b.name as 'building' from company as c
join apartment as a on c.apartment = a.id
join floor as f on a.floor = f.id
join building as b on b.id = f.building
join type_of_floor as t on t.id = f.type_of_floor
where t.name = 'business' and c.name = 'CTY BAA' and a.name = 'B1001';

select p.id, a.name as 'apartment', p.name, p.birthday, p.gender, p.id_card, p.phone, p.village, p.current_accommodation  from person as p
join resident_apartment as r on p.id = r.resident
join apartment as a on a.id = r.apartment
join floor as f on a.floor = f.id
join building as b on b.id = f.building
join type_of_floor as t on t.id = 2
where p.is_delete = 0 and p.is_resident = 1;

select a.id as 'apartment_id', a.name as 'apartment', f.id as 'floor_id', 
f.name as 'floor', b.id as 'building_id', b.name as 'building' from apartment as a
join floor as f on a.floor = f.id
join building as b on b.id = f.building
join type_of_floor as t on t.id = f.type_of_floor
where t.id = 2 and a.name = 'A6001';

select p.id, a.name as 'apartment', p.name, p.birthday, 
if(p.gender=1, 'Male', 'Female') as 'gender', p.id_card, 
p.phone, p.village, p.current_accommodation  from person as p
join resident_apartment as r on p.id = r.resident
join apartment as a on a.id = r.apartment
join floor as f on a.floor = f.id
join building as b on b.id = f.building
join type_of_floor as t on t.id = 2
where p.is_delete = 0 and p.is_resident = 1 and r.id = 1;

-- select company office
select c.id, c.name, a.id as 'office_id', a.name as 'office', f.id as 'floor_id', 
        f.name as 'floor', b.id as 'building_id', b.name as 'building' from company as c
        join apartment as a on c.apartment = a.id
        join floor as f on a.floor = f.id
        join building as b on b.id = f.building
        join type_of_floor as t on t.id = f.type_of_floor
        where t.id = 1 and c.name = 'CTY ABC' and a.name = 'A1001';

select p.id, a.name as 'apartment', a.id as 'apartment_id', p.name, p.birthday, 
                    if(p.gender=1, 'Male', 'Female') as 'gender', p.id_card, 
                    p.phone, p.village, p.current_accommodation  from person as p
                    join resident_apartment as r on p.id = r.resident
                    join apartment as a on a.id = r.apartment
                    join floor as f on a.floor = f.id
                    join building as b on b.id = f.building
                    join type_of_floor as t on t.id = 2
                    where p.is_delete = 0 and p.is_resident = 1 and p.id =7;
select pdp.id, b.name as 'building', f.name as 'floor', d.name as 'door', p.name as 'person',  p.id_card, p.phone, p.current_accommodation, pm.name as 'permission' from person_door_permission as pdp 
join person as p on pdp.person = p.id
join door as d on pdp.door = d.id
join floor as f on d.floor = f.id
join building as b on f.building = b.id
join permission as pm on pdp.permission = pm.id
join role_door as rd on d.role = rd.id
where rd.id = 2;

-- select door with building and floor
select d.id, d.floor, d.name, d.role from door as d
join floor as f on d.floor = f.id
join building as b on b.id = f.building
join role_door as r on d.role = r.id
where r.id = 2;

-- select permission with door

select r.id, r.name, r.description from role_door as r
join door as d on r.id = d.role
join person_door_permission 
where d.id = 5;

select a.id, b.name as 'building', f.name as 'floor', a.name, if(a.status =0, 'Available', 'Not Available') as 'status' from apartment as a 
    join floor as f on a.floor = f.id
    join building as b on b.id = f.building
    join type_of_floor as t on t.id = f.type_of_floor
    where t.name = 'bussiness';

select d.id, d.name, d.floor, d.role from door as d
            join floor as f on d.floor = f.id
            join building as b on b.id = f.building
            join role_door as r on d.role = r.id
            where r.id = 2 and b.id = 1;

select oiog.id, p.name, p.birthday, if(p.gender=1, 'Male', 'Female') as 'gender', p.id_card, p.phone, p.village, p.current_accommodation, a.name as 'apartment', oiog.time_in, oiog.time_out, oiog.visit_to from guest as g 
join person as p on p.id = g.person
join out_in_of_guest as oiog on oiog.guest = g.id
join apartment as a on a.id = oiog.apartment;

select a.id as 'apartment_id', a.name as 'apartment', f.id as 'floor_id', 
        f.name as 'floor', b.id as 'building_id', b.name as 'building' from apartment as a
        join floor as f on a.floor = f.id
        join building as b on b.id = f.building
        join type_of_floor as t on t.id = f.type_of_floor
        where t.id = 1 and a.name = 'A1001' limit 1;

select c.name from company as c join apartment as a
where c.apartment = a.id and a.name = 'A1001';

select p from person as p join guest as g on p.id = g.person
join out_in_of_guest as oiog on oiog.guest = g.id
where p.id = 6 order by time_in desc limit 1;

select p.id_card from person as p join guest as g on p.id = g.person
join out_in_of_guest as oiog on oiog.guest = g.id
where oiog.id = 2 limit 1;