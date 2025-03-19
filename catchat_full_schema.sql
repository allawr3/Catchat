-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: Catchat
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.22.04.1

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
-- Table structure for table `bot_actions`
--

DROP TABLE IF EXISTS `bot_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bot_actions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `intent_id` int DEFAULT NULL,
  `action_type` varchar(255) DEFAULT NULL,
  `action_details` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `intent_id` (`intent_id`),
  CONSTRAINT `bot_actions_ibfk_1` FOREIGN KEY (`intent_id`) REFERENCES `intents` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bot_logs`
--

DROP TABLE IF EXISTS `bot_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bot_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `intent_id` int DEFAULT NULL,
  `action_taken` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `intent_id` (`intent_id`),
  CONSTRAINT `bot_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `bot_logs_ibfk_2` FOREIGN KEY (`intent_id`) REFERENCES `intents` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bot_performance_metrics`
--

DROP TABLE IF EXISTS `bot_performance_metrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bot_performance_metrics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `metric_name` varchar(255) DEFAULT NULL,
  `metric_value` float DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bot_responses`
--

DROP TABLE IF EXISTS `bot_responses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bot_responses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `intent` varchar(255) NOT NULL,
  `response` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `chat_history`
--

DROP TABLE IF EXISTS `chat_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `message` text,
  `response` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `chat_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `conversation_topics`
--

DROP TABLE IF EXISTS `conversation_topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversation_topics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `topic_name` varchar(255) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `comments` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `intents`
--

DROP TABLE IF EXISTS `intents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `intent_name` varchar(255) NOT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `keywords`
--

DROP TABLE IF EXISTS `keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keywords` (
  `id` int NOT NULL AUTO_INCREMENT,
  `intent_id` int DEFAULT NULL,
  `keyword` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `intent_id` (`intent_id`),
  CONSTRAINT `keywords_ibfk_1` FOREIGN KEY (`intent_id`) REFERENCES `intents` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `knowledge_base`
--

DROP TABLE IF EXISTS `knowledge_base`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knowledge_base` (
  `id` int NOT NULL AUTO_INCREMENT,
  `topic` varchar(255) DEFAULT NULL,
  `content` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scheduled_tasks`
--

DROP TABLE IF EXISTS `scheduled_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scheduled_tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_name` varchar(255) DEFAULT NULL,
  `task_details` text,
  `scheduled_time` timestamp NULL DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `scheduled_tasks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `session_start` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `session_end` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_interactions`
--

DROP TABLE IF EXISTS `user_interactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_interactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `total_interactions` int DEFAULT '0',
  `last_interaction` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_interactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_preferences`
--

DROP TABLE IF EXISTS `user_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_preferences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `preference_key` varchar(255) DEFAULT NULL,
  `preference_value` text,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_preferences_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `last_login` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-19 12:15:54

-- New tables for Catchat Quantum Integration

-- Table for quantum applications registry
CREATE TABLE IF NOT EXISTS `quantum_applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `category` ENUM('Decision', 'Security', 'Finance', 'Creative', 'Scientific', 'Everyday', 'Business', 'Healthcare') NOT NULL,
  `complexity` ENUM('Basic', 'Intermediate', 'Advanced') NOT NULL,
  `qubit_requirement` int NOT NULL DEFAULT 3,
  `circuit_template` text,
  `parameter_schema` JSON,
  `requires_randomness` BOOLEAN DEFAULT FALSE,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table for mapping user intents to quantum applications
CREATE TABLE IF NOT EXISTS `quantum_intent_mapping` (
  `id` int NOT NULL AUTO_INCREMENT,
  `intent_pattern` text NOT NULL,
  `quantum_application_id` int NOT NULL,
  `confidence_threshold` float NOT NULL DEFAULT 0.7,
  `parameter_extraction_pattern` text,
  `example_phrases` JSON,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `quantum_application_id` (`quantum_application_id`),
  CONSTRAINT `quantum_intent_mapping_ibfk_1` FOREIGN KEY (`quantum_application_id`) REFERENCES `quantum_applications` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table for quantum system catalog
CREATE TABLE IF NOT EXISTS `quantum_systems_catalog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `system_name` varchar(50) NOT NULL,
  `qubit_count` int NOT NULL,
  `system_type` ENUM('QVM', 'Noisy QVM', 'QPU') NOT NULL,
  `is_free` BOOLEAN DEFAULT TRUE,
  `requires_api_key` BOOLEAN DEFAULT FALSE,
  `description` text,
  `technical_specs` JSON,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_name` (`system_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table for hardware performance tracking
CREATE TABLE IF NOT EXISTS `hardware_performance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hardware_id` varchar(50) NOT NULL,
  `application_id` int NOT NULL,
  `avg_execution_time` float NOT NULL,
  `success_rate` float NOT NULL,
  `error_rate` float NOT NULL,
  `last_calibration` timestamp NULL DEFAULT NULL,
  `availability_percentage` float DEFAULT 99.9,
  `is_free` BOOLEAN DEFAULT TRUE,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hardware_application` (`hardware_id`, `application_id`),
  KEY `application_id` (`application_id`),
  CONSTRAINT `hardware_performance_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `quantum_applications` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table for application execution logs
CREATE TABLE IF NOT EXISTS `application_execution_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `application_id` int NOT NULL,
  `hardware_id` varchar(50) NOT NULL,
  `execution_time` float NOT NULL,
  `success` BOOLEAN NOT NULL,
  `error_message` text,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `application_id` (`application_id`),
  CONSTRAINT `application_execution_logs_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `quantum_applications` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table for verifying quantum operations
CREATE TABLE IF NOT EXISTS `quantum_operation_verification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `operation_id` varchar(64) NOT NULL,
  `user_id` int NOT NULL,
  `application_id` int NOT NULL,
  `raw_qubits_state` text NOT NULL,
  `verification_hash` varchar(128) NOT NULL,
  `circuit_visualization_data` JSON,
  `hardware_used` varchar(50) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operation_id` (`operation_id`),
  KEY `user_id` (`user_id`),
  KEY `application_id` (`application_id`),
  CONSTRAINT `quantum_operation_verification_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `quantum_operation_verification_ibfk_2` FOREIGN KEY (`application_id`) REFERENCES `quantum_applications` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table for user quantum preferences
CREATE TABLE IF NOT EXISTS `user_quantum_preferences` (
  `user_id` int NOT NULL,
  `preferred_hardware` JSON,
  `favorite_applications` JSON,
  `quantum_literacy_level` ENUM('Beginner', 'Intermediate', 'Advanced') DEFAULT 'Beginner',
  `interface_complexity_preference` ENUM('Simple', 'Standard', 'Advanced') DEFAULT 'Simple',
  `usage_stats` JSON,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_quantum_preferences_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Initial data for quantum systems catalog
INSERT INTO `quantum_systems_catalog`
(system_name, qubit_count, system_type, is_free, requires_api_key, description)
VALUES
(
    '9q-square-qvm',
    9,
    'QVM',
    TRUE,
    FALSE,
    'A 9-qubit quantum virtual machine in a square topology. Provides ideal qubit simulation without noise.'
),
(
    '9q-square-noisy-qvm',
    9,
    'Noisy QVM',
    TRUE,
    FALSE,
    'A 9-qubit noisy quantum virtual machine in a square topology. Simulates realistic quantum behavior including decoherence and gate errors.'
),
(
    'Ankaa-3',
    3,
    'QPU',
    FALSE,
    TRUE,
    'Rigetti Ankaa-3 quantum processing unit. A real quantum processor providing true quantum computation capabilities, available with purchase of an API key.'
);

-- Initial data for quantum applications
INSERT INTO `quantum_applications` 
(name, description, category, complexity, qubit_requirement, requires_randomness, parameter_schema)
VALUES
(
    'Basic Decision Helper', 
    'Quantum-powered decision making between user-provided options',
    'Decision',
    'Basic',
    3,
    TRUE,
    '{"parameters": ["options"], "response_format": {"decision": "string", "confidence": "number", "alternatives": ["string"]}}'
),
(
    'Rock Paper Scissors', 
    'Play rock paper scissors against a truly random quantum opponent',
    'Everyday',
    'Basic',
    2,
    TRUE,
    '{"parameters": ["choice"], "response_format": {"user_choice": "string", "quantum_choice": "string", "result": "string", "stats": {"wins": "number", "losses": "number", "ties": "number"}}}'
),
(
    'Bitcoin Blockchain Nonce Generator', 
    'Generate optimal nonce values for Bitcoin mining using quantum entropy',
    'Finance',
    'Basic',
    5,
    TRUE,
    '{"parameters": ["difficulty"], "response_format": {"nonce_ranges": ["string"], "quantum_entropy_source": "string", "verification_hash": "string"}}'
),
(
    'Powerball Lottery Number Generator', 
    'Generate truly random selections for Powerball lottery',
    'Everyday',
    'Basic',
    5,
    TRUE,
    '{"parameters": [], "response_format": {"white_balls": [{"number": "number"}], "powerball": "number", "verification_hash": "string"}}'
),
(
    'Mega Millions Lottery Number Generator', 
    'Generate truly random selections for Mega Millions lottery',
    'Everyday',
    'Basic',
    5,
    TRUE,
    '{"parameters": [], "response_format": {"white_balls": [{"number": "number"}], "mega_ball": "number", "verification_hash": "string"}}'
),
(
    'Available Quantum Systems', 
    'Provides a comprehensive list of all available quantum systems with their specifications, availability, and access requirements.',
    'Everyday',
    'Basic',
    0,
    FALSE,
    '{"parameters": [], "response_format": {"systems": [{"name": "string", "qubits": "number", "type": "string", "is_free": "boolean", "description": "string"}]}}'
);

-- Initial data for quantum intent mapping
INSERT INTO `quantum_intent_mapping` 
(intent_pattern, quantum_application_id, confidence_threshold, parameter_extraction_pattern, example_phrases)
VALUES
-- Decision Helper
('(help|assist)?.*(decide|choose|pick|select).*between', 1, 0.75, 
 '(?:between|from|choices:?)\s+((?:[^,]+,\s*)*[^,]+(?:\s+(?:and|or)\s+[^,]+)?)', 
 '["Help me decide between A and B", "Choose between these options", "I need to pick one of these choices"]'),

-- Rock Paper Scissors
('(play|let\'?s play|game of)?.*(rock paper scissors|rps)', 2, 0.8, 
 NULL, 
 '["Let\'s play rock paper scissors", "I want to play RPS", "Rock paper scissors game"]'),

-- Bitcoin Nonce Generator
('(generate|create|find)?.*(bitcoin|btc).*(nonce|mining)', 3, 0.7, 
 '(?:difficulty|target):\s*([0-9a-fA-F]+)', 
 '["Generate a Bitcoin nonce", "Help me with Bitcoin mining", "Find optimal BTC nonces"]'),

-- Powerball Numbers
('(generate|pick|choose|select)?.*(powerball).*(numbers|lottery)', 4, 0.8, 
 NULL, 
 '["Generate Powerball numbers", "Pick Powerball lottery numbers for me", "I need Powerball numbers"]'),

-- Mega Millions Numbers
('(generate|pick|choose|select)?.*(mega millions).*(numbers|lottery)', 5, 0.8, 
 NULL, 
 '["Generate Mega Millions numbers", "Pick Mega Millions lottery numbers for me", "I need Mega Millions numbers"]'),

-- Available Quantum Systems
('(show|list|display|tell).*(available|accessible)?.*(quantum|qubit|qpu).*(systems|computers|hardware|processors|backends)', 6, 0.8,
 NULL,
 '["Show me available quantum systems", "List quantum hardware", "What quantum computers can I use?", "Tell me about available quantum processors"]');

-- Initial hardware performance data
INSERT INTO `hardware_performance` 
(hardware_id, application_id, avg_execution_time, success_rate, error_rate, availability_percentage, is_free)
VALUES
('9q-square-qvm', 1, 0.5, 0.99, 0.01, 99.9, TRUE),
('9q-square-noisy-qvm', 1, 0.8, 0.92, 0.08, 99.9, TRUE),
('Ankaa-3', 1, 1.2, 0.96, 0.04, 95.0, FALSE),
('9q-square-qvm', 2, 0.3, 0.99, 0.01, 99.9, TRUE),
('9q-square-noisy-qvm', 2, 0.5, 0.95, 0.05, 99.9, TRUE),
('Ankaa-3', 2, 0.8, 0.98, 0.02, 95.0, FALSE),
('9q-square-qvm', 3, 0.8, 0.97, 0.03, 99.9, TRUE),
('9q-square-noisy-qvm', 3, 1.2, 0.94, 0.06, 99.9, TRUE),
('Ankaa-3', 3, 1.5, 0.97, 0.03, 95.0, FALSE),
('9q-square-qvm', 4, 0.6, 0.98, 0.02, 99.9, TRUE),
('9q-square-noisy-qvm', 4, 0.9, 0.93, 0.07, 99.9, TRUE),
('Ankaa-3', 4, 1.1, 0.96, 0.04, 95.0, FALSE),
('9q-square-qvm', 5, 0.6, 0.98, 0.02, 99.9, TRUE),
('9q-square-noisy-qvm', 5, 0.9, 0.93, 0.07, 99.9, TRUE),
('Ankaa-3', 5, 1.1, 0.96, 0.04, 95.0, FALSE),
('9q-square-qvm', 6, 0.2, 1.00, 0.00, 99.9, TRUE),
('9q-square-noisy-qvm', 6, 0.2, 1.00, 0.00, 99.9, TRUE),
('Ankaa-3', 6, 0.2, 1.00, 0.00, 95.0, FALSE);
