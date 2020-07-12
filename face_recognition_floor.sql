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
-- Table structure for table `floor`
--

DROP TABLE IF EXISTS `floor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `floor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` int(11) NOT NULL,
  `building` int(11) DEFAULT NULL,
  `type_of_floor` int(11) DEFAULT NULL,
  `number_of_apartment` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`building`),
  KEY `building` (`building`),
  KEY `type_of_floor` (`type_of_floor`),
  CONSTRAINT `floor_ibfk_1` FOREIGN KEY (`building`) REFERENCES `building` (`id`) ON DELETE CASCADE,
  CONSTRAINT `floor_ibfk_2` FOREIGN KEY (`type_of_floor`) REFERENCES `type_of_floor` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_520_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `floor`
--

LOCK TABLES `floor` WRITE;
/*!40000 ALTER TABLE `floor` DISABLE KEYS */;
INSERT INTO `floor` VALUES (1,1,1,1,20),(2,2,1,1,20),(3,3,1,1,20),(4,4,1,1,40),(5,5,1,2,20),(6,1,2,1,20),(7,2,2,1,20),(8,3,2,1,20),(9,4,2,1,20),(10,5,2,2,40),(11,1,3,1,20),(12,2,3,1,20),(13,3,3,1,20),(14,4,3,1,20),(15,5,3,2,20),(16,6,1,2,40),(17,7,1,2,40),(18,8,1,2,40),(19,9,1,2,40),(20,10,1,2,40),(21,11,1,2,40),(22,12,1,2,40),(23,13,1,2,40),(24,14,1,2,40),(25,15,1,2,40),(26,16,1,2,40),(27,17,1,2,40),(28,18,1,2,40),(29,19,1,2,40),(30,20,1,2,40),(31,21,1,2,40),(32,22,1,2,40),(33,23,1,2,40),(34,24,1,2,40),(35,25,1,2,40),(36,26,1,2,40),(37,27,1,2,40),(38,28,1,2,40),(39,29,1,2,30),(40,6,2,2,40),(41,7,2,2,40),(42,8,2,2,40),(43,9,2,2,40),(44,10,2,2,40),(45,11,2,2,40),(46,12,2,2,40),(47,13,2,2,40),(48,14,2,2,40),(49,15,2,2,40),(50,16,2,2,40),(51,17,2,2,40),(52,18,2,2,40),(53,19,2,2,40),(54,20,2,2,40),(55,21,2,2,40),(56,22,2,2,40),(57,23,2,2,40),(58,24,2,2,40),(59,25,2,2,40),(60,26,2,2,40),(61,27,2,2,40),(62,28,2,2,40),(63,29,2,2,30),(64,6,3,2,40),(65,7,3,2,40),(66,8,3,2,40),(67,9,3,2,40),(68,10,3,2,40),(69,11,3,2,40),(70,12,3,2,40),(71,13,3,2,40),(72,14,3,2,40),(73,15,3,2,40),(74,16,3,2,40),(75,17,3,2,40),(76,18,3,2,40),(77,19,3,2,40),(78,20,3,2,40),(79,21,3,2,40),(80,22,3,2,40),(81,23,3,2,40),(82,24,3,2,40),(83,25,3,2,40),(84,26,3,2,40),(85,27,3,2,40),(86,28,3,2,40),(87,29,3,2,30);
/*!40000 ALTER TABLE `floor` ENABLE KEYS */;
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
