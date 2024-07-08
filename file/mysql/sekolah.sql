-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 05, 2024 at 10:00 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_pppk_petra`
--

-- --------------------------------------------------------

--
-- Table structure for table `sekolah`
--

CREATE TABLE `sekolah` (
  `id` int(11) NOT NULL,
  `kode_sekolah` varchar(256) NOT NULL,
  `nama_sekolah` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sekolah`
--

INSERT INTO `sekolah` (`id`, `kode_sekolah`, `nama_sekolah`) VALUES
(1, 'D01', 'SD Kristen Petra 1'),
(2, 'D05', 'SD Kristen Petra 5'),
(3, 'D07', 'SD Kristen Petra 7'),
(4, 'D09', 'SD Kristen Petra 9'),
(5, 'D10', 'SD Kristen Petra 10'),
(6, 'D11', 'SD Kristen Petra 11'),
(7, 'D12', 'SD Kristen Petra 12'),
(8, 'D13', 'SD Kristen Petra 13'),
(9, 'P01', 'SMP Kristen Petra 1'),
(10, 'P02', 'SMP Kristen Petra 2'),
(11, 'P03', 'SMP Kristen Petra 3'),
(12, 'P04', 'SMP Kristen Petra 4'),
(13, 'P05', 'SMP Kristen Petra 5'),
(14, 'P06', 'SMP Kristen Petra Acitya'),
(15, 'A01', 'SMA Kristen Petra 1'),
(16, 'A02', 'SMA Kristen Petra 2'),
(17, 'A03', 'SMA Kristen Petra 3'),
(18, 'A04', 'SMA Kristen Petra 4'),
(19, 'A05', 'SMA Kristen Petra 5'),
(20, 'A06', 'SMA Kristen Petra Acitya'),
(21, 'SMK', 'SMK Kristen Petra');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sekolah`
--
ALTER TABLE `sekolah`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `sekolah`
--
ALTER TABLE `sekolah`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
