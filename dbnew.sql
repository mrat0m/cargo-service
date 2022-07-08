/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.7.9 : Database - c_binup
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`c_bin` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `c_bin`;

/*Table structure for table `bookings` */

DROP TABLE IF EXISTS `bookings`;

CREATE TABLE `bookings` (
  `booking_id` int(50) NOT NULL AUTO_INCREMENT,
  `customer_id` int(50) DEFAULT NULL,
  `booking_date` varchar(50) DEFAULT NULL,
  `from_loc` varchar(50) DEFAULT NULL,
  `toloc` varchar(50) DEFAULT NULL,
  `weight` varchar(50) DEFAULT NULL,
  `length` varchar(50) DEFAULT NULL,
  `width` varchar(50) DEFAULT NULL,
  `from_branch` int(50) DEFAULT NULL,
  `to_branch` int(50) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `booking_status` varchar(50) DEFAULT NULL,
  `pack_id` int(50) DEFAULT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `bookings` */
insert  into `bookings`(`booking_id`,`customer_id`,`booking_date`,`from_loc`,`toloc`,`weight`,`length`,`width`,`from_branch`,`to_branch`,`amount`,`booking_status`,`boy_id`,`pack_id`) values (1,1,'2022-03-21','EE','YY','500','55','666',1,1,'Pending','Pending',0,1),(2,1,'2022-03-21','bridge','chpel','500','55','666',1,2,'10000','delivered',2,1);

/*Table structure for table `branches` */

DROP TABLE IF EXISTS `branches`;

CREATE TABLE `branches` (
  `branch_id` int(50) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `branch_name` varchar(50) DEFAULT NULL,
  `latitude` varchar(50) DEFAULT NULL,
  `longitude` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`branch_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `branches` */

insert  into `branches`(`branch_id`,`username`,`branch_name`,`latitude`,`longitude`,`phone`,`email`) values (1,'vypin','vypin','9.988800214678564','76.27249717712402','9876546543','vishnu@gmail.com'),(2,'kochi','kochi','9.988293036447752','76.28811836242676','9876546543','buyer@gmail.com');

/*Table structure for table `cargo_status` */

DROP TABLE IF EXISTS `cargo_status`;

CREATE TABLE `cargo_status` (
  `status_id` int(50) NOT NULL AUTO_INCREMENT,
  `booking_id` int(50) DEFAULT NULL,
  `place_name` varchar(50) DEFAULT NULL,
  `status_date_time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`status_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `cargo_status` */

insert  into `cargo_status`(`status_id`,`booking_id`,`place_name`,`status_date_time`) values (1,2,'qwwerr','2022-03-21 18:00:48');

/*Table structure for table `customers` */

DROP TABLE IF EXISTS `customers`;

CREATE TABLE `customers` (
  `customer_id` int(50) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `latitude` varchar(50) DEFAULT NULL,
  `longitude` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `customers` */

insert  into `customers`(`customer_id`,`username`,`first_name`,`last_name`,`phone`,`email`,`latitude`,`longitude`) values (1,'customer','customer','wer','9876546543','customer@gmail.com','9.976712251779837','76.28459930419922');

/*Table structure for table `deliveryboys` */

DROP TABLE IF EXISTS `deliveryboys`;

CREATE TABLE `deliveryboys` (
  `boy_id` int(50) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `branch_id` int(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`boy_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `deliveryboys` */

insert  into `deliveryboys`(`boy_id`,`username`,`first_name`,`last_name`,`branch_id`,`phone`,`email`) values (1,'vypindboy','vypindboy','hh',1,'9876546543','wells@gmail.com'),(2,'kochidboy','KOCHIDBOY','xdfg',2,'9876546543','joyelroy24@gmail.com');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(50) NOT NULL AUTO_INCREMENT,
  `customer_id` int(50) DEFAULT NULL,
  `branch_id` int(50) DEFAULT NULL,
  `feedback_description` varchar(50) DEFAULT NULL,
  `reply` varchar(50) DEFAULT NULL,
  `feedback_date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `user_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`username`,`password`,`user_type`) values ('admin','admin','admin'),('customer','customercustomer','customer'),('vypin','vypinvypin','branch'),('kochi','kochikochi','branch'),('vypindboy','vypindboy','dboy'),('kochidboy','dboyk','dboy'),('kochinstaff','kochinstaffyy','staff'),('vypinstaff','vypinstaff','staff');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(50) NOT NULL AUTO_INCREMENT,
  `booking_id` int(50) DEFAULT NULL,
  `amount_paid` varchar(50) DEFAULT NULL,
  `payment_date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`booking_id`,`amount_paid`,`payment_date`) values (1,2,'10000','2022-03-21 17:54:37');

/*Table structure for table `packages` */

DROP TABLE IF EXISTS `packages`;

CREATE TABLE `packages` (
  `pack_id` int(50) NOT NULL AUTO_INCREMENT,
  `packname` varchar(50) DEFAULT NULL,
  `maximum_weight` varchar(50) DEFAULT NULL,
  `maximum_height` varchar(50) DEFAULT NULL,
  `maximum_width` varchar(50) DEFAULT NULL,
  `maximum_distance` varchar(50) DEFAULT NULL,
  `minimum_price` varchar(50) DEFAULT NULL,
  `pstatus` varcpack_idDEFAULT NULL,
  PRIMARY KEY (`pack_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `packages` */
pack_id
insert  into `packages`(`pack_id`,`packname`,`maximum_weight`,`maximum_height`,`maximum_width`,`maximum_distance`,`minimum_price`,`pstatus`) values (1,'pack3','500','55','666','55','10000','active'),(2,'pack1','577','345','567','55','1500','active');

/*Table structure for table `resign_request` */

DROP TABLE IF EXISTS `resign_request`;

CREATE TABLE `resign_request` (
  `resign_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `reason` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`resign_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `resign_request` */

/*Table structure for table `review_rating` */

DROP TABLE IF EXISTS `review_rating`;

CREATE TABLE `review_rating` (
  `review_id` int(50) NOT NULL AUTO_INCREMENT,
  `customer_id` int(50) DEFAULT NULL,
  `branch_id` int(50) DEFAULT NULL,
  `review_comment` varchar(50) DEFAULT NULL,
  `rating_point` varchar(50) DEFAULT NULL,
  `review_date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`review_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `review_rating` */

/*Table structure for table `staffs` */

DROP TABLE IF EXISTS `staffs`;

CREATE TABLE `staffs` (
  `staff_id` int(50) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `branch` int(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`staff_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `staffs` */

insert  into `staffs`(`staff_id`,`username`,`first_name`,`last_name`,`branch`,`phone`,`email`) values (1,'kochinstaff','KOCHISTAFF','TT',2,'9876546543','joyelroy24@gmail.com'),(2,'vypinstaff','VYPINSTAFF','fs',1,'9876546543','vishnu@gmail.com');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
