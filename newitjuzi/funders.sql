-- MySQL dump 10.13  Distrib 5.7.11, for Linux (x86_64)
--
-- Host: localhost    Database: funders
-- ------------------------------------------------------
-- Server version	5.7.11-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `fu_case`
--
USE funders;

DROP TABLE IF EXISTS `fu_investevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fu_investevent` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `type` bigint(2) NOT NULL,
  `companyId` bigint(10) NOT NULL,
  `phaseId` bigint(10) NOT NULL,
  `amount` float NOT NULL,
  `symbol` varchar(2) NOT NULL,
  `amountmsg` varchar(128) NOT NULL,
  `institutionId` bigint(10) NOT NULL,
  `institutionmsg` varchar(128) NOT NULL,
  `comment` varchar(128) NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lastmodified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `author` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22597 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `fu_merger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fu_merger` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `type` bigint(2) NOT NULL,
  `companyId` bigint(10) NOT NULL,
  `proportion` bigint(10) NOT NULL,
  `proportionmsg` varchar(128) NOT NULL,
  `amount` float NOT NULL,
  `symbol` varchar(2) NOT NULL,
  `amountmsg` varchar(128) NOT NULL,
  `institutionId` bigint(10) NOT NULL,
  `institutionmsg` varchar(128) NOT NULL,
  `comment` varchar(128) NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lastmodified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `author` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22597 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fu_company`
--

DROP TABLE IF EXISTS `fu_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fu_company` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `industryId` bigint(10) NOT NULL,
  `areaId` bigint(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11391 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fu_contacts`
--




--
-- Table structure for table `fu_industry`
--

DROP TABLE IF EXISTS `fu_industry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fu_industry` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `pid` bigint(10),
  `industryid` bigint(10) NOT NULL,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=909 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fu_insititution`
--

DROP TABLE IF EXISTS `fu_institution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fu_institution` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `institutionid` bigint(10) NOT NULL,
  `name` varchar(128) NOT NULL,
  `describe` text NOT NULL COMMENT '机构描述',
  `news` varchar(128) NOT NULL COMMENT '最近动态',
  `lastmodified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `author` varchar(128) NOT NULL COMMENT '修改人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3865 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `fu_phase`
--

DROP TABLE IF EXISTS `fu_phase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fu_phase` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `phaseId` bigint(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=561 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fu_area`
--

DROP TABLE IF EXISTS `fu_area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fu_area` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=561 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-12 20:13:15
