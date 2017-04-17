-- MySQL dump 10.13  Distrib 5.5.47, for Win32 (x86)
--
-- Host: localhost    Database: huaban
-- ------------------------------------------------------
-- Server version	5.5.47-log

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
-- Table structure for table `photogirls`
--

DROP TABLE IF EXISTS `photogirls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `photogirls` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned DEFAULT '0',
  `like` int(10) unsigned DEFAULT NULL COMMENT '喜欢量',
  `image` varchar(100) DEFAULT NULL COMMENT '图片地址',
  `img_type` varchar(50) DEFAULT NULL,
  `created` int(10) unsigned DEFAULT '0' COMMENT '加入时间',
  `via` int(10) unsigned DEFAULT NULL,
  `pin_id` int(10) unsigned DEFAULT NULL,
  `repin_count` int(10) unsigned DEFAULT NULL,
  `original` int(10) unsigned DEFAULT NULL,
  `raw` varchar(300) DEFAULT NULL,
  `comment_count` int(10) unsigned DEFAULT NULL,
  `meta` varchar(3000) DEFAULT NULL,
  `link` varchar(300) DEFAULT NULL,
  `file_id` int(10) unsigned DEFAULT NULL,
  `via_user_id` int(10) unsigned DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `photogirls`
--
