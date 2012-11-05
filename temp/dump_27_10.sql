-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 27, 2012 at 09:05 AM
-- Server version: 5.5.27
-- PHP Version: 5.4.6-1ubuntu1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `linetshop`
--

-- --------------------------------------------------------

--
-- Table structure for table `main_brand`
--

CREATE TABLE IF NOT EXISTS `main_brand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `new_title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `new_url` varchar(255) DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;


-- --------------------------------------------------------

--
-- Table structure for table `main_category`
--
CREATE TABLE IF NOT EXISTS `main_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `new_title` varchar(255) DEFAULT NULL,
  `piture` varchar(255) DEFAULT NULL,
  `count_products` int(11) DEFAULT NULL,
  `ord` int(11) DEFAULT NULL,
  `hide_pictures` int(11) DEFAULT NULL,
  `display` tinyint(1) NOT NULL DEFAULT '1',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `main_category_63f17a16` (`parent_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;


-- --------------------------------------------------------

--
-- Table structure for table `main_paytype`
--

CREATE TABLE IF NOT EXISTS `main_paytype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `currency_name` varchar(255) DEFAULT NULL,
  `new_currency_name` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `new_title` varchar(255) DEFAULT NULL,
  `rate_usd` double DEFAULT NULL,
  `rate_uah` double DEFAULT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `main_product`
--

CREATE TABLE IF NOT EXISTS `main_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `brand_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `currency` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `new_title` varchar(255) DEFAULT NULL,
  `description` longtext,
  `new_description` longtext,
  `features` longtext,
  `new_features` longtext,
  `price` double DEFAULT NULL,
  `new_price` double DEFAULT NULL,
  `garant` int(11) DEFAULT NULL,
  `display` tinyint(1) NOT NULL DEFAULT '1',
  `bestseller` tinyint(1) NOT NULL DEFAULT '0',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `weight` varchar(255) DEFAULT NULL,
  `available_date` varchar(255) DEFAULT NULL,
  `actual_date` varchar(255) DEFAULT NULL,
  `photo` int(11) DEFAULT NULL,
  `ord` int(11) DEFAULT NULL,
  `mtstamp` int(11) DEFAULT NULL,
  `preview_height` int(11) DEFAULT NULL,
  `preview_width` int(11) DEFAULT NULL,
  `recomended` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `source` (`source`),
  KEY `main_product_42dc49bc` (`category_id`),
  KEY `main_product_74876276` (`brand_id`),
  KEY `main_product_44224078` (`status_id`),
  KEY `main_product_41f657b3` (`currency_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5000;
-- --------------------------------------------------------

--
-- Table structure for table `main_settings`
--

CREATE TABLE IF NOT EXISTS `main_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `keywords` varchar(255) DEFAULT NULL,
  `favicon` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `fax` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `main_settings`
--

INSERT INTO `main_settings` (`id`, `title`, `description`, `keywords`, `favicon`, `email`, `phone`, `fax`, `address`) VALUES
(1, 'Linet Shop', 'Продажа всякого барахла', 'Лептоп, Компьютер, Принтер', '', 'wikitorya@gmail.com', '(+456) 94-09-445', '(+456) 94-09-444', 'ул. Койкого, 35 г. Запорожье');

-- --------------------------------------------------------

--
-- Table structure for table `main_status`
--

CREATE TABLE IF NOT EXISTS `main_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `short_title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `main_status`
--

INSERT INTO `main_status` (`id`, `title`, `short_title`) VALUES
(1, 'Товар недоступен', 'Нет'),
(2, 'Товар есть в наличии', 'Есть'),
(3, 'Есть в наличии, в резерве', 'В резерве'),
(4, 'Ожидается поступление', 'Ожидается'),
(5, 'Товар доступен под заказ', 'Под заказ'),
(6, '', ''),
(7, '', ''),
(8, '', ''),
(9, 'Нет в наличии, уточняйте доступность у менеджера', 'Нет');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `main_category`
--
ALTER TABLE `main_category`
  ADD CONSTRAINT `parent_id_refs_id_4a3cf3b3` FOREIGN KEY (`parent_id`) REFERENCES `main_category` (`id`);

--
-- Constraints for table `main_product`
--
ALTER TABLE `main_product`
  ADD CONSTRAINT `brand_id_refs_id_2dac6de5` FOREIGN KEY (`brand_id`) REFERENCES `main_brand` (`id`),
  ADD CONSTRAINT `category_id_refs_id_7095e957` FOREIGN KEY (`category_id`) REFERENCES `main_category` (`id`),
  ADD CONSTRAINT `currency_id_refs_id_6edb72b4` FOREIGN KEY (`currency_id`) REFERENCES `main_paytype` (`id`),
  ADD CONSTRAINT `status_id_refs_id_4d6da36b` FOREIGN KEY (`status_id`) REFERENCES `main_status` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
