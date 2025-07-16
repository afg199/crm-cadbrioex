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
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (27,'Patricio ','Garcia','22233355G','Bad','Merida','C/ La ruina','02233','655555666','Patricio@gmail.com','2025-06-30 18:23:25'),(29,'Manolo','Yuea','2222','Bada','Cala','ads','asd','asd','arro@df','2025-07-01 17:48:59'),(30,'Fonsi','Yea','5555','Cal','Badajoz','ca','012','66666','ad@la','2025-07-01 17:51:09'),(32,'Patricio','Garcia','22223333','Badajoz','Calamonte','C/esa','06810','555222333','patri@asd','2025-07-04 16:31:46'),(33,'Manuel','Asi','555','Calamonte','Badajoz','cc','0625','5252332','asd@as','2025-07-08 19:02:10');
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
  KEY `id_clientes_idx` (`id_Clientes`),
  CONSTRAINT `id_clientes` FOREIGN KEY (`id_Clientes`) REFERENCES `clientes` (`id_Clientes`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipos`
--

LOCK TABLES `equipos` WRITE;
/*!40000 ALTER TABLE `equipos` DISABLE KEYS */;
INSERT INTO `equipos` VALUES (11,27,'EOX','12KW Rosa','00000001',1,12,2,'2025-06-30','asd'),(15,29,'Ferroli','15KW ','555555',1,12,1,'2025-07-01','- Salón de vivienda'),(16,29,'Bronpi','12KW Rita','222233335555',1,12,2,'2025-07-09','aaaa'),(17,29,'Lasian','Audaz 8kW','888888888',2,0,2,'2025-07-01','-'),(18,30,'CADHOT','15KW','5522236',1,12,1,'2024-03-12','-');
/*!40000 ALTER TABLE `equipos` ENABLE KEYS */;
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
  KEY `id_equipo_idx` (`id_Equipo`),
  CONSTRAINT `id_equipo` FOREIGN KEY (`id_Equipo`) REFERENCES `equipos` (`id_Equipos`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicios`
--

LOCK TABLES `servicios` WRITE;
/*!40000 ALTER TABLE `servicios` DISABLE KEYS */;
INSERT INTO `servicios` VALUES (14,11,1,'2025-06-30','Miguel',3,'Salida humos'),(18,11,2,'2025-07-08','Miguel',12,'-'),(19,17,1,'2025-07-01','Miguel',3,'vvv'),(20,17,2,'2025-07-10','Miguel',12,'ss'),(21,17,2,'2025-07-02','Miguel',12,'as'),(22,18,1,'2024-01-12','Miguel',1,'-');
/*!40000 ALTER TABLE `servicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicios_piezas_reparacion`
--

DROP TABLE IF EXISTS `servicios_piezas_reparacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicios_piezas_reparacion` (
  `id_servicio_reparacion_pieza` int NOT NULL AUTO_INCREMENT,
  `id_servicio_reparacion` int NOT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  `marca` varchar(45) DEFAULT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  PRIMARY KEY (`id_servicio_reparacion_pieza`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicios_piezas_reparacion`
--

LOCK TABLES `servicios_piezas_reparacion` WRITE;
/*!40000 ALTER TABLE `servicios_piezas_reparacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicios_piezas_reparacion` ENABLE KEYS */;
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
  PRIMARY KEY (`id_Venta_Pellet`)
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
  PRIMARY KEY (`id_venta_productos`)
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

-- Dump completed on 2025-07-13 17:47:08
