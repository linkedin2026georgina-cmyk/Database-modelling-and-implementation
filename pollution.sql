-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 08, 2025 at 03:07 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pollution`
--

-- --------------------------------------------------------

--
-- Table structure for table `Constituency`
--

CREATE TABLE `Constituency` (
  `c_name` varchar(50) NOT NULL,
  `mp_firstname` varchar(50) DEFAULT NULL,
  `mp_surname` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `DataSchema`
--

CREATE TABLE `DataSchema` (
  `ident` varchar(50) NOT NULL,
  `measure` varchar(50) DEFAULT NULL,
  `desc` varchar(200) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Measurement`
--

CREATE TABLE `Measurement` (
  `object_2` int(11) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `station_id` int(11) NOT NULL,
  `nitrogen_oxides` float DEFAULT NULL,
  `nitrogen_dioxide` float DEFAULT NULL,
  `nitric_oxide` float DEFAULT NULL,
  `pm_10` float DEFAULT NULL,
  `ozone_concentration` float DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `object_1` int(11) DEFAULT NULL,
  `non_vol_pm_10` float DEFAULT NULL,
  `vol_pm_10` float DEFAULT NULL,
  `non_vol_pm_2_5` float DEFAULT NULL,
  `pm_2_5` float DEFAULT NULL,
  `vol_pm_2_5` float DEFAULT NULL,
  `carbon_monoxide` float DEFAULT NULL,
  `relative_humidity` float DEFAULT NULL,
  `air_pressure` float DEFAULT NULL,
  `sulphur_dioxide` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Station`
--

CREATE TABLE `Station` (
  `sid` int(11) NOT NULL,
  `s_name` varchar(50) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `constituency_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Constituency`
--
ALTER TABLE `Constituency`
  ADD PRIMARY KEY (`c_name`);

--
-- Indexes for table `DataSchema`
--
ALTER TABLE `DataSchema`
  ADD PRIMARY KEY (`ident`);

--
-- Indexes for table `Measurement`
--
ALTER TABLE `Measurement`
  ADD PRIMARY KEY (`object_2`),
  ADD KEY `fk_Measurement_Station1_idx` (`station_id`);

--
-- Indexes for table `Station`
--
ALTER TABLE `Station`
  ADD PRIMARY KEY (`sid`),
  ADD KEY `fk_Station_Constituency_idx` (`constituency_name`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Measurement`
--
ALTER TABLE `Measurement`
  ADD CONSTRAINT `fk_Measurement_Station1` FOREIGN KEY (`station_id`) REFERENCES `Station` (`sid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `Station`
--
ALTER TABLE `Station`
  ADD CONSTRAINT `fk_Station_Constituency` FOREIGN KEY (`constituency_name`) REFERENCES `Constituency` (`c_name`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
