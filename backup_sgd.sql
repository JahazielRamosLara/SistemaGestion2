-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: sgd_jalisco
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (3,'Administrador'),(2,'Responsable'),(1,'Secretaria');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (8,1,16),(2,1,25),(3,1,26),(4,1,28),(1,1,32),(9,1,36),(10,2,16),(6,2,26),(7,2,28),(5,2,32),(11,3,1),(12,3,2),(13,3,3),(14,3,4),(15,3,5),(16,3,6),(17,3,7),(18,3,8),(19,3,9),(20,3,10),(21,3,11),(22,3,12),(23,3,13),(24,3,14),(25,3,15),(26,3,16),(27,3,17),(28,3,18),(29,3,19),(30,3,20),(31,3,21),(32,3,22),(33,3,23),(34,3,24),(35,3,25),(36,3,26),(37,3,27),(38,3,28),(39,3,29),(40,3,30),(41,3,31),(42,3,32),(43,3,33),(44,3,34),(45,3,35),(46,3,36);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add documento',7,'add_documento'),(26,'Can change documento',7,'change_documento'),(27,'Can delete documento',7,'delete_documento'),(28,'Can view documento',7,'view_documento'),(29,'Can add estatus',8,'add_estatus'),(30,'Can change estatus',8,'change_estatus'),(31,'Can delete estatus',8,'delete_estatus'),(32,'Can view estatus',8,'view_estatus'),(33,'Can add transicion estatus',9,'add_transicionestatus'),(34,'Can change transicion estatus',9,'change_transicionestatus'),(35,'Can delete transicion estatus',9,'delete_transicionestatus'),(36,'Can view transicion estatus',9,'view_transicionestatus');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$UyMQqM73VnmWyDLX6nLuru$UZOmS+NouN8fbXEifOhGotBGHucINIUampk5f5lDG6g=','2025-11-09 04:38:06.676238',1,'jahaz','','','jachachel@gmail.com',1,1,'2025-11-07 19:08:46.000000'),(2,'pbkdf2_sha256$1000000$EJbFjgIbN0oa4OAVTG9Gvg$WEh6QNlUUROlTfah/fVD7To/BeCIL21mDvlqs5boULM=','2025-11-09 04:35:48.975091',0,'ejemplo_secretaria','','','',0,1,'2025-11-08 20:04:25.000000'),(3,'pbkdf2_sha256$1000000$D5sQUftosS8Z7qoVG5GiGc$pRteqFlinuSXjhBTt2h4jUD/RClVRM0v2eOLHfOY+i8=','2025-11-09 04:35:33.924228',0,'ejemplo_responsable','','','',0,1,'2025-11-08 20:05:52.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (9,1,3),(7,2,1),(8,3,2);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28),(29,1,29),(30,1,30),(31,1,31),(32,1,32),(33,1,33),(34,1,34),(35,1,35),(36,1,36);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_documento`
--

DROP TABLE IF EXISTS `core_documento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_documento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `folio` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `remitente` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `asunto` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `resumen` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_recepcion` date NOT NULL,
  `archivo_pdf` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `documento_salida` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_archivo` date DEFAULT NULL,
  `responsable_id` int DEFAULT NULL,
  `estatus_actual_id` bigint NOT NULL,
  `fecha_salida` date DEFAULT NULL,
  `folio_salida` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `folio` (`folio`),
  KEY `core_documento_responsable_id_3025b7db_fk_auth_user_id` (`responsable_id`),
  KEY `core_documento_estatus_actual_id_79831c0c_fk_core_estatus_id` (`estatus_actual_id`),
  CONSTRAINT `core_documento_estatus_actual_id_79831c0c_fk_core_estatus_id` FOREIGN KEY (`estatus_actual_id`) REFERENCES `core_estatus` (`id`),
  CONSTRAINT `core_documento_responsable_id_3025b7db_fk_auth_user_id` FOREIGN KEY (`responsable_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_documento`
--

LOCK TABLES `core_documento` WRITE;
/*!40000 ALTER TABLE `core_documento` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_documento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_estatus`
--

DROP TABLE IF EXISTS `core_estatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_estatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_estatus`
--

LOCK TABLES `core_estatus` WRITE;
/*!40000 ALTER TABLE `core_estatus` DISABLE KEYS */;
INSERT INTO `core_estatus` VALUES (1,'Capturado','Captura inicial del oficio.'),(2,'Notificado','El oficio es registrado y notificado por el sistema y correo al responsable'),(3,'En Trámite','Se da atención al oficio, requiere varios pasos o etapas.'),(4,'Turnado','Se turna a otra área de la misma coordinación.'),(5,'Terminado','El área finaliza su tarea correspondiente.'),(6,'Contestar por memo','Se regresa a la Secretaria indicando que la solicitud está finalizada para su respuesta.'),(7,'En Firma','Estado generado después de que la Secretaria realiza la \"Salida por turno\" y el documento debe imprimirse y firmarse.'),(8,'Archivado','El folio contestado es entregado al requirente o remitente y se guarda en registro.');
/*!40000 ALTER TABLE `core_estatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_transicionestatus`
--

DROP TABLE IF EXISTS `core_transicionestatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_transicionestatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `documento_id` bigint NOT NULL,
  `estatus_anterior_id` bigint NOT NULL,
  `estatus_nuevo_id` bigint NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_transicionestat_documento_id_c84fafbd_fk_core_docu` (`documento_id`),
  KEY `core_transicionestat_estatus_anterior_id_6325dc57_fk_core_esta` (`estatus_anterior_id`),
  KEY `core_transicionestat_estatus_nuevo_id_6bf4e439_fk_core_esta` (`estatus_nuevo_id`),
  KEY `core_transicionestatus_usuario_id_8b776e4c_fk_auth_user_id` (`usuario_id`),
  CONSTRAINT `core_transicionestat_documento_id_c84fafbd_fk_core_docu` FOREIGN KEY (`documento_id`) REFERENCES `core_documento` (`id`),
  CONSTRAINT `core_transicionestat_estatus_anterior_id_6325dc57_fk_core_esta` FOREIGN KEY (`estatus_anterior_id`) REFERENCES `core_estatus` (`id`),
  CONSTRAINT `core_transicionestat_estatus_nuevo_id_6bf4e439_fk_core_esta` FOREIGN KEY (`estatus_nuevo_id`) REFERENCES `core_estatus` (`id`),
  CONSTRAINT `core_transicionestatus_usuario_id_8b776e4c_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_transicionestatus`
--

LOCK TABLES `core_transicionestatus` WRITE;
/*!40000 ALTER TABLE `core_transicionestatus` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_transicionestatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-11-07 19:14:34.219569','1','Capturado',1,'[{\"added\": {}}]',8,1),(2,'2025-11-07 19:14:59.949413','2','Notificado',1,'[{\"added\": {}}]',8,1),(3,'2025-11-07 19:15:28.766194','3','En Trámite',1,'[{\"added\": {}}]',8,1),(4,'2025-11-07 19:15:50.496027','4','Turnado',1,'[{\"added\": {}}]',8,1),(5,'2025-11-07 19:16:10.270662','5','Terminado',1,'[{\"added\": {}}]',8,1),(6,'2025-11-07 19:17:02.549743','6','Contestar por memo',1,'[{\"added\": {}}]',8,1),(7,'2025-11-07 19:17:47.738410','7','En Firma',1,'[{\"added\": {}}]',8,1),(8,'2025-11-07 19:18:15.433582','8','Archivado',1,'[{\"added\": {}}]',8,1),(9,'2025-11-07 19:19:05.938189','1','Secretaria',1,'[{\"added\": {}}]',3,1),(10,'2025-11-07 19:19:10.597659','2','Responsable',1,'[{\"added\": {}}]',3,1),(11,'2025-11-07 19:23:59.507389','1','Secretaria',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(12,'2025-11-07 19:24:38.062435','2','Responsable',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(13,'2025-11-07 22:01:48.504664','1','jahaz',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(14,'2025-11-07 22:02:16.260739','1','jahaz',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(15,'2025-11-07 22:19:26.063870','1','jahaz',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(16,'2025-11-07 22:19:34.304467','1','jahaz',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(17,'2025-11-07 22:20:02.087670','1','jahaz',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(18,'2025-11-07 22:20:29.126140','1','jahaz',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(19,'2025-11-08 19:51:16.266950','1','jahaz',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(20,'2025-11-08 19:53:18.215262','1','jahaz',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(21,'2025-11-08 19:53:50.614621','1','jahaz',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(22,'2025-11-08 20:04:25.722175','2','ejemplo_secretaria',1,'[{\"added\": {}}]',4,1),(23,'2025-11-08 20:04:52.867613','2','ejemplo_secretaria',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(24,'2025-11-08 20:05:52.445567','3','ejemplo_responsable',1,'[{\"added\": {}}]',4,1),(25,'2025-11-08 20:05:55.911274','3','ejemplo_responsable',2,'[]',4,1),(26,'2025-11-08 20:06:22.263383','3','ejemplo_responsable',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(27,'2025-11-08 20:08:24.130686','3','ejemplo_responsable',2,'[]',4,1),(28,'2025-11-08 20:08:26.571392','2','ejemplo_secretaria',2,'[]',4,1),(29,'2025-11-08 20:08:55.170396','1','jahaz',2,'[]',4,1),(30,'2025-11-08 20:44:28.948926','1','Secretaria',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(31,'2025-11-08 20:44:47.182376','2','Responsable',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(32,'2025-11-08 20:46:15.841459','3','Administrador',1,'[{\"added\": {}}]',3,1),(33,'2025-11-08 20:46:31.002857','1','jahaz',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),(34,'2025-11-08 20:47:24.936971','3','ejemplo_responsable',2,'[]',4,1),(35,'2025-11-09 04:38:37.796346','10','Folio 0010 - Archivado',3,'',7,1),(36,'2025-11-09 04:38:37.796373','9','Folio 0009 - Turnado',3,'',7,1),(37,'2025-11-09 04:38:37.796386','8','Folio 0008 - Turnado',3,'',7,1),(38,'2025-11-09 04:38:37.796395','7','Folio 0007 - Archivado',3,'',7,1),(39,'2025-11-09 04:38:37.796405','6','Folio 0006 - Archivado',3,'',7,1),(40,'2025-11-09 04:38:37.796415','5','Folio 0005 - Turnado',3,'',7,1),(41,'2025-11-09 04:38:37.796424','4','Folio 0004 - Notificado',3,'',7,1),(42,'2025-11-09 04:38:37.796433','3','Folio 0003 - Archivado',3,'',7,1),(43,'2025-11-09 04:38:37.796441','2','Folio 0002 - Notificado',3,'',7,1),(44,'2025-11-09 04:38:37.796450','1','Folio 0001 - Notificado',3,'',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'core','documento'),(8,'core','estatus'),(9,'core','transicionestatus'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-11-07 18:46:29.870663'),(2,'auth','0001_initial','2025-11-07 18:46:30.175696'),(3,'admin','0001_initial','2025-11-07 18:46:30.249493'),(4,'admin','0002_logentry_remove_auto_add','2025-11-07 18:46:30.254048'),(5,'admin','0003_logentry_add_action_flag_choices','2025-11-07 18:46:30.258293'),(6,'contenttypes','0002_remove_content_type_name','2025-11-07 18:46:30.320010'),(7,'auth','0002_alter_permission_name_max_length','2025-11-07 18:46:30.354988'),(8,'auth','0003_alter_user_email_max_length','2025-11-07 18:46:30.367046'),(9,'auth','0004_alter_user_username_opts','2025-11-07 18:46:30.371255'),(10,'auth','0005_alter_user_last_login_null','2025-11-07 18:46:30.403321'),(11,'auth','0006_require_contenttypes_0002','2025-11-07 18:46:30.405231'),(12,'auth','0007_alter_validators_add_error_messages','2025-11-07 18:46:30.409460'),(13,'auth','0008_alter_user_username_max_length','2025-11-07 18:46:30.458177'),(14,'auth','0009_alter_user_last_name_max_length','2025-11-07 18:46:30.497944'),(15,'auth','0010_alter_group_name_max_length','2025-11-07 18:46:30.508263'),(16,'auth','0011_update_proxy_permissions','2025-11-07 18:46:30.512380'),(17,'auth','0012_alter_user_first_name_max_length','2025-11-07 18:46:30.549864'),(18,'sessions','0001_initial','2025-11-07 18:46:30.570660'),(19,'core','0001_initial','2025-11-07 18:53:50.726990'),(20,'core','0002_documento_fecha_salida_documento_folio_salida_and_more','2025-11-08 20:39:07.959555');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2rogkxmkm7egrdylu1elfta9voxp55dw','.eJxVjMEOwiAQRP-FsyFAlxY8evcbyO4CUjU0Ke3J-O9K0oMeZ96beYmA-1bC3tIa5ijOQovTb0fIj1Q7iHest0XyUrd1JtkVedAmr0tMz8vh_h0UbKWvwQ0me0SlBmbK3wQOHHmcFANZo1L0GVxiyw5QYyQXE2irDE40juL9AettOCg:1vHxBm:G-r0l4z8GtNfEqdV7YhsCrdBSHhVDdEuYyEPkDR4BM0','2025-11-09 06:38:06.678189'),('d8lqetxra7oq705f5mqlfafqmvz9nod0','.eJxVjEEOwiAQRe_C2pDC0FJduu8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uLsur0u0Wkh5Qd8B3LrWqqZV3mqHdFH7TpqbI8r4f7d5Cx5W-dYs_imTpzHkcAwz5JggGgE8tGLCGwM8gwiCdBS5Ks6QHFO4zoknp_AAOuOQ4:1vHrQx:pLb9pCwhiWEj5PT8wCw4nxEWrLVNGzHs-aYpKpAXE_Q','2025-11-09 00:29:23.284498'),('e0lxh7897hcttlvfdlyon7rmtloo8o77','.eJxVjEEOwiAQRe_C2pDC0FJduu8ZyDAzSNVAUtqV8e7apAvd_vfef6mA25rD1mQJM6uLsur0u0Wkh5Qd8B3LrWqqZV3mqHdFH7TpqbI8r4f7d5Cx5W-dYs_imTpzHkcAwz5JggGgE8tGLCGwM8gwiCdBS5Ks6QHFO4zoknp_AAOuOQ4:1vHx9Y:EJJWEom0pVP4ETKXyXTtG-iMdfQ1HwiZ1-J6p4MaD_g','2025-11-09 06:35:48.976513'),('jbzhv5h4k6ivumqmrizsgvas4incw6uu','.eJxVjMEOwiAQRP-FsyFAlxY8evcbyO4CUjU0Ke3J-O9K0oMeZ96beYmA-1bC3tIa5ijOQovTb0fIj1Q7iHest0XyUrd1JtkVedAmr0tMz8vh_h0UbKWvwQ0me0SlBmbK3wQOHHmcFANZo1L0GVxiyw5QYyQXE2irDE40juL9AettOCg:1vHoz6:1AE4u1svAtX7lozfF1yeVjVKfsNYGS1qDGG-HsySFjE','2025-11-22 19:52:28.522588'),('xtfexm12l8dkd4hds0tjy6piya4e5eqj','.eJxVjDsOwjAQBe_iGlnxJ46hpM8ZrN31GgeQLcVJhbh7EikFtG9m3kcEWJcc1sZzmKK4CSMuvxsCvbgcID6hPKqkWpZ5Qnko8qRNjjXy-366fwcZWt5rZnbWKo_kEiP1lHTqE3jtPGrGnYBiRcmgjc6QZ90NV0KnMA6g0IvvBhssOSA:1vHreB:5Rkv1A0AZIsVCH3AgQdkEcH60Dy4mS1Nj9n_0rsjbVo','2025-11-09 00:43:03.331053');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-09 22:39:53
