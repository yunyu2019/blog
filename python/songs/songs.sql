-- MySQL dump 10.13  Distrib 5.5.47, for Win32 (x86)
--
-- Host: localhost    Database: songs
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
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '作者名字',
  `dynasty_id` int(10) unsigned DEFAULT '0' COMMENT '朝代id',
  `dynasty` varchar(50) DEFAULT NULL COMMENT '朝代',
  `author_url` varchar(50) DEFAULT NULL COMMENT '原作者链接',
  `faceimg` varchar(100) DEFAULT NULL,
  `descp` text COMMENT '作者描述',
  `pinyin` varchar(50) DEFAULT NULL COMMENT '作者拼音全拼',
  `relation_urls` varchar(300) DEFAULT NULL,
  `status` tinyint(1) unsigned DEFAULT '1' COMMENT '作者状态',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `author_relation`
--

DROP TABLE IF EXISTS `author_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author_relation` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `author_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '作者id',
  `title` varchar(100) NOT NULL DEFAULT '' COMMENT '故事标题',
  `description` text CHARACTER SET utf8mb4 COMMENT '作者相关故事内容',
  `created` int(11) unsigned DEFAULT '0' COMMENT '录入时间',
  `editor` varchar(100) DEFAULT NULL,
  `view_url` varchar(100) DEFAULT NULL COMMENT '原始链接地址',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `content`
--

DROP TABLE IF EXISTS `content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `author_id` mediumint(8) unsigned NOT NULL DEFAULT '0' COMMENT '作者id',
  `dynasty_id` int(10) unsigned DEFAULT '0' COMMENT '朝代id',
  `title` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '古文标题',
  `content` mediumtext CHARACTER SET utf8mb4 COMMENT '古文内容',
  `created` int(11) unsigned DEFAULT '0' COMMENT '录入时间',
  `view_url` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '古文原文链接地址',
  `comment_num` mediumint(8) unsigned DEFAULT '0' COMMENT '评论人数',
  `point` decimal(2,1) unsigned DEFAULT '0.0' COMMENT '评分(0-10)',
  `status` tinyint(1) unsigned DEFAULT '1' COMMENT '文章状态',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `content_relation`
--

DROP TABLE IF EXISTS `content_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_relation` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `cont_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '古文id',
  `title` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '古文相关标题',
  `descrp` text CHARACTER SET utf8 COMMENT '古文相关内容',
  `created` int(11) unsigned DEFAULT '0' COMMENT '录入时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dynasty`
--

DROP TABLE IF EXISTS `dynasty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dynasty` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT '朝代',
  `created` int(11) unsigned DEFAULT '0' COMMENT '加入时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-08 15:51:40
