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
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `name_en` varchar(50) COLLATE utf8_unicode_520_ci DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `id_card` varchar(12) COLLATE utf8_unicode_520_ci NOT NULL,
  `gender` int(11) DEFAULT NULL,
  `phone` varchar(10) COLLATE utf8_unicode_520_ci DEFAULT NULL,
  `village` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `current_accommodation` text COLLATE utf8_unicode_520_ci,
  `is_delete` int(11) DEFAULT NULL,
  `is_resident` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_card` (`id_card`),
  UNIQUE KEY `name_en` (`name_en`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES (1,'Hoàng Mai Nghị','NghiHM2406_618_29_06_20','1996-06-24','163355618',1,NULL,'Việt Hùng, Trực Ninh, Nam Định','Minh Khai, Bắc Từ Liêm, Hà Nội',0,1),(2,'Lê Thị Hồng Ngân','NganLH2509_619_29_06_20','1997-09-25','163355619',0,NULL,'Văn Miếu, Thanh Sơn, Phú Thọ','Hồ Tùng Mậu, Cầu Giấy, Hà Nội',0,1),(3,'Trần Văn Vụ','VuTV1004_620_29_06_20','2000-04-10','163355620',1,NULL,'Trực Bình, Trực Ninh, Nam Định','Hồ Tùng Mậu, Cầu Giấy, Hà Nội',0,1),(4,'Phạm Vũ Mạnh','ManhVP0207_621_29_06_20','1997-07-02','163355621',1,NULL,'Kim Bảng, Hà Nam','Trần Cung, Cầu Giấy, Hà Nội',0,1),(5,'Bui Đức Sinh','SinhDB2210_622_29_06_20','2001-10-22','163355622',1,NULL,'Nam Sách, Hải Dương','Minh Khai, Bắc Từ Liêm, Hà Nội',0,0),(6,'Bui Văn Trúc','TrucDB0208_623_29_06_20','1994-08-02','163355623',1,NULL,'Nam Sách, Hải Dương','Minh Khai, Bắc Từ Liêm, Hà Nội',0,0),(7,'Lê Thị Ánh','AnhLT2007_624_29_06_20','2000-07-20','163355624',0,NULL,'Kim Sơn, Ninh Bình','Thanh Xuân, Hà Nội',0,1),(8,'Trần Đức Long',NULL,'1978-06-10','162780125',1,'0986256817','Nguyễn Trãi, Thanh Xuân, Hà Nội','Đốc Ngữ, Ba Đình, Hà Nội',0,1);
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-12 22:13:30
