-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: recipeapp
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
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `uid` int NOT NULL,
  `rid` int NOT NULL,
  PRIMARY KEY (`uid`,`rid`),
  KEY `uid` (`uid`),
  KEY `rid` (`rid`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`),
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`rid`) REFERENCES `recipes` (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
INSERT INTO `favorites` VALUES (3,3),(6,2),(6,3),(6,5),(14,6),(14,9),(16,2),(16,7),(16,9),(16,17),(16,25),(16,26),(17,2),(17,5),(17,6),(17,8),(17,9),(17,17),(17,25),(17,26),(18,6),(18,10),(18,15),(18,25),(18,26),(19,2),(19,9),(19,10),(19,25),(19,26),(20,8),(20,9),(20,17),(20,25),(20,26),(22,3),(22,8),(22,9),(22,25),(22,26),(23,25),(23,26),(24,7),(24,8),(24,9),(24,15),(24,25),(24,26),(25,2),(25,6),(25,7);
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredients` (
  `rid` int DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `iid` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`iid`),
  KEY `rid` (`rid`),
  CONSTRAINT `ingredients_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `recipes` (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (3,'chicken','500g','meat',1),(3,'tomato','1/2','vegetable',2),(3,'rice','2 dl','rice',3),(5,'test','500g','test',4),(5,'tester','200g','tester',5),(2,'tomato','1/2','vegetable',6),(2,'rice','2 dl','rice',7),(6,'pork medallion','500g','meat',8),(6,'potato','2 whole','compliment',9),(6,'bbq sauce','200ml','sauce',10),(7,'test','500g','ing',11),(8,'Tortilla bread','2 whole','Bread',12),(8,'Chicken','500g','Meat',13),(8,'Taco sauce','1 spoon','Sauce',14),(8,'Shredded cheese','Enough','Cheese',15),(9,'Minced meat','500g','Meat',16),(9,'Carrot','1 whole','Vegetable',17),(9,'Yellow onion','1/3','Vegetable',18),(9,'Nicely cut tomato mess','1 package','Vegetable',19),(9,'Pasta of your choice','However much you want','Pasta',20),(10,'Chicken','2 files','Meat',21),(10,'Those small tomatoes','1 package','Vegetable',22),(10,'Roman salad','1 whole','Vegetable',23),(11,'Literally none','-','-',24),(15,'hashmap','2','unspecified',28),(15,'priority queue','1','unspecified',29),(16,'secret','secret','secret',30),(17,'Hamburger meat','1','meat',31),(17,'Salad','1 leaf','Vegetable',32),(17,'Tomato','1 slice','Vegetable',33),(17,'Cucumber','3 slices','Vegetable',34),(17,'Burger cheese','1 slice','Cheese',35),(17,'Bun','1','Bread',36),(18,'helloworld','helloworld','helloworld',37),(19,'CHicken','all','Meat',38),(20,'Rice','200g','rice',39),(20,'Water','enough','liquid',40),(21,'Rice','200g','rice',41),(21,'Water','not enough','liquid',42),(22,'Water','200','liquid',43),(22,'Flour','200','solid',44),(22,'yeast','eyeball it','mushroom',45),(22,'','','',46),(23,'Pure Caffeine powder','900g','Holy',47),(23,'Mint','4 leaves','Herb',48),(23,'Sugar','2 tbsp','sugar',49),(23,'PWO','100g','Mixed Alch',50),(24,'???? herb','3 leaves','herb',51),(24,'rosemary','10g','herb',52),(24,'biltema energy drink','2 cans','alchemical solution',53),(26,'olive oil','1 tbsp ','',63),(26,'onion','1','',64),(26,'medium carrot','1','',65),(26,'celery stick ','1','',66),(26,'garlic cloves','2','',67),(26,'beef mince','1kg','',68),(26,'canned crushed tomato','800g','',69),(26,'tomato paste','75g','',70),(26,'pinot noir red wine','250ml','',71),(26,'beef bouillon cubes','3 crumbled','',72),(26,'bay leaves','2','',73),(26,'dried thyme','0.5 tsp','',74),(26,'oregano','0.5 tsp','',75),(26,'Worcestershire Sauce','2 tsp','',76),(26,'sugar','1 - 2 tsp','',77),(26,'butter','60g','',78),(26,'flour','75g','',79),(26,'milk','1 litre','',80),(26,'Colby cheese','200g','',81),(26,'freshly ground nutmeg','pinch','',82),(26,'Salt and pepper','eyeball it','',83),(26,'lasagna sheets','350g','',84),(26,'mozzarella cheese','150g','',85),(26,'chopped basil or parsley','eyeball it','',86),(25,'graham cracker crumbs','170g','bread',87),(25,'sugar','2 Tablespoons','sugar',88),(25,'brown sugar','1 Tablespoon ','sugar',89),(25,'butter, melted','7 Tablespoons ','butter',90),(25,'cream cheese','910g','cheese',91),(25,'sour cream','160g','',92),(25,'vanilla extract','1 ½ teaspoons ','',93),(25,'salt','⅛ teaspoon','',94),(25,'eggs','4 large','',95);
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipes`
--

DROP TABLE IF EXISTS `recipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipes` (
  `rid` int NOT NULL AUTO_INCREMENT,
  `recipename` varchar(50) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `ispublic` tinyint DEFAULT NULL,
  `uid` int DEFAULT NULL,
  `lastmodified` date DEFAULT NULL,
  PRIMARY KEY (`rid`),
  KEY `uid` (`uid`),
  CONSTRAINT `recipes_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipes`
--

LOCK TABLES `recipes` WRITE;
/*!40000 ALTER TABLE `recipes` DISABLE KEYS */;
INSERT INTO `recipes` VALUES (2,'chicken recipe','tasty chicken',1,3,'2026-03-08'),(3,'chicken recipe','tasty chicken',1,3,NULL),(5,'a testy recipe','a very testing recipe',1,3,NULL),(6,'pork medallions','tasty pork medallions',1,6,NULL),(7,'testrescp','test',1,6,NULL),(8,'Chicken quesedilas','Tasty chicken quesedilas with taco sause',1,17,NULL),(9,'Pasta bolognese','Delicious pasta bolognes for you',1,17,NULL),(10,'Cesar salad','A fresh cesar salad with the bare minimum ingredients',1,16,NULL),(11,'The bare minimum','Feeling lazy? This for you',0,16,NULL),(15,'dijkstras special','Dijkstras special that will fry your brain',1,23,NULL),(16,'grandmas secret recipe','grandmas special recipe',0,23,NULL),(17,'hamburgir','tasty \"homemade\" hamburger',1,24,NULL),(18,'helloworld','helloworld',1,22,NULL),(19,'OFC','Oongaboonga fried chicken',1,26,NULL),(20,'Cooked rice','Cooked rice',0,26,NULL),(21,'Transmute Cooked rice to fried rice','',1,26,NULL),(22,'Bread','Bread',1,26,NULL),(23,'Potion of Haste','',1,26,NULL),(24,'Potion of LocoMotion','Not for public consumption magical drink that will summon a car if consumed',1,27,NULL),(25,'GranGrans CheeseCake','',1,28,'2026-05-26'),(26,'GranGrans Lasagne','',1,28,NULL);
/*!40000 ALTER TABLE `recipes` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `onRecipeUpdate` BEFORE UPDATE ON `recipes` FOR EACH ROW BEGIN
	SET NEW.lastmodified = current_timestamp();
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `rec_del_helper` BEFORE DELETE ON `recipes` FOR EACH ROW BEGIN
	DELETE FROM ingredients WHERE rid = OLD.rid;
    
    DELETE FROM steps WHERE rid = OLD.rid;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `steps`
--

DROP TABLE IF EXISTS `steps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `steps` (
  `rid` int NOT NULL,
  `stepNr` int NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`rid`,`stepNr`),
  KEY `rid` (`rid`),
  CONSTRAINT `steps_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `recipes` (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `steps`
--

LOCK TABLES `steps` WRITE;
/*!40000 ALTER TABLE `steps` DISABLE KEYS */;
INSERT INTO `steps` VALUES (2,1,'cut vegetables'),(2,2,'cook chicken'),(2,3,'DO NOT EAT'),(3,1,'cook rice'),(3,2,'cut vegetables'),(3,3,'cook chicken'),(5,1,'cook test'),(5,2,'cook tester'),(6,1,'cook pork medallion'),(6,2,'put potato in oven 30 minutes'),(6,3,'pour sauce on that meat'),(7,1,'cook test'),(7,2,'burn test'),(8,1,'Cook chicken'),(8,2,'Cut chicken into pieces'),(8,3,'Put chicken on tortilla bread, add taco sauce and cheese'),(8,4,'Fold tortilla and put on pan'),(9,1,'Cut onion and carrot'),(9,2,'Cook onion and carrot in saucepan'),(9,3,'Add minced meat and the cut tomato mess'),(9,4,'Let cook for a long time'),(9,5,'Boil pasta'),(10,1,'Cook chicken'),(10,2,'Cut chicken'),(10,3,'Cut tomatoes'),(10,4,'Tear up salad'),(10,5,'Mix into bowl, serve'),(11,1,'Call pizza store'),(11,2,'Order pizza delivery'),(11,3,'Relax'),(15,1,'Create a hashmap of visited nodes'),(15,2,'create a hashmap of parent values'),(15,3,'Add some edges and choose shortest path'),(16,1,'secret'),(17,1,'Cut vegetables into the specified thingy'),(17,2,'Cook the meat'),(17,3,'Add cheese when meat almost done, and continue cooking to let the cheese melt'),(17,4,'build your burger'),(18,1,'helloworld'),(19,1,'Manifest'),(19,2,'win'),(20,1,'put rice in water'),(20,2,'cook'),(20,3,'hope for the best'),(21,1,'Put rice in water'),(21,2,'Cook'),(21,3,'Dont burn down home cause not enough water'),(22,1,'Mix water and yeast'),(22,2,'add flour'),(22,3,'put in oven'),(22,4,'hope for the best.'),(23,1,'Fill a large jug with all dry ingredients'),(23,2,'add water copious amounts'),(23,3,'Dont drink in 1 sitting'),(25,1,'Preheat oven to 325F (160C).'),(25,2,'Prepare Graham Cracker crust first by combining graham cracker crumbs, sugar, and brown sugar, and stirring well. Add melted butter and use a fork to combine ingredients well.'),(25,3,'Pour crumbs into a 9” Springform pan and press firmly into the bottom and up the sides of your pan. Set aside.'),(25,4,'In the bowl of a stand mixer or in a large bowl (using a hand mixer) add cream cheese and stir until smooth and creamy (don’t over-beat or you’ll incorporate too much air). 32 oz cream cheese²'),(25,5,'Add sugar and stir again until creamy.'),(25,6,'Add sour cream, vanilla extract, and salt, and stir until well-combined. If using a stand mixer, make sure you pause periodically to scrape the sides and bottom of the bowl with a spatula so that all ingredients are evenly incorporated.'),(25,7,'With mixer on low speed, gradually add lightly beaten eggs, one at a time, stirring just until each egg is just incorporated. Once all eggs have been added, use a spatula to scrape the sides and bottom of the bowl again and make sure all ingredients are well combined.'),(25,8,'Pour cheesecake batter into prepared springform pan. To insure against leaks, place pan on a cookie sheet that’s been lined with foil.'),(25,9,'Transfer to the center rack of your oven and bake on 325F (160C) for 50-60 minutes (or longer as needed, see note 3). Edges will likely have slightly puffed and may have just begun to turn a light golden brown and the center should spring back to the touch but will still be Jello-jiggly. Don\'t over-bake or the texture will suffer, which means we all suffer.'),(25,10,'Remove from oven and allow to cool on top of the oven⁴ for 10 minutes. Once 10 minutes has passed, use a knife to gently loosen the crust from the inside of the springform pan (this will help prevent cracks as your cheesecake cools and shrinks). Do not remove the ring of the springform pan.'),(25,11,'Allow cheesecake to cool another 1-2 hours or until near room temperature before transferring to refrigerator and allowing to cool overnight or at least 6 hours. I remove the ring of the springform pan just before serving then return it to the pan to store. Enjoy!'),(26,1,'Heat oil in a large heavy based pot over medium heat. Add garlic, onion, celery and carrots. Cook for 10 minutes until softened and sweet – they should not brown (if they do, turn heat down).'),(26,2,'Add beef, turn heat up and cook the beef, breaking it up as you go.'),(26,3,'Once the beef has all turned brown, add the remaining Ragu ingredients EXCEPT the sugar.'),(26,4,'Stir then adjust the heat so it is bubbling very gently. Place the lid on and cook for 1.5 – 2 hours, stirring every now and then, then remove the lid and simmer for 30 minutes.'),(26,5,'The ragu is ready when the meat is really tender and the sauce has thickened and is rich – see video for consistency (Note 6). Adjust salt and pepper to taste, and add sugar if required (Note 3)'),(26,6,'Warm milk up in a saucepan (optional – just makes sauce thicken faster).'),(26,7,'In a large saucepan, melt butter over medium low heat. Add flour and mix constantly for 1 minute.'),(26,8,'Pour about 1 cup of the milk in, mixing as you go to incorporate into the flour mixture. Once mostly lump free, add remaining milk. Use a whisk if needed to make it lump free.'),(26,9,'Turn heat up to medium high. Stir occasionally at first then regularly after a few minutes until sauce thickens – about 5 – 8 minutes. It should coat the back of the wooden spoon.'),(26,10,'Remove from heat, add cheese, nutmeg, salt and pepper. Mix until the cheese is melted. The Sauce should be thick but still easily pourable – the consistency of heavy cream (you need to be able to drizzle it over the Ragu when layering – see video). If it’s too thick, add a splash of water or milk.'),(26,11,'Preheat oven to 180°C/350°F.'),(26,12,'Use a 33 x 22 x 7 cm / 13 x 9 x 2.5″ baking dish.'),(26,13,'Smear a bit of Ragu on the base, then cover with lasagna sheets. Tear sheets to fit.'),(26,14,'Spread over 2 1/2 cups of Ragu (enough to cover sheets), then drizzle over 1 cup of Cheese Sauce.'),(26,15,'Top with lasagna sheets (Note 7). Spread with another 2 1/2 cups of Ragu, then 1 cup of Cheese Sauce. Top with lasagna sheets then repeat 1 more time.'),(26,16,'Top with a 4th layer of lasagna sheets, then pour over the remaining Cheese Sauce.'),(26,17,'Sprinkle with Mozzarella, then bake for 25 minutes or until golden and bubbling.'),(26,18,'Stand for 5 to 10 minutes before cutting and serving, garnished with basil or parsley if desired.');
/*!40000 ALTER TABLE `steps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `uid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'test','test@email.com','$2b$12$y1Hgt4g9rEFNY/N7d4C0xehjBd6znoCBckP7.OVIXs6pYRzGBmzyu'),(6,'username','username@email.com','$2b$12$423i5.lp2ycwemLW1OLYCOLWmRN02u6jBZALvAcQXTcpHeX4T17uC'),(8,'tester','tester@email.com','$2b$12$PjSvsrHN1t1ovmfF6DyBn.SRvAdKLFCZW4J/igkAm/RKczBhh9REi'),(10,'tester','testing@email.com','$2b$12$PjSvsrHN1t1ovmfF6DyBn.SRvAdKLFCZW4J/igkAm/RKczBhh9REi'),(14,'Gurrnos','Gurrnos@email.com','$2b$12$XY/GSpcOOy7Vo38uIA9.H.mv.0M7Hn.3rgtJGjLfJlbrXx0uJMrf6'),(15,'Zadikiel','Zadikiel@email.com','$2b$12$XY/GSpcOOy7Vo38uIA9.H.7VuZwGW00GEp6AXimIOM6fx4PQimrX.'),(16,'Warp','Warp@email.com','$2b$12$XY/GSpcOOy7Vo38uIA9.H..0d7OcXzLSNFHoS9U7wu.8M7FQaQgly'),(17,'Hadal','Hadal@email.com','$2b$12$XY/GSpcOOy7Vo38uIA9.H.fQeQu.RVGnlz3C0ut02b9ZsxvFUcxVm'),(18,'KockenAnna','KockenAnna@email.com','$2b$12$XY/GSpcOOy7Vo38uIA9.H.k0TJQnR9dSYefoQxBDKGLZVgltmoeLi'),(19,'GordanRamsay','GordanRamsay@email.com','$2b$12$XY/GSpcOOy7Vo38uIA9.H.e/DCtCIyZ1f6zAhsn0a6lWgDhEOTFX.'),(20,'CookingAddict','CookingAddict@email.com','$2b$12$XY/GSpcOOy7Vo38uIA9.H.NBvn1WnFoIfT3h8J3RtvgwHv.m9uCqq'),(22,'helloworld','helloworld@email.com','$2b$12$fzlhDJsY0ibFsyu9.ClLaua1INqhmr9SHSkVtH/UIviVxcjpzggLq'),(23,'dijkstra','dijkstra@email.com','$2b$12$4yNgYjEvrEDAU1UxLTmQnOPZEmbJC/8X8OUrJdhldfQjOCEr/wmJ6'),(24,'gurrdogl','gurrdogl@gmail.com','$2b$12$aMPDCTio.DZ9G8Q5M7uWAemHgF.AE5zQe.yHs0re53MX/aupqrnEy'),(25,'myacc','myacc@email.com','$2b$12$aMPDCTio.DZ9G8Q5M7uWAe.xfAlTwYOzmiqbhowaP15gqaOVohFvi'),(26,'oongaboonga13','oongaboonga13@gmail.com','$2b$12$kcT6fAWibqgyxKZyDrDyEuBvOYpfpOlqmUqCL.CUwiLNyC6T0yUD6'),(27,'Alchemist','Alchemist@alchemy.gov','$2b$12$kcT6fAWibqgyxKZyDrDyEu83ztXCPEQot3gl0vZGl3A59OpXjs02G'),(28,'GranGran','GranGran@GranGran.com','$2b$12$kcT6fAWibqgyxKZyDrDyEugEJaibkaQ7Yuen4ex3tVzXvctwgV/ym');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `handle_delete` BEFORE DELETE ON `users` FOR EACH ROW BEGIN
	DELETE FROM favorites WHERE uid = old.uid;
    
    DELETE FROM recipes WHERE uid = old.uid;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Dumping routines for database 'recipeapp'
--
/*!50003 DROP PROCEDURE IF EXISTS `toggleFavorite` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `toggleFavorite`(
param_uid int,
param_rid int,
out results int
)
begin
    declare existance_flag int default 0;
    SELECT count(*) into existance_flag 
    FROM favorites where favorites.uid = param_uid 
    and favorites.rid = param_rid;
    
    if existance_flag = 0 then 
        INSERT INTO favorites(uid, rid) VALUES(param_uid, param_rid);
        set results = 1;
    else 
        DELETE FROM favorites WHERE uid=param_uid AND rid=param_rid;
        set results = 0;
    end if;
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

-- Dump completed on 2026-05-26 22:03:13
