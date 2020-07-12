CREATE DATABASE  IF NOT EXISTS `face_recognition` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_520_ci */;
USE `face_recognition`;
-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: face_recognition
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping events for database 'face_recognition'
--

--
-- Dumping routines for database 'face_recognition'
--
/*!50003 DROP PROCEDURE IF EXISTS `edit_resident` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `edit_resident`(in apartment_in int,in name_in nvarchar(255), in birthday_in date, in gender_in int, in phone_in varchar(10), in id_card_in varchar(12), in village_in nvarchar(255), in current_accommodation_in text, in cur_id_card varchar(12), in cur_apartment int)
begin
	declare person_id int;
    declare person_id_number nvarchar(12);
    select p.id_card into person_id_number from person as p where p.id_card = id_card_in;
	update person set name = name_in, birthday= birthday_in, id_card = id_card_in, gender=gender_in, phone = phone_in, 
	village = village_in, current_accommodation=current_accommodation_in where id_card = cur_id_card;
	select p.id into person_id from person as p where p.id_card = id_card_in limit 1;
	update resident_apartment set apartment = apartment_in where resident = person_id and apartment = cur_apartment;

end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `edit_staff` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `edit_staff`(in company_in int,in name_in nvarchar(255), in birthday_in date, in gender_in int, in phone_in varchar(10), in id_card_in varchar(12), in village_in nvarchar(255), in current_accommodation_in text, in cur_id_card varchar(12), in cur_company int)
begin
	declare person_id int;
    declare person_id_number nvarchar(12);
    select p.id_card into person_id_number from person as p where p.id_card = id_card_in;
	update person set name = name_in, birthday= birthday_in, id_card = id_card_in, gender=gender_in, phone = phone_in, 
	village = village_in, current_accommodation=current_accommodation_in where id_card = cur_id_card;
	select p.id into person_id from person as p where p.id_card = id_card_in limit 1;
	update company_staff set company = company_in where staff = person_id and company = cur_company;

end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_apartment_from_file` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `insert_apartment_from_file`(in building_name nvarchar(50),in floor_name int ,in apartment_name nvarchar(50), in status_in nvarchar(50))
begin
	declare building_id int;
    declare floor_id int;
    declare status_int int;
    set status_int = if (status_in = 'Available', 0, 1);
    select b.id into building_id from building as b where b.name = building_name limit 1;
    select f.id into floor_id from building as b join floor as f on f.building = b.id where b.id = building_id and f.name = floor_name limit 1;
    insert into apartment(name, floor, status) value (apartment_name, floor_id, status_int);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_company` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `insert_company`(in name_in nvarchar(255),in phone_in nvarchar(10),in office_in int)
begin
	update apartment set status = 1 where id = office_in;
    insert into company(name, phone, apartment) value (name_in, phone_in, office_in);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_company_from_file` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `insert_company_from_file`(in building_name nvarchar(50),in floor_name int ,in office_name nvarchar(50), in name_company nvarchar(255),in phone_in nvarchar(10))
begin
	declare building_id int;
    declare floor_id int;
    declare office_id int;
    select id into building_id from building where name = building_name limit 1;
    select f.id into floor_id from floor as f join building as b on f.building = b.id where f.name = floor_name and b.id = building_id limit 1;
    select a.id into office_id from apartment as a join floor as f on a.floor = f.id where f.id = floor_id and a.name = office_name limit 1;
    call insert_company(name_company, phone_in, office_id);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_door_from_file` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `insert_door_from_file`(in floor_id int, in door_id int, in role_name nvarchar(50))
begin
	declare role_id int;
	select r.id into role_id from role_door as r where r.name = role_name limit 1;
    insert into door(name, floor, role) value (door_id, floor_id, role_id);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_office_from_file` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `insert_office_from_file`(in building_name nvarchar(50),  floor_name int, in name_in nvarchar(50), in status_in nvarchar(50))
begin
	declare building_id int;
    declare floor_id int;
    declare status_int int;
    set status_int = if (status_in = 'Available', 0, 1);
    select b.id into building_id from building as b where b.name = building_name limit 1;
    select f.id into floor_id from building as b join floor as f on f.building = b.id where b.id = building_id and f.name = floor_name limit 1;
    insert into apartment(name, floor, status) value (name_in, floor_id, status_int);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_resident` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `insert_resident`(in apartment_in int,in name_in nvarchar(255),in name_en_in varchar(50),in birthday_in date, in gender_in int, in phone_in varchar(10), in id_card_in varchar(12), in village_in nvarchar(255), in current_accommodation_in text)
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
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_resident_from_file` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `insert_resident_from_file`(in apartment_name nvarchar(50), in name_in nvarchar(255), in name_en_in varchar(50), in birthday_in date, in gender_in varchar(10),in phone_in varchar(10), in id_card_in varchar(12),in village_in nvarchar(255), in cur_accom text)
begin
	declare apartment_id int;
    declare gender_new int;
    set gender_new = if(gender_in ='Male', 1, 0);
    select a.id into apartment_id from apartment as a where a.name = apartment_name limit 1;
    call insert_resident(apartment_id, name_in, name_en_in, birthday_in, gender_new, phone_in, id_card_in, village_in, cur_accom);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_staff_from_file` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `insert_staff_from_file`(in company_name nvarchar(255), in office_name nvarchar(50), in name_in nvarchar(255), in name_en_in varchar(50), in birthday_in date, in gender_in varchar(10),in phone_in varchar(10), in id_card_in varchar(12),in village_in nvarchar(255), in cur_accom text)
begin
	declare company_id int;
    declare office_id int;
    declare gender_new int;
    set gender_new = if(gender_in ='Male', 1, 0);
    select a.id into office_id from apartment as a where a.name = office_name limit 1;
    select c.id into company_id from company as c where c.name = company_name and c.apartment = office_id limit 1;
    call insert_staff(company_id, name_in, name_en_in, birthday_in, gender_new, phone_in, id_card_in, village_in, cur_accom);
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_company` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`henrydb`@`localhost` PROCEDURE `update_company`(in id_in int, in name_in nvarchar(255),in phone_in nvarchar(10),in office_in_cur int, in office_in_new int)
begin
    update apartment set status = 0 where id = office_in_cur;
	update apartment set status = 1 where id = office_in_new;
    update company set name = name_in, phone = phone_in, apartment = office_in_new where id = id_in;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-12 22:13:30
