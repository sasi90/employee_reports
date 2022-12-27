CREATE DATABASE  IF NOT EXISTS `emp_report` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `emp_report`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: emp_report
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `emp_details`
--

DROP TABLE IF EXISTS `emp_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emp_details` (
  `s.no` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `emp_id` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `phn_num` varchar(20) DEFAULT NULL,
  `department` varchar(45) DEFAULT NULL,
  `reporting_manager` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`s.no`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emp_details`
--

LOCK TABLES `emp_details` WRITE;
/*!40000 ALTER TABLE `emp_details` DISABLE KEYS */;
INSERT INTO `emp_details` VALUES (1,'sasikumar','devaraj','1002','sasi@gmail.com','9994288732','Automation','Gaurav'),(2,'ramesh','kumar','1003','ramesh@gmail.com','8248595191','IT','SASI'),(3,'mahesh','babu','1005','mahesh@gmail.com','9824859519','IT','Suresh'),(19,'SMITH','ALLEN','1001','smith@gmail.com','9845645452','Admin','MARTINEZ'),(20,'JOHNSON','YOUNG','1004','john@gmail.com','9754543542','Hr','MARTINEZ'),(21,'WILLIAMS','WALKER','1006','willi@gmail.com','6875123122','IT','HERNANDEZ'),(22,'BROWN','ROBINSON','1008','brown@gmail.com','6654332452','Automation','MARTINEZ'),(23,'JONES','LEWIS','1009','jones@gmail.com','7875212121','Accounts','HERNANDEZ'),(24,'GARCIA','RAMIREZ','1010','garcia@gmail.com','8651321225','System admin','MARTINEZ'),(25,'MILLER','CLARK','1011','miller@gmail.com','9894422124','Accounts','HERNANDEZ'),(26,'DAVIS','SANCHEZ','1012','davis@gmail.com','8754545321','IT','MARTINEZ'),(27,'RODRIGUEZ','HARRIS','1013','rodri@gmail.com','9112255331','Hr','MARTINEZ');
/*!40000 ALTER TABLE `emp_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-27 14:47:43
