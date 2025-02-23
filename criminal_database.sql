-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 23, 2025 at 02:24 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `criminal_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `criminal_records`
--

CREATE TABLE `criminal_records` (
  `record_id` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `crime_description` text DEFAULT NULL,
  `case_number` varchar(100) DEFAULT NULL,
  `arrest_date` date DEFAULT NULL,
  `court_name` varchar(255) DEFAULT NULL,
  `sentencing_date` date DEFAULT NULL,
  `previous_criminal_history` text DEFAULT NULL,
  `last_known_address` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `additional_notes` text DEFAULT NULL,
  `image_dir` varchar(255) NOT NULL,
  `image` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `criminal_records`
--

INSERT INTO `criminal_records` (`record_id`, `full_name`, `date_of_birth`, `gender`, `title`, `crime_description`, `case_number`, `arrest_date`, `court_name`, `sentencing_date`, `previous_criminal_history`, `last_known_address`, `district`, `state`, `additional_notes`, `image_dir`, `image`, `created_at`, `updated_at`) VALUES
(3, 'nljkl', '2025-02-23', 'Male', 'jukjl', 'jkjk', 'hjhj', '2025-02-23', 'jnjnk', '2025-02-23', 'hbjhj', 'kjk', 'jkj', 'jkjkjk', 'jkkjjk', 'nljkl5e1df872-d574-4ea0-8961-ff9034f69b9e', '5e1df872-d574-4ea0-8961-ff9034f69b9emore-services-1.jpg', '2025-02-23 06:49:58', '2025-02-23 06:49:58'),
(4, 'Babu', '2025-02-23', 'Male', 'Rape Case', 'ghhj', 'jkjkjk', '2025-02-23', 'njjk', '2025-02-23', 'bkjkl', 'klkm', 'kllkm', 'klml', 'k.m.,', 'Babufa8d1c84-7d66-440f-8837-71964b625c9c', 'fa8d1c84-7d66-440f-8837-71964b625c9cp2.jpg', '2025-02-23 11:23:51', '2025-02-23 11:23:51'),
(5, 'Babu', '2000-01-17', 'Male', 'Test', 'jhhkjnm', 'hjjkjk', '2025-02-23', 'bkuijlk', '2025-02-23', 'nljlkkjl', 'hkjkj', 'jnkjkl', 'llkmklkl', 'lkmlklk', 'Babu108ad0f8-3581-42e5-9442-38ad54ad6404', '108ad0f8-3581-42e5-9442-38ad54ad6404p2.jpg', '2025-02-23 13:04:20', '2025-02-23 13:04:20');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password`) VALUES
(1, 'admin@gmail.com', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `criminal_records`
--
ALTER TABLE `criminal_records`
  ADD PRIMARY KEY (`record_id`),
  ADD UNIQUE KEY `case_number` (`case_number`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `criminal_records`
--
ALTER TABLE `criminal_records`
  MODIFY `record_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
