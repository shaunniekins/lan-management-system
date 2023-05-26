-- phpMyAdmin SQL Dump
-- version 5.2.1-1.fc38
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 26, 2023 at 01:10 AM
-- Server version: 8.0.33
-- PHP Version: 8.2.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lan_management_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `active_user_ip`
--

CREATE TABLE `active_user_ip` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `ip_address` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_type` varchar(15) NOT NULL,
  `is_active` tinyint NOT NULL DEFAULT '0',
  `connection_ip_address` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `active_user_ip`
--

INSERT INTO `active_user_ip` (`id`, `user_id`, `ip_address`, `user_type`, `is_active`, `connection_ip_address`) VALUES
(4, 1, '192.168.1.12', 'admin', 0, NULL),
(5, 14, '192.168.1.12', 'instructor', 0, NULL),
(6, 8, '192.168.1.12', 'student', 0, ' '),
(8, 7, '192.168.1.12', 'instructor', 1, NULL),
(9, 10, '192.168.0.115', 'student', 0, ' '),
(11, 15, '192.168.1.12', 'instructor', 0, NULL),
(12, 11, '192.168.0.115', 'student', 0, ' '),
(13, 16, '192.168.0.115', 'instructor', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `avail_academic_year`
--

CREATE TABLE `avail_academic_year` (
  `id` int NOT NULL,
  `school_year` varchar(10) NOT NULL,
  `semester` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `avail_academic_year`
--

INSERT INTO `avail_academic_year` (`id`, `school_year`, `semester`) VALUES
(5, '2022-2023', '1st Semester');

-- --------------------------------------------------------

--
-- Table structure for table `avail_course`
--

CREATE TABLE `avail_course` (
  `id` int NOT NULL,
  `code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `avail_course`
--

INSERT INTO `avail_course` (`id`, `code`, `description`) VALUES
(6, 'CS', 'Computer Science');

-- --------------------------------------------------------

--
-- Table structure for table `avail_subject`
--

CREATE TABLE `avail_subject` (
  `id` int NOT NULL,
  `code` varchar(10) NOT NULL,
  `description` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `avail_subject`
--

INSERT INTO `avail_subject` (`id`, `code`, `description`) VALUES
(10, 'ITE12', 'Introduction to Programming');

-- --------------------------------------------------------

--
-- Table structure for table `enrolled_subject`
--

CREATE TABLE `enrolled_subject` (
  `id` int NOT NULL,
  `subject` int NOT NULL,
  `student` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `enrolled_subject`
--

INSERT INTO `enrolled_subject` (`id`, `subject`, `student`) VALUES
(2, 5, 8),
(3, 6, 11);

-- --------------------------------------------------------

--
-- Table structure for table `instructor_log`
--

CREATE TABLE `instructor_log` (
  `id` int NOT NULL,
  `instructor_id` int NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `hostname` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `instructor_log`
--

INSERT INTO `instructor_log` (`id`, `instructor_id`, `date`, `time`, `hostname`) VALUES
(1, 14, '2023-05-19', '13:40:00', 'fedora'),
(2, 15, '2023-05-19', '19:10:31', 'fedora'),
(3, 14, '2023-05-21', '07:40:51', 'fedora'),
(4, 14, '2023-05-22', '02:57:15', 'fedora'),
(5, 14, '2023-05-23', '08:22:07', 'fedora'),
(6, 16, '2023-05-23', '08:26:29', 'fedora'),
(7, 14, '2023-05-24', '05:24:43', 'fedora'),
(8, 14, '2023-05-26', '06:17:34', 'fedora');

-- --------------------------------------------------------

--
-- Table structure for table `registered_student_id`
--

CREATE TABLE `registered_student_id` (
  `id` int NOT NULL,
  `student_id` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `registered_student_id`
--

INSERT INTO `registered_student_id` (`id`, `student_id`) VALUES
(16, '11'),
(17, '111'),
(18, '1123'),
(19, '1212'),
(14, '122'),
(13, '1315961111'),
(15, '999');

-- --------------------------------------------------------

--
-- Table structure for table `registered_subject`
--

CREATE TABLE `registered_subject` (
  `id` int NOT NULL,
  `subject_description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `year_level` int NOT NULL,
  `section` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `course_description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `academic_school_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `academic_semester` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `instructor` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `registered_subject`
--

INSERT INTO `registered_subject` (`id`, `subject_description`, `year_level`, `section`, `course_description`, `academic_school_year`, `academic_semester`, `instructor`) VALUES
(5, 'Introduction to Programming', 2, 'A1', 'Computer Science', '2022-2023', '1st Semester', 14),
(6, 'Introduction to Programming', 3, '99', 'Computer Science', '2022-2023', '1st Semester', 16);

-- --------------------------------------------------------

--
-- Table structure for table `student_attendance`
--

CREATE TABLE `student_attendance` (
  `id` int NOT NULL,
  `student_number` int NOT NULL,
  `date` date NOT NULL,
  `time_in` time NOT NULL,
  `time_out` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `student_attendance`
--

INSERT INTO `student_attendance` (`id`, `student_number`, `date`, `time_in`, `time_out`) VALUES
(6, 10, '2023-05-12', '06:10:19', NULL),
(12, 10, '2023-05-19', '08:48:05', NULL),
(13, 8, '2023-05-19', '09:39:46', NULL),
(14, 8, '2023-05-21', '07:40:59', NULL),
(15, 8, '2023-05-22', '02:57:22', NULL),
(16, 10, '2023-05-22', '04:14:04', NULL),
(17, 8, '2023-05-23', '08:22:18', NULL),
(18, 11, '2023-05-23', '08:24:26', NULL),
(19, 8, '2023-05-24', '05:10:08', NULL),
(20, 8, '2023-05-26', '08:43:56', '09:05:59');

-- --------------------------------------------------------

--
-- Table structure for table `user_admin`
--

CREATE TABLE `user_admin` (
  `id` int NOT NULL,
  `username` varchar(15) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `password` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user_admin`
--

INSERT INTO `user_admin` (`id`, `username`, `first_name`, `last_name`, `password`) VALUES
(1, 'admin', 'admin', 'admin', '123');

-- --------------------------------------------------------

--
-- Table structure for table `user_instructor`
--

CREATE TABLE `user_instructor` (
  `id` int NOT NULL,
  `username` varchar(20) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `password` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user_instructor`
--

INSERT INTO `user_instructor` (`id`, `username`, `first_name`, `last_name`, `password`) VALUES
(14, 'bruce', 'Bruce', 'Wayne', '123'),
(15, 'clark', 'Clark', 'Kent', '123'),
(16, 'rk', 'Robert', 'Kiyosaki', '123');

-- --------------------------------------------------------

--
-- Table structure for table `user_student`
--

CREATE TABLE `user_student` (
  `id` int NOT NULL,
  `id_number` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `middle_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `last_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `year_level` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user_student`
--

INSERT INTO `user_student` (`id`, `id_number`, `username`, `first_name`, `middle_name`, `last_name`, `year_level`, `password`) VALUES
(8, '1315961111', 'edward', 'Edward', 'Duffel', 'Smith', '2', '123'),
(9, '122', 'kent', 'Clark', 'dfd', 'Kent', '2', '123'),
(10, '999', 'robin', 'Robin', 'H', 'Hood', '8', '123'),
(11, '1212', 'matt.l', 'Matt', 'L', 'Leblanc', '2', '123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `active_user_ip`
--
ALTER TABLE `active_user_ip`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `avail_academic_year`
--
ALTER TABLE `avail_academic_year`
  ADD PRIMARY KEY (`id`),
  ADD KEY `school_year` (`school_year`),
  ADD KEY `semester` (`semester`);

--
-- Indexes for table `avail_course`
--
ALTER TABLE `avail_course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `description_idx` (`description`);

--
-- Indexes for table `avail_subject`
--
ALTER TABLE `avail_subject`
  ADD PRIMARY KEY (`id`),
  ADD KEY `description` (`description`);

--
-- Indexes for table `enrolled_subject`
--
ALTER TABLE `enrolled_subject`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student` (`student`),
  ADD KEY `subject` (`subject`);

--
-- Indexes for table `instructor_log`
--
ALTER TABLE `instructor_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `instructor_id` (`instructor_id`);

--
-- Indexes for table `registered_student_id`
--
ALTER TABLE `registered_student_id`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_id` (`student_id`);

--
-- Indexes for table `registered_subject`
--
ALTER TABLE `registered_subject`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_description` (`course_description`),
  ADD KEY `subject_description` (`subject_description`),
  ADD KEY `academic_school_year` (`academic_school_year`),
  ADD KEY `academic_semester` (`academic_semester`),
  ADD KEY `instructor` (`instructor`);

--
-- Indexes for table `student_attendance`
--
ALTER TABLE `student_attendance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_number` (`student_number`);

--
-- Indexes for table `user_admin`
--
ALTER TABLE `user_admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_instructor`
--
ALTER TABLE `user_instructor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_student`
--
ALTER TABLE `user_student`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`id_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `active_user_ip`
--
ALTER TABLE `active_user_ip`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `avail_academic_year`
--
ALTER TABLE `avail_academic_year`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `avail_course`
--
ALTER TABLE `avail_course`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `avail_subject`
--
ALTER TABLE `avail_subject`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `enrolled_subject`
--
ALTER TABLE `enrolled_subject`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `instructor_log`
--
ALTER TABLE `instructor_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `registered_student_id`
--
ALTER TABLE `registered_student_id`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `registered_subject`
--
ALTER TABLE `registered_subject`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `student_attendance`
--
ALTER TABLE `student_attendance`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `user_admin`
--
ALTER TABLE `user_admin`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user_instructor`
--
ALTER TABLE `user_instructor`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `user_student`
--
ALTER TABLE `user_student`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `enrolled_subject`
--
ALTER TABLE `enrolled_subject`
  ADD CONSTRAINT `enrolled_subject_ibfk_1` FOREIGN KEY (`student`) REFERENCES `user_student` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `enrolled_subject_ibfk_2` FOREIGN KEY (`subject`) REFERENCES `registered_subject` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `instructor_log`
--
ALTER TABLE `instructor_log`
  ADD CONSTRAINT `instructor_log_ibfk_1` FOREIGN KEY (`instructor_id`) REFERENCES `user_instructor` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `registered_subject`
--
ALTER TABLE `registered_subject`
  ADD CONSTRAINT `registered_subject_ibfk_3` FOREIGN KEY (`academic_school_year`) REFERENCES `avail_academic_year` (`school_year`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `registered_subject_ibfk_4` FOREIGN KEY (`academic_semester`) REFERENCES `avail_academic_year` (`semester`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `registered_subject_ibfk_5` FOREIGN KEY (`instructor`) REFERENCES `user_instructor` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `registered_subject_ibfk_6` FOREIGN KEY (`course_description`) REFERENCES `avail_course` (`description`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `student_attendance`
--
ALTER TABLE `student_attendance`
  ADD CONSTRAINT `student_attendance_ibfk_1` FOREIGN KEY (`student_number`) REFERENCES `user_student` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `user_student`
--
ALTER TABLE `user_student`
  ADD CONSTRAINT `user_student_ibfk_1` FOREIGN KEY (`id_number`) REFERENCES `registered_student_id` (`student_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
