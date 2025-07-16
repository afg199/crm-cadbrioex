-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: bd_cadbioex
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_Clientes` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `nif` varchar(15) DEFAULT NULL,
  `provincia` varchar(50) DEFAULT NULL,
  `poblacion` varchar(100) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `codigo_postal` varchar(15) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_Clientes`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Josete','Fernandez',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'nombre_cliente','apellido_cliente','nif_cliente',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'JOSE','JOSE','ASD',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'jose','ee','3333333h','bvas','asdads','asdasd','asdsad','6666622222','sdsdsd@gmail.com',NULL),(6,'Jose','enr','55566g','Badajoz','Calamonte','C/nrrrrsdsd','06810','666555444','ff@gmail.com',NULL),(7,'Jose','enr','55566g','Badajoz','Calamonte','C/nrrrrsdsd','06810','666555444','ff@gmail.com','2025-06-08 10:59:46'),(8,'joSE','ASDASD','ASDASD','ASDSAD','ASDSAD','ASDASD','ADSASD','ADSASD','ASDAS@SDS','2025-06-08 11:14:39'),(9,'joSE','ASDASD','ASDASD','ASDSAD','ASDSAD','ASDASD','ADSASD','ADSASD','ASDAS@SDS','2025-06-08 11:19:39'),(10,'sdf','sdf','sdf','sdf','sdf','sdf','sdf','sdf','sdf@df','2025-06-08 11:20:27'),(11,'sdf','sdf','sdf','sdf','sdf','sdf','sdf','sdf','sdf@df','2025-06-08 11:21:21'),(12,'fgh','fgh','fgh','fgh','fgh','fgh','fgh','fgh','fgh@sad','2025-06-08 11:21:47'),(13,'sdf','sdf','sdf','asd','ads','asd','asd','sdf','sdf@sd','2025-06-08 11:26:07'),(14,'tr','rt','rt','rt','sdf','sdf','sdf','rt','rt@44','2025-06-08 11:27:44'),(16,'Boorrrar','asd','asd','asd','adsa','asd','asd','asd','ad@asd','2025-06-08 12:20:04'),(17,'Jose','Macias','77755566L','Badajoz','Meriada','C/ El Peri, 666','06100','777666555','jmacias@gmail.com','2025-06-08 15:32:48'),(18,'Jose Angel MOD','Porro MOD','111222333G MOD','BarcelonaMOD','TarragonaMOD','C/ El moro, 55MOD','153645636256MOD','666555333MOD','hola@dronflay.comMOD','2025-06-14 09:14:01'),(19,'Jose aaaa','aaaaa','aaaaa','asd','asd','asd','asd','aaaaa','asd@asd.com','2025-06-14 09:15:44'),(20,'yeaa','sss','sss','sdsd','sd','asd','asd','sdsd','sdsd@dd','2025-06-15 20:01:49'),(21,'Antonio','Casa','11111111f','Bad','Cal','C/ sss','0000','666555222','asd@as','2025-06-27 18:06:31');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipos`
--

DROP TABLE IF EXISTS `equipos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipos` (
  `id_Equipos` int NOT NULL AUTO_INCREMENT,
  `id_Clientes` int NOT NULL,
  `marca` varchar(45) NOT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `n_serie` varchar(45) DEFAULT NULL,
  `garantia` int DEFAULT '0',
  `meses_garantia` int DEFAULT NULL,
  `compra_biomex` int DEFAULT '0',
  `fecha_compra` varchar(30) DEFAULT NULL,
  `comentario` varchar(1600) DEFAULT NULL,
  PRIMARY KEY (`id_Equipos`),
  KEY `id_Clientes_idx` (`id_Clientes`),
  CONSTRAINT `id_Clientes` FOREIGN KEY (`id_Clientes`) REFERENCES `clientes` (`id_Clientes`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipos`
--

LOCK TABLES `equipos` WRITE;
/*!40000 ALTER TABLE `equipos` DISABLE KEYS */;
INSERT INTO `equipos` VALUES (1,17,'NEO','12asd','12345',2,12,1,'2025-06-10','sad'),(2,17,'FELUX','13KW','1111111111111',1,12,1,'2025-06-11','sdasd'),(3,17,'asd','asd','asd',1,12,1,'2025-06-11','asd'),(4,19,'EOX','15KW aasd','55555666664448888',1,12,2,'2025-06-13','asdasdasdasd');
/*!40000 ALTER TABLE `equipos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio_limpieza`
--

DROP TABLE IF EXISTS `servicio_limpieza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio_limpieza` (
  `id_servicio_limpieza` int NOT NULL AUTO_INCREMENT,
  `id_Equipo` int NOT NULL,
  `fecha` varchar(30) NOT NULL,
  `trabajador` varchar(150) DEFAULT NULL,
  `horas` int DEFAULT NULL,
  `comentarios` varchar(1600) DEFAULT NULL,
  PRIMARY KEY (`id_servicio_limpieza`),
  KEY `id_Equipos_idx` (`id_Equipo`) /*!80000 INVISIBLE */,
  CONSTRAINT `id_Equipo` FOREIGN KEY (`id_Equipo`) REFERENCES `equipos` (`id_Equipos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio_limpieza`
--

LOCK TABLES `servicio_limpieza` WRITE;
/*!40000 ALTER TABLE `servicio_limpieza` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicio_limpieza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio_puesta_marcha`
--

DROP TABLE IF EXISTS `servicio_puesta_marcha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio_puesta_marcha` (
  `id_servicio_puesta_marcha` int NOT NULL AUTO_INCREMENT,
  `id_Equipos` int NOT NULL,
  `fecha` varchar(30) NOT NULL,
  `trabajador` varchar(150) DEFAULT NULL,
  `horas` int DEFAULT NULL,
  `comentario` varchar(1600) DEFAULT NULL,
  PRIMARY KEY (`id_servicio_puesta_marcha`),
  KEY `id_Equipos_idx` (`id_Equipos`),
  CONSTRAINT `id_Equipos` FOREIGN KEY (`id_Equipos`) REFERENCES `equipos` (`id_Equipos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio_puesta_marcha`
--

LOCK TABLES `servicio_puesta_marcha` WRITE;
/*!40000 ALTER TABLE `servicio_puesta_marcha` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicio_puesta_marcha` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio_reparacion`
--

DROP TABLE IF EXISTS `servicio_reparacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio_reparacion` (
  `id_servicio_reparacion` int NOT NULL AUTO_INCREMENT,
  `id_Equip` int NOT NULL,
  `fecha` varchar(30) NOT NULL,
  `trabajador` varchar(150) DEFAULT NULL,
  `horas` int DEFAULT NULL,
  `comentario` varchar(1600) DEFAULT NULL,
  PRIMARY KEY (`id_servicio_reparacion`),
  KEY `id_Equip_idx` (`id_Equip`),
  CONSTRAINT `id_Equip` FOREIGN KEY (`id_Equip`) REFERENCES `equipos` (`id_Equipos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio_reparacion`
--

LOCK TABLES `servicio_reparacion` WRITE;
/*!40000 ALTER TABLE `servicio_reparacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicio_reparacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio_reparacion_pieza`
--

DROP TABLE IF EXISTS `servicio_reparacion_pieza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio_reparacion_pieza` (
  `id_servicio_reparacion_pieza` int NOT NULL AUTO_INCREMENT,
  `id_servicio_reparacion` int NOT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  `marca` varchar(45) DEFAULT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  PRIMARY KEY (`id_servicio_reparacion_pieza`),
  KEY `id_servicio_reparacion_idx` (`id_servicio_reparacion`),
  CONSTRAINT `id_servicio_reparacion` FOREIGN KEY (`id_servicio_reparacion`) REFERENCES `servicio_reparacion` (`id_servicio_reparacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio_reparacion_pieza`
--

LOCK TABLES `servicio_reparacion_pieza` WRITE;
/*!40000 ALTER TABLE `servicio_reparacion_pieza` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicio_reparacion_pieza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicios`
--

DROP TABLE IF EXISTS `servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicios` (
  `id_Servicios` int NOT NULL AUTO_INCREMENT,
  `id_Equipo` int NOT NULL,
  `tipo_servicio` int NOT NULL,
  `fecha_servicio` varchar(30) DEFAULT NULL,
  `trabajador` varchar(150) DEFAULT NULL,
  `horas` int DEFAULT NULL,
  `comentario` varchar(1600) DEFAULT NULL,
  PRIMARY KEY (`id_Servicios`),
  KEY `id_Eq_idx` (`id_Equipo`),
  CONSTRAINT `id_Eq` FOREIGN KEY (`id_Equipo`) REFERENCES `equipos` (`id_Equipos`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicios`
--

LOCK TABLES `servicios` WRITE;
/*!40000 ALTER TABLE `servicios` DISABLE KEYS */;
INSERT INTO `servicios` VALUES (1,3,1,'2025-06-04','Miguel',12,'-ddddd'),(2,3,2,'2025-06-04','Miguel',12,'-sssss'),(3,3,2,'2025-06-14','Miguel',12,'asd'),(4,3,3,'2025-06-18','Miguel',5,'- Cambio de ffff'),(5,4,3,'2025-06-14','Jose',59,'- Tienen que volver a raparla'),(6,4,1,'2025-06-13','Jose',1,'- Todo ok');
/*!40000 ALTER TABLE `servicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicios_otros`
--

DROP TABLE IF EXISTS `servicios_otros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicios_otros` (
  `id_servicios_otros` int NOT NULL AUTO_INCREMENT,
  `id_Equi` int NOT NULL,
  `fecha` varchar(30) DEFAULT NULL,
  `trabajador` varchar(150) DEFAULT NULL,
  `horas` int DEFAULT NULL,
  `comentario` varchar(1600) DEFAULT NULL,
  PRIMARY KEY (`id_servicios_otros`),
  KEY `id_Equi_idx` (`id_Equi`),
  CONSTRAINT `id_Equi` FOREIGN KEY (`id_Equi`) REFERENCES `equipos` (`id_Equipos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicios_otros`
--

LOCK TABLES `servicios_otros` WRITE;
/*!40000 ALTER TABLE `servicios_otros` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicios_otros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name_surname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email_user` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `pass_user` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_user` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'YEAH','yeah@gmail.com','scrypt:32768:8:1$fbX1V9CPC8zP3qy2$3abb2933ffe62e837d59a0cbf067e906de6644ce411e89b20c3c0162aade596dcb3b2946624ef1454372672e66fa68cf8bce1696fa74c7e655cd275727cebf30','2025-06-06 17:33:11');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta_pellet`
--

DROP TABLE IF EXISTS `venta_pellet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta_pellet` (
  `id_Venta_Pellet` int NOT NULL AUTO_INCREMENT,
  `id_Client` int NOT NULL,
  `fecha` varchar(30) DEFAULT NULL,
  `cantidad_sacos` int DEFAULT NULL,
  `precio_saco` varchar(45) DEFAULT NULL,
  `marca_saco` varchar(150) DEFAULT NULL,
  `referencia_saco` varchar(50) DEFAULT NULL,
  `comentario` varchar(1600) DEFAULT NULL,
  PRIMARY KEY (`id_Venta_Pellet`),
  KEY `id_Client_idx` (`id_Client`),
  CONSTRAINT `id_Client` FOREIGN KEY (`id_Client`) REFERENCES `clientes` (`id_Clientes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta_pellet`
--

LOCK TABLES `venta_pellet` WRITE;
/*!40000 ALTER TABLE `venta_pellet` DISABLE KEYS */;
/*!40000 ALTER TABLE `venta_pellet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta_productos`
--

DROP TABLE IF EXISTS `venta_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta_productos` (
  `id_venta_productos` int NOT NULL AUTO_INCREMENT,
  `id_Clien` int NOT NULL,
  `fecha` varchar(30) DEFAULT NULL,
  `producto` varchar(100) DEFAULT NULL,
  `marca` varchar(45) DEFAULT NULL,
  `referencia` varchar(45) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `comentario` varchar(1600) DEFAULT NULL,
  PRIMARY KEY (`id_venta_productos`),
  KEY `id_Clien_idx` (`id_Clien`),
  CONSTRAINT `id_Clien` FOREIGN KEY (`id_Clien`) REFERENCES `clientes` (`id_Clientes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta_productos`
--

LOCK TABLES `venta_productos` WRITE;
/*!40000 ALTER TABLE `venta_productos` DISABLE KEYS */;
/*!40000 ALTER TABLE `venta_productos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-27 20:09:47
